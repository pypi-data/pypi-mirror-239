from typing import List

from PIL import Image
import numpy as np
import torch
from torch import nn
from torchvision import transforms

from explainer.datasets.base import Dataset
from explainer.grabcut.grabcut import relevantAreaMask
from explainer.models.base import ExplainedInput
from explainer.part_extr import extract_parts as part_extraction
from explainer.pre_seg import extract_relevant_segments, merge_neighbors, segment
from explainer.util.functionalities import timeit
from explainer.util.return_types import Object, Part, Result


@timeit
def _run_object_model(
    img: Image, model: torch.nn.Module, dataset: Dataset
) -> ExplainedInput:
    img = dataset.transform(img).to(model.device())

    assert (
        model.device() == img.device
    ), f"Model device: {model.device()} != image device: {img.device}"

    # run model
    out = model.explain(img)[0]

    return out


def _extract_parts(
    heatmap: np.ndarray,
    img: np.ndarray,
    n_segments: int = 1000,  # number of segments in initial segmentation
    compactness: int = 10,  # compactness of segmentation
    grabcut: bool = False,
    extraction_method="threshold",  # No grabcut: Method for selecting relevant segments. Options "threshold", "top_k_segments"
    threshold=0.35,  # No grabcut: Threshold when using method "threshold"
    num_segments=10,  # No grabcut: Number of segments when using method "top_k_segments"
    thresh_fgd=0.8,  # With grabcut: threshold for sure foreground
    thresh_bgd=0.4,  # With grabcut: threshold for sure background
    seg_method="slic",  # "felzenszwalb" # "slic" # "watershed" # "quickshift
    merge_method="louvain",  # "normalized_graph_cut" # "greedy_modularity" # "girvan_newman" # "louvain"
    num_parts=5,  # only relevant for  "normalized_graph_cut" and "girvan_newman"
):
    if grabcut:
        relevant_area = relevantAreaMask(img, heatmap, thresh_bgd, thresh_fgd)

        seg_img = segment(
            img=img,
            method=seg_method,
            n_segments=n_segments,
            compactness=compactness,
            mask=relevant_area,
        )
        seg_img[seg_img == 1] = 0

        relevant_segments = merge_neighbors(seg_img, heatmap, merge_method, num_parts)
    else:
        seg_img = segment(
            img=img,
            method=seg_method,
            n_segments=n_segments,
            compactness=compactness,
        )

        relevant_segments = extract_relevant_segments(
            segmentation=seg_img,
            heatmap=heatmap,
            evaluation_method="mean",
            merge_neightbors=True,
            num_pixels=-1,
            extraction_method=extraction_method,
            threshold=threshold,
            num_segments=num_segments,
            partition_method=merge_method,
            num_parts=num_parts,
        )

    parts = part_extraction(
        segmentation=relevant_segments,
        image=img,
        heatmap=heatmap,
        cut=True,
        replace="blur",
    )

    return parts


@timeit
def extract_parts(np_img, heatmap, **kwargs):
    use_grabcut = kwargs.get("grabcut", False)
    segmentation_method = kwargs.get("seg_method", "slic")

    exctracted_parts: List[tuple] = _extract_parts(
        heatmap,
        np_img,
        grabcut=use_grabcut,
        seg_method=segmentation_method,
        n_segments=200 if use_grabcut else 1000,
    )

    return exctracted_parts


def _run_parts_model(img: Image, model: torch.nn.Module, dataset: Dataset, **kwargs):
    img = dataset.transform(img).to(model.device())
    img = img.unsqueeze(0)

    _idx_to_name = {}

    _idx = 0
    for class_, _parts in dataset.parts.items():
        for _part in _parts:
            _idx_to_name[_idx] = (class_, _part)
            _idx += 1

    with torch.no_grad():
        out = model(img)[0]

    out = nn.Sigmoid()(out)
    out = out.squeeze().cpu().numpy()
    class_labels = np.argwhere(out > 0.5).flatten().tolist()

    class_labels = (
        [_idx_to_name[idx] for idx in class_labels] if len(class_labels) else []
    )

    # organize parts by class
    class_labels_organized = {class_: [] for class_, _ in class_labels}
    for class_, part_ in class_labels:
        class_labels_organized[class_].append(part_)

    return class_labels_organized


def _process_explaination(label, heatmap, img, class_map: dict):
    label_name = class_map[label]

    np_img = np.array(img)

    heatmap = heatmap.unsqueeze(0) if len(heatmap.shape) == 2 else heatmap

    assert (
        len(heatmap.shape) == 3
    ), f"heatmap.shape = {heatmap.shape} != (1, H, W) or (C, H, W)"

    heatmap = transforms.Resize((np_img.shape[0], np_img.shape[1]), antialias=True)(
        heatmap
    )
    heatmap = heatmap.squeeze().numpy(force=True)

    return label_name, heatmap, np_img


@timeit
def _process_parts(exctracted_parts, parts_model, parts_data, **kwargs):
    """
    Outer loop for processing parts.

    Args:
        exctracted_parts (list): List of tuples (part_img, relevancy).
        parts_model (torch.nn.Module): Parts model.
        parts_data (Dataset): Parts dataset.
        kwargs: Additional arguments.

    Returns:
        list: List of Part objects.
    """

    _parts_collector = []

    for i, (part_img, relevancy, rect) in enumerate(exctracted_parts):
        part_img = Image.fromarray(part_img)

        part_labels = _run_parts_model(
            part_img,
            parts_model,
            parts_data,
            **kwargs,
        )

        _parts_collector.append(
            Part(
                img=part_img,
                relevancy=relevancy,
                labels=part_labels,
                rect=rect,
            )
        )

    return _parts_collector


@timeit
def run(
    img: Image.Image,
    object_model: torch.nn.Module,
    parts_model: torch.nn.Module,
    object_data: Dataset,
    parts_data: Dataset,
) -> Result:
    # run object model and get explained input
    explained_input = _run_object_model(img, object_model, object_data)

    # create a mapping from class index to class name
    class_map = {idx: name for idx, name in enumerate(object_data.get_classes())}

    _object_collector = []

    for label, heatmap in explained_input:
        # do some preprocessing on the explained input
        _explaination = _process_explaination(label, heatmap, img, class_map)
        label_name: str = _explaination[0]  # for example: "person"
        heatmap: np.ndarray = _explaination[1]  # 2D-array with values in range [0, 1]
        np_img: np.ndarray = _explaination[2]  # RBG values in range [0, 255]

        extracted_parts = extract_parts(
            heatmap=heatmap,
            np_img=np_img,
        )

        collected_parts: List[Part] = _process_parts(
            extracted_parts, parts_model, parts_data
        )

        _object_collector.append(
            Object(
                label=label_name,
                heatmap=heatmap,
                parts=collected_parts,
            )
        )

    return Result(img=img, objects=_object_collector)
