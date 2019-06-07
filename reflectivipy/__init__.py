"""
Reflectivity implementation for Python base package
"""
from .reflectivity import (
    link,
    reflective_ast_for_method,
    reflective_method_for,
    uninstall_all,
    metalinks,
    rf_methods,
)
from .core import MetaLink, ReflectiveMethod

__version__ = "0.1.1"

__all__ = [
    "link",
    "reflective_ast_for_method",
    "reflective_method_for",
    "uninstall_all",
    "metalinks",
    "rf_methods",
    "MetaLink",
    "ReflectiveMethod",
]
