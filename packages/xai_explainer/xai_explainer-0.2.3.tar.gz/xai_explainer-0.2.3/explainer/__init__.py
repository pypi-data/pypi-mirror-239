"""
Explainer is a Python package for explaining the predictions of machine learning models.
"""

from .main import Explainer  # relative import in __init__.py
from .util.return_types import Object, Part, Result  # relative import in __init__.py

__all__ = [
    "Explainer",
    "Object",
    "Part",
    "Result",
]
