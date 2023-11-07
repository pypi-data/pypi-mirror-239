from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

import pandas as pd
from py4j.java_gateway import Py4JJavaError

from autobi.core import AutobiJVM, takes, to_resolved_path_str
from .featurenames_builder import FeatureSet


class DatasetBuilder:
    def __init__(self, jvm: AutobiJVM, params: str):
        try:
            self._jvm = jvm
            self._object = jvm._jvm.edu.leidenuniv.AuToBIAdapter.DataSetBuilder(params)
            self._written = False
        except Py4JJavaError:
            raise ValueError("Cannot read arguments. Could not parse Textgrid or Wav.")

    def _assert_not_written(self) -> None:
        if self._written:
            raise ValueError("Cannot add features or build again after writing")

    def with_default_features(self, name: str) -> DatasetBuilder:
        self._assert_not_written()
        try:
            self._object.withDefaultFeatures(name)
        except Py4JJavaError:
            raise ValueError(f"Cannot add feature {name}, not found")
        return self

    def with_feature(self, name: str) -> DatasetBuilder:
        self._assert_not_written()
        try:
            self._object.withFeature(name)
        except Py4JJavaError:
            raise ValueError(f"Cannot add feature {name}, not found")
        return self

    def with_features(self, names: List[str]) -> DatasetBuilder:
        self._assert_not_written()
        try:
            self._object.withFeatures(json.dumps(names))
        except Py4JJavaError:
            raise ValueError(f"Cannot add features {names}, not found")
        return self

    def with_feature_set(self, features: FeatureSet):
        self._assert_not_written()
        self.with_features(features._strings)

    @takes(Path, converter=to_resolved_path_str)
    def write_csv(self, filename: str):
        self._assert_not_written()
        self._written = True
        self._object.writeCSV(filename)

    @takes(Path, converter=to_resolved_path_str)
    def write_arff(self, filename: str):
        self._assert_not_written()
        self._written = True
        self._object.writeARFF(filename)

    @takes(Path, converter=to_resolved_path_str)
    def write_liblinear(self, filename: str):
        self._assert_not_written()
        self._written = True
        self._object.writeLibLinear(filename)

    def build_pandas(self) -> pd.DataFrame:
        with TemporaryDirectory() as temp_dir:
            tempfile = Path(temp_dir) / "out.csv"
            self.write_csv(tempfile)
            return pd.read_csv(tempfile, delimiter=",", na_values=["?"]).astype(float)
