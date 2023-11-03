import copy
import logging
from pathlib import Path
from typing import Union

from PIL import Image
import torch

import explainer._default_pipeline as _default_pipeline  # explicit import
from explainer.datasets import DatasetHandler
from explainer.models import ModelLoader
from explainer.util import enums
from explainer.util.filehandling import clear_directory, ensure_dir
from explainer.util.functionalities import init_cuda, timeit, unify_string
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
        enable_model_caching (bool): Whether to cache the models. Default: True

    Example:
        >>> from explainer import Explainer
        >>> explainer = Explainer(".", device="gpu", object_model="vit")
        >>> img = Image.open("example_image.jpg")
        >>> result = explainer(img)
    """

    def __init__(
        self,
        working_dir: Union[str, Path],
        dataset: str = "pascal",
        device: Union[str, torch.device] = "cpu",
        object_model: str = "cam",
        parts_model: str = "resnet",
        enable_model_caching: bool = True,
    ):
        self._dataset = None
        self._device = None
        self._object_model = None
        self._parts_model = None

        self.set_dataset(dataset)
        self.set_device(device)
        self.set_object_model(object_model)
        self.set_parts_model(parts_model)

        self._working_dir = self._setup_directory(working_dir)

        self._model_loader = ModelLoader(
            self.working_dir / "models", enable_model_caching
        )
        self._dataset_handler = DatasetHandler()

    # init methods
    def _setup_directory(self, path) -> Path:
        """
        Initialize the working directory.

        Args:
            path (Union[str, Path]): Path to the working directory.

        Returns:
            Path: Path to the working directory.
        """
        path = Path(path)

        ensure_dir(path)
        # ensure_dir(path / "cache")
        ensure_dir(path / "models")
        # ensure_dir(path / "logs")
        ensure_dir(path / "tmp")

        logging.debug(f"Working directory: {path}")

        return path

    # class methods
    def __call__(self, img: Image.Image) -> Result:
        """
        Start the explainer process.

        Args:
            img (Image.Image): The image to explain.

        Returns:
            Result: The explanation, which can be converted to a dict using its "to_dict" method. See explainer.util.return_types.Result for more information.
        """
        # start explainer
        return self._run_pipeline(img)

    def update_models(self):
        self._model_loader.update_models()

    def delete_models(self):
        self._model_loader.delete_models()

    def enable_model_caching(self):
        self._model_loader.enable_caching()

    def disable_model_caching(self):
        self._model_loader.disable_caching()

    #  private methods
    def _clear_tmp_directory(self):
        clear_directory(self.working_dir / "tmp")

    @timeit
    def _init_run(self, img: Image.Image):
        logging.info("Starting explainer...")
        logging.info(f"Working directory: {self.working_dir}")
        logging.info(f"Dataset: {self.dataset}")
        logging.info(f"Device: {self.device}")
        logging.info(f"Object model: {self.object_model}")
        logging.info(f"Parts model: {self.parts_model}")

        # check input
        assert isinstance(
            img, Image.Image
        ), f"img must be of type PIL.Image.Image, but is {type(img)}"

        # clear tmp directory
        self._clear_tmp_directory()

        img = copy.deepcopy(img)  # don't modify the original image

        object_model = self._model_loader.get_model(
            model_name=self.object_model, dataset=self.dataset, device=self.device
        )

        parts_model = self._model_loader.get_model(
            model_name=self.parts_model, dataset=self.dataset, device=self.device
        )

        object_data = self._dataset_handler.get_dataset(
            dataset_name=self.dataset, model_type="object_model"
        )

        parts_data = self._dataset_handler.get_dataset(
            dataset_name=self.dataset, model_type="parts_model"
        )

        return img, object_model, parts_model, object_data, parts_data

    @timeit
    def _run_pipeline(self, img: Image.Image) -> Result:
        # load models and datasets
        img, object_model, parts_model, object_data, parts_data = self._init_run(img)

        result = _default_pipeline.run(
            img=img,
            object_model=object_model,
            parts_model=parts_model,
            object_data=object_data,
            parts_data=parts_data,
        )

        return result

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

    # setter functions implementing chaining
    def set_dataset(self, dataset: str) -> "Explainer":
        assert isinstance(
            dataset, str
        ), f"dataset must be of type str, but is {type(dataset)}"

        dataset = unify_string(dataset)

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

        model_name = unify_string(model_name)

        try:
            self._object_model = enums.ObjectModel[model_name]
        except KeyError:
            raise ValueError(
                f"model_name must be one of {enums.ObjectModel}, but is {model_name}"
            )

        return self

    def set_parts_model(self, model_name: str) -> "Explainer":
        assert isinstance(
            model_name, str
        ), f"model must be of type str, but is {type(model_name)}"

        model_name = unify_string(model_name)

        try:
            self._parts_model = enums.PartsModel[model_name]
        except KeyError:
            raise ValueError(
                f"model_name must be one of {enums.PartsModel}, but is {model_name}"
            )

        return self
