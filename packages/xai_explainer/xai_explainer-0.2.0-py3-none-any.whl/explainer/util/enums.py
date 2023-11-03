import enum


class ModelType(enum.Enum):
    object_model = 0
    parts_model = 1


class ObjectModel(enum.Enum):
    cam = 0
    vit = 1
    prm = 2


class PartsModel(enum.Enum):
    resnet = 0


class SegmentationMethod(enum.Enum):
    default = 0
    grabcut = 1


class Dataset(enum.Enum):
    pascal = 0
