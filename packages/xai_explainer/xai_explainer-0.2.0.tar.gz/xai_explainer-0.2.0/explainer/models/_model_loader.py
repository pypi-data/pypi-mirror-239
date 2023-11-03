import dataclasses
import logging
from pathlib import Path
from typing import Callable

import torch

from explainer.models.base import BaseExplainableModel
from explainer.util.filehandling import download_url
from explainer.util.functionalities import unify_string


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class ModelKey:
    model: str
    dataset: str
    uid: str = None


@dataclasses.dataclass(frozen=True)
class RegisteredModel:
    model_handle: Callable  # Handle to the model class
    weights_url: str  # URL to download the model weights from
    weights_file: Path  # Local path to the weights file
    _key: ModelKey  # Unique key for the model
    defaults: dict = dataclasses.field(default_factory=dict)

    def download_weights(self):
        self.delete_local_weights()
        try:
            download_url(self.weights_url, self.weights_file)
        except Exception:
            raise RuntimeError(
                f"Could not download weights for {self.model_handle.__name__}."
            )

    def delete_local_weights(self):
        if self.weights_file.exists():
            self.weights_file.unlink()

    def new_weights_available(self):
        return False  # TODO: implement

    @property
    def download_required(self):
        return not self.weights_file.exists() or self.new_weights_available()

    def initialize(self, device: torch.device, **kwargs) -> BaseExplainableModel:
        """Initialize the model."""

        _kwargs = self.defaults.copy()
        _kwargs.update(kwargs)

        model = self.model_handle(**_kwargs)

        if self.download_required:
            self.download_weights()

        if self.weights_file.exists():
            state_dict = torch.load(self.weights_file, map_location=device)
            model.load_state_dict(state_dict)
        else:
            logging.warning(f"No weights available for {self.model_handle.__name__}.")

        try:
            model.unfreeze()  # unfreeze all layers
        except AttributeError:
            pass

        model.to(device)
        model.eval()

        return model


class ModelLoader:
    def __init__(
        self,
        model_directory: Path,
        cache_models: bool,
        _register_default_models: bool = True,
    ):
        self._models = {}
        self._model_dir = model_directory
        self._cache_models = cache_models

        if _register_default_models:
            self._register_default_models()

    def _register_default_models(self):
        from .object_model.ViT import ViT
        from .object_model.cam import Cam
        from .object_model.prm.resnet import PRM
        from .parts_model.resnet_based import ResNetParts

        self.register_model(
            Cam,
            dataset="pascal",
            weight_url="https://tu-dortmund.sciebo.de/s/2UeO47mYjEx5YKt/download",
            num_classes=20,
        )

        self.register_model(
            PRM,
            dataset="pascal",
            weight_url="https://tu-dortmund.sciebo.de/s/8mX0HD7GSP1Eqcn/download",
            num_classes=20,
        )

        self.register_model(
            ViT,
            dataset="pascal",
            weight_url="https://tu-dortmund.sciebo.de/s/jFdXY3k0uVIb1XS/download",
            num_classes=20,
            pretrained_vit="base",
            method="gradient_rollout",
        )

        self.register_model(
            ResNetParts,
            dataset="pascal",
            weight_url="https://tu-dortmund.sciebo.de/s/7fAxd4RMPcg1drr/download",
            num_classes=194,
            model_name="resnet",
        )

    def register_model(
        self,
        model: Callable,
        dataset: str,
        weight_url: str = None,
        uid: str = None,
        model_name: str = None,
        **default_kwargs,
    ):
        """Register a model.

        Args:
            model (nn.Module): Model to register.
            dataset (str): Dataset the model was trained on.
            weight_url (str, optional): URL to download the model weights from.
                Defaults to None.
            uid (str, optional): Unique identifier for the model, e.g. for ViT: ViT_base_patch16_224.
            model_name (str, optional): Name of the model. Defaults to None.
            kwargs: Additional arguments that must be passed to the constructor.
        """
        name = model_name if model_name is not None else unify_string(model.__name__)
        _key = ModelKey(
            name,
            dataset,
            uid,
        )

        if _key in self._models:
            raise ValueError(f"Model {_key} already registered.")

        weights_file = self._model_dir / f"{_key}.pth"

        self._models[_key] = RegisteredModel(
            model_handle=model,
            weights_url=weight_url,
            weights_file=weights_file,
            _key=_key,
            defaults=default_kwargs,
        )

    def list_models(self):
        """List all registered models.

        Returns:
            list: List of registered models.
        """
        return list(self._models.keys())

    def update_models(self):
        """Update all registered models."""
        for model in self._models.values():
            model.download_weights()

    def delete_models(self):
        """Delete all local model weights."""
        for model in self._models.values():
            model.delete_local_weights()

    def get_model(
        self,
        model_name: str,
        dataset: str,
        device: torch.device,
        uid: str = None,
        **kwargs,
    ):
        """Get a registered model.

        Args:
            model_name (str): Name of the model.
            dataset (str): Dataset the model was trained on.
            device (torch.device): Device to use.
            uid (str, optional): Unique identifier for the model, e.g. for ViT: ViT_base_patch16_224.
            kwargs: Additional arguments to pass to the model constructor. These
                overwrite the default arguments.

        Raises:
            ValueError: If model is not registered.

        Returns:
            nn.Module: Model.
        """

        _key = ModelKey(model_name, dataset, uid)

        model = self._models.get(_key)

        if model is None:
            if uid is None:
                error_str = f"Model {model_name} is not registered for {dataset}."
            else:
                error_str = f"Model {model_name} with uid {uid} is not registered for {dataset}."
            raise ValueError(error_str)

        return model.initialize(device, **kwargs)

    def enable_caching(self):
        """Enable caching of models."""
        self._cache_models = True

    def disable_caching(self):
        """Disable caching of models."""
        self._cache_models = False
