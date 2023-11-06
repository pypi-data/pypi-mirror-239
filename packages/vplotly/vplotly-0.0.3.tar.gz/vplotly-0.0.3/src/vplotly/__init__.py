"""A small Python package for plotting based on Plotly.
This package is accompanying the package `vstats`.
"""
from importlib.metadata import version

from vplotly._est_test_properties import (  # noqa: F401
    add_est_rejection_probabilities_to_figure,
    create_figure_for_rejection_probabilities)

# read version from installed package
__version__ = version("vplotly")

# To make autodoc document imported objects
# in package vplotly and not in some submodule
# of it, we follow the approach described in
# https://stackoverflow.com/a/66996523 :

imported_objects = [
    create_figure_for_rejection_probabilities,
    add_est_rejection_probabilities_to_figure
]

for o in imported_objects:
    o.__module__ = __name__

__all__ = [o.__name__ for o in imported_objects]
