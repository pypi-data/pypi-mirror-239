import pytest
from pathlib import Path

from autobi import DatasetBuilder, ArgumentBuilder, FeaturenamesBuilder
from autobi.core import AutobiJVMHandler

from .datafiles import WAVFILE, GRIDFILE


class TestDatasetBuilder:
    def test_instantiable(self):
        with AutobiJVMHandler("test") as jvm:
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            DatasetBuilder(jvm, params.to_args_string())

    def test_instantiable_directly(self):
        with AutobiJVMHandler("test") as jvm:
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = params.build_dataset()
            assert isinstance(builder, DatasetBuilder)

    def test_default_features_addable(self):
        with AutobiJVMHandler("test") as jvm:
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            builder.with_default_features("PhraseAccentClassificationFeatureSet")

    def test_with_feature(self):
        with AutobiJVMHandler("test") as jvm:
            feature1 = r"cog[subregionC[delta[prodC[znormC[log[f0]],rnormC[I],0.1]],subregion[200ms]]]"
            feature2 = r"mean[subregionC[znormC[f0],subregion[200ms]]]"
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            builder.with_feature(feature1)
            builder.with_feature(feature2)

    def test_with_features(self):
        with AutobiJVMHandler("test") as jvm:
            feature1 = r"cog[subregionC[delta[prodC[znormC[log[f0]],rnormC[I],0.1]],subregion[200ms]]]"
            feature2 = r"mean[subregionC[znormC[f0],subregion[200ms]]]"
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            builder.with_features([feature1, feature2])

    def test_with_feature_set(self):
        with AutobiJVMHandler("test") as jvm:
            fnames = FeaturenamesBuilder(jvm)
            fnames.with_default_features("PhraseAccentClassificationFeatureSet")
            feature_set = fnames.build()
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            builder.with_feature_set(feature_set)

    def test_buildable(self):
        with AutobiJVMHandler("test") as jvm:
            feature = r"mean[subregionC[znormC[f0],subregion[200ms]]]"
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            builder.with_feature(feature)
            data_frame = builder.build_pandas()
            assert data_frame.columns.values == [feature.replace(",", "_")]

    def test_not_writable_after_build(self):
        with AutobiJVMHandler("test") as jvm:
            feature = r"mean[subregionC[znormC[f0],subregion[200ms]]]"
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            builder.with_feature(feature)
            _ = builder.build_pandas()
            with pytest.raises(ValueError):
                builder.with_feature(feature)

    def test_not_double_buildable(self):
        with AutobiJVMHandler("test") as jvm:
            feature = r"mean[subregionC[znormC[f0],subregion[200ms]]]"
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            builder.with_feature(feature)
            _ = builder.build_pandas()
            with pytest.raises(ValueError):
                builder.write_csv(Path() / "out.csv")

    def test_feature_errors_propogated_properly(self):
        with AutobiJVMHandler("test") as jvm:
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            with pytest.raises(ValueError):
                builder.with_feature("jkfjdklsjkl")

    def test_features_errors_propogated_properly(self):
        with AutobiJVMHandler("test") as jvm:
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            with pytest.raises(ValueError):
                builder.with_features(
                    ["jkfjdklsjkl", r"mean[subregionC[znormC[f0],subregion[200ms]]]"]
                )

    def test_default_feature_errors_propogated_properly(self):
        with AutobiJVMHandler("test") as jvm:
            params = ArgumentBuilder(jvm)
            params.with_input_wav(WAVFILE)
            params.with_input_TextGrid(GRIDFILE)
            builder = DatasetBuilder(jvm, params.to_args_string())
            with pytest.raises(ValueError):
                builder.with_default_features("jkfjdklsjkl")
