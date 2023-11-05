from explainer.datasets.base import Dataset as DatasetBase


class DatasetHandler:
    def __init__(self):
        self._datasets = {}
        self._register_default_datasets()

    def _register_default_datasets(self):
        from .pascal import Pascal, PascalParts

        self.register_dataset(Pascal, dataset_name="pascal", model_type="object_model")
        self.register_dataset(
            PascalParts, dataset_name="pascal", model_type="parts_model"
        )

    def register_dataset(
        self, dataset: DatasetBase, dataset_name: str, model_type: str
    ):
        assert isinstance(
            dataset_name, str
        ), f"dataset_name must be of type str, but is {type(dataset_name)}"

        k = (dataset_name, model_type)

        if k in self._datasets:
            raise ValueError(f"Dataset {k} already registered.")

        self._datasets[k] = dataset

    def get_dataset(self, dataset_name: str, model_type: str):
        return self._datasets[(dataset_name, model_type)]
