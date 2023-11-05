from abc import abstractstaticmethod
from typing import List

from PIL import Image
import torch


class Dataset:
    @abstractstaticmethod
    def transform(img: Image.Image) -> torch.Tensor:
        raise NotImplementedError

    @abstractstaticmethod
    def inverse_transform(tensor: torch.Tensor) -> Image.Image:
        raise NotImplementedError

    @abstractstaticmethod
    def get_classes() -> List[str]:
        raise NotImplementedError

    @abstractstaticmethod
    def get_num_classes() -> int:
        raise NotImplementedError

    @abstractstaticmethod
    def class_index_to_name(idx: int) -> str:
        raise NotImplementedError
