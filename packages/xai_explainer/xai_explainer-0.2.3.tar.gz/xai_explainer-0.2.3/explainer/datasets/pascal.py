from typing import List

from PIL import Image
from torchvision import transforms

from .base import Dataset


class Pascal(Dataset):
    categories = [
        "aeroplane",
        "bicycle",
        "bird",
        "boat",
        "bottle",
        "bus",
        "car",
        "cat",
        "chair",
        "cow",
        "diningtable",
        "dog",
        "horse",
        "motorbike",
        "person",
        "pottedplant",
        "sheep",
        "sofa",
        "train",
        "tvmonitor",
    ]

    @staticmethod
    def transform(img: Image):
        size = 224
        return transforms.Compose(
            [
                transforms.Resize(size),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )(img)

    @staticmethod
    def get_classes() -> List[str]:
        return Pascal.categories

    @staticmethod
    def get_num_classes() -> int:
        return len(Pascal.categories)

    @staticmethod
    def class_index_to_name(idx: int) -> str:
        return Pascal.categories[idx]


class PascalParts(Dataset):
    parts = {
        "aeroplane": ["body", "stern", "lwing", "rwing", "tail", "engine", "wheel"],
        "bicycle": [
            "fwheel",
            "bwheel",
            "saddle",
            "handlebar",
            "chainwheel",
            "headlight",
        ],
        "bird": [
            "head",
            "leye",
            "reye",
            "beak",
            "torso",
            "neck",
            "lwing",
            "rwing",
            "lleg",
            "lfoot",
            "rleg",
            "rfoot",
            "tail",
        ],
        "boat": [],
        "bottle": ["cap", "body"],
        "bus": [
            "frontside",
            "leftside",
            "rightside",
            "backside",
            "roofside",
            "leftmirror",
            "rightmirror",
            "fliplate",
            "bliplate",
            "door",
            "wheel",
            "headlight",
            "window",
        ],
        "car": [
            "frontside",
            "leftside",
            "rightside",
            "backside",
            "roofside",
            "leftmirror",
            "rightmirror",
            "fliplate",
            "bliplate",
            "door",
            "wheel",
            "headlight",
            "window",
        ],
        "cat": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "nose",
            "torso",
            "neck",
            "lfleg",
            "lfpa",
            "rfleg",
            "rfpa",
            "lbleg",
            "lbpa",
            "rbleg",
            "rbpa",
            "tail",
        ],
        "chair": [],
        "cow": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "muzzle",
            "lhorn",
            "rhorn",
            "torso",
            "neck",
            "lfuleg",
            "lflleg",
            "rfuleg",
            "rflleg",
            "lbuleg",
            "lblleg",
            "rbuleg",
            "rblleg",
            "tail",
        ],
        "table": [],
        "dog": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "nose",
            "torso",
            "neck",
            "lfleg",
            "lfpa",
            "rfleg",
            "rfpa",
            "lbleg",
            "lbpa",
            "rbleg",
            "rbpa",
            "tail",
            "muzzle",
        ],
        "horse": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "muzzle",
            "lfho",
            "rfho",
            "lbho",
            "rbho",
            "torso",
            "neck",
            "lfuleg",
            "lflleg",
            "rfuleg",
            "rflleg",
            "lbuleg",
            "lblleg",
            "rbuleg",
            "rblleg",
            "tail",
        ],
        "motorbike": ["fwheel", "bwheel", "handlebar", "saddle", "headlight"],
        "person": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "lebrow",
            "rebrow",
            "nose",
            "mouth",
            "hair",
            "torso",
            "neck",
            "llarm",
            "luarm",
            "lhand",
            "rlarm",
            "ruarm",
            "rhand",
            "llleg",
            "luleg",
            "lfoot",
            "rlleg",
            "ruleg",
            "rfoot",
        ],
        "pottedplant": ["pot", "plant"],
        "sheep": [
            "head",
            "leye",
            "reye",
            "lear",
            "rear",
            "muzzle",
            "lhorn",
            "rhorn",
            "torso",
            "neck",
            "lfuleg",
            "lflleg",
            "rfuleg",
            "rflleg",
            "lbuleg",
            "lblleg",
            "rbuleg",
            "rblleg",
            "tail",
        ],
        "sofa": [],
        "train": [
            "head",
            "hfrontside",
            "hleftside",
            "hrightside",
            "hbackside",
            "hroofside",
            "headlight",
            "coach",
            "cfrontside",
            "cleftside",
            "crightside",
            "cbackside",
            "croofside",
        ],
        "tvmonitor": [
            "screen",
            "frame",
        ],  # NOTE: frame was missing in the paper! See https://github.com/pmeletis/panoptic_parts/blob/v2.0/panoptic_parts/specs/dataset_specs/ppp_datasetspec.yaml for correct version
    }

    @staticmethod
    def transform(img: Image):
        size = 128
        return transforms.Compose(
            [
                transforms.Resize(size),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )(img)
