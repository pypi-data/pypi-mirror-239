import copy
import logging
from pathlib import Path
from typing import Union

from PIL import Image
import torch

import explainer._default_pipeline as _default_pipeline
from explainer.datasets import DatasetHandler
from explainer.models import ModelLoader
from explainer.util import enums
from explainer.util.filehandling import ensure_dir
from explainer.util.functionalities import init_cuda, timeit
from explainer.util.return_types import Result


class Explainer:
    """
    Entry point for the explainer. This class is used to start the explanation process.

    Args:
        working_dir (Union[str, Path]): The working directory where local files are stored.

    Keyword Args:
        dataset (str): The dataset to use. Default: "pascal"
        device (Union[str, torch.device]): The device to use. Default: "cpu"
        object_model (str): The object model to use. Default: "cam"
        parts_model (str): The parts model to use. Default: "resnet"
        segmentation_method (str): The segmentation method to use. Default: "default"

    Example:
        >>> from explainer import Explainer
        >>> explainer = Explainer("./testing_cwd", device="cuda", object_model="cam")
        >>> img = Image.open("example_image.jpg")
        >>> result = explainer(img)
    """

    @timeit
    def __init__(
        self,
        working_dir: Union[str, Path],
        dataset: str = "pascal",
        device: Union[str, torch.device] = "cpu",
        object_model: str = "cam",
        parts_model: str = "resnet",
        segmentation_method: str = "default",
    ):
        self._working_dir = Path(working_dir)
        ensure_dir(self._working_dir)
        ensure_dir(self._working_dir / "models")

        self._model_loader = ModelLoader(self.working_dir / "models")
        self._dataset_handler = DatasetHandler()

        self.set_dataset(dataset)
        self.set_device(device)
        self.set_object_model(object_model)
        self.set_parts_model(parts_model)
        self.set_segmentation_method(segmentation_method)

    # class methods
    def __call__(self, img: Image.Image) -> Result:
        """
        Start the explainer process.

        Args:
            img (Image.Image): The image to explain.

        Returns:
            Result: The explanation, which can be converted to a dict using its "to_dict" method. See explainer.util.return_types.Result for more information.
        """
        img, object_data, parts_data = self._init_run(img)

        pipeline_args = (
            img,
            self._loaded_object_model,
            self._loaded_parts_model,
            object_data,
            parts_data,
            self.segmentation_method,
        )  # just for better readability

        return _default_pipeline.run(*pipeline_args)

    def __repr__(self):
        return (
            f"Explainer(working_dir={self.working_dir}, "
            f"dataset={self.dataset}, "
            f"device={self.device}, "
            f"object_model={self.object_model}, "
            f"parts_model={self.parts_model}, "
            f"segmentation_method={self.segmentation_method})"
        )

    def __str__(self):
        return self.__repr__()

    def update_model_weights(self):
        self._model_loader.update_models()

    def delete_model_weights(self):
        self._model_loader.delete_models()

    def _init_run(self, img: Image.Image):
        logging.info(f"Starting {self}...")

        # check input
        assert isinstance(
            img, Image.Image
        ), f"img must be of type PIL.Image.Image, but is {type(img)}"

        img = copy.deepcopy(img)  # don't modify the original image

        object_data = self._dataset_handler.get_dataset(self.dataset, "object_model")
        parts_data = self._dataset_handler.get_dataset(self.dataset, "parts_model")

        return img, object_data, parts_data

    # properties
    @property
    def working_dir(self) -> Path:
        return self._working_dir

    @property
    def device(self) -> torch.device:
        return self._device

    @property
    def dataset(self) -> str:
        return self._dataset.name

    @property
    def object_model(self) -> str:
        return self._object_model.name

    @property
    def parts_model(self) -> str:
        return self._parts_model.name

    @property
    def segmentation_method(self) -> str:
        return self._segmentation_method.name

    # setter functions implementing chaining
    def set_dataset(self, dataset: str) -> "Explainer":
        assert isinstance(
            dataset, str
        ), f"dataset must be of type str, but is {type(dataset)}"

        try:
            self._dataset = enums.Dataset[dataset]
        except KeyError:
            raise ValueError(
                f"dataset must be one of {enums.Dataset}, but is {dataset}"
            )

        return self

    def set_device(self, device: Union[str, torch.device]) -> "Explainer":
        self._device = (
            init_cuda(device_id=device)
            if not isinstance(device, torch.device)
            else device
        )

        return self

    def set_object_model(self, model_name: str) -> "Explainer":
        assert isinstance(
            model_name, str
        ), f"model must be of type str, but is {type(model_name)}"

        try:
            self._object_model = enums.ObjectModel[model_name]
        except KeyError:
            raise ValueError(
                f"model_name must be one of {enums.ObjectModel}, but is {model_name}"
            )

        self._loaded_object_model = self._model_loader.get_model(
            model_name=self.object_model, dataset=self.dataset, device=self.device
        )
        return self

    def set_parts_model(self, model_name: str) -> "Explainer":
        assert isinstance(
            model_name, str
        ), f"model must be of type str, but is {type(model_name)}"

        try:
            self._parts_model = enums.PartsModel[model_name]
        except KeyError:
            raise ValueError(
                f"model_name must be one of {enums.PartsModel}, but is {model_name}"
            )

        self._loaded_parts_model = self._model_loader.get_model(
            model_name=self.parts_model, dataset=self.dataset, device=self.device
        )

        return self

    def set_segmentation_method(self, segmentation_method: str) -> "Explainer":
        assert isinstance(
            segmentation_method, str
        ), f"segmentation_method must be of type str, but is {type(segmentation_method)}"

        try:
            self._segmentation_method = enums.SegmentationMethod[segmentation_method]
        except KeyError:
            raise ValueError(
                f"segmentation_method must be one of {enums.SegmentationMethod}, but is {segmentation_method}"
            )

        return self
