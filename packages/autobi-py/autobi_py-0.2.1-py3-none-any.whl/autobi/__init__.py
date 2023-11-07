"""
Python bindings for AuToBI: an Automatic prosodic annotation tool written in Java.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:license: APACHE 2.0, see LICENSE for more details.
"""

__title__ = "AuToBI-py"
__author__ = "JJWRoeloffs"
__license__ = "APACHE"
__version__ = "0.2.1"


import autobi.core as core
from autobi.run_default import RunDefault
from autobi.arguments_builder import ArgumentBuilder
from autobi.featurenames_builder import FeaturenamesBuilder, FeatureSet
from autobi.dataset_builder import DatasetBuilder

__all__ = (
    "core",
    "RunDefault",
    "ArgumentBuilder",
    "FeaturenamesBuilder",
    "FeatureSet",
    "DatasetBuilder",
)
