import pytest
from autobi.core import AutobiJVMHandler
from autobi import FeaturenamesBuilder, FeatureSet


class TestFeaturenamesBuilder:
    def test_with_default_features(self):
        with AutobiJVMHandler("test") as jvm:
            builder = FeaturenamesBuilder(jvm)
            builder.with_default_features("PhraseAccentClassificationFeatureSet")
            strings = builder.build_strings()
            assert strings
            assert all(isinstance(item, str) for item in strings)

    def test_with_feature(self):
        with AutobiJVMHandler("test") as jvm:
            feature1 = r"cog[subregionC[delta[prodC[znormC[log[f0]],rnormC[I],0.1]],subregion[200ms]]]"
            feature2 = r"mean[subregionC[znormC[f0],subregion[200ms]]]"
            builder = FeaturenamesBuilder(jvm)
            builder.with_feature(feature1)
            builder.with_feature(feature2)
            strings = builder.build_strings()
            assert len(strings) == 2
            assert feature1 in strings
            assert feature2 in strings

    def test_with_features(self):
        with AutobiJVMHandler("test") as jvm:
            feature1 = r"cog[subregionC[delta[prodC[znormC[log[f0]],rnormC[I],0.1]],subregion[200ms]]]"
            feature2 = r"mean[subregionC[znormC[f0],subregion[200ms]]]"
            builder = FeaturenamesBuilder(jvm)
            builder.with_features([feature1, feature2])
            strings = builder.build_strings()
            assert len(strings) == 2
            assert feature1 in strings
            assert feature2 in strings

    def test_featureset(self):
        with AutobiJVMHandler("test") as jvm:
            feature1 = r"cog[subregionC[delta[prodC[znormC[log[f0]],rnormC[I],0.1]],subregion[200ms]]]"
            feature2 = r"mean[subregionC[znormC[f0],subregion[200ms]]]"
            builder = FeaturenamesBuilder(jvm)
            builder.with_features([feature1, feature2])
            feature_set = builder.build()
            assert isinstance(feature_set, FeatureSet)
            strings = feature_set._strings
            assert len(strings) == 2
            assert feature1 in strings
            assert feature2 in strings

    def test_feature_errors_propogated_properly(self):
        with AutobiJVMHandler("test") as jvm:
            builder = FeaturenamesBuilder(jvm)
            with pytest.raises(ValueError):
                builder.with_feature("jkfjdklsjkl")

    def test_features_errors_propogated_properly(self):
        with AutobiJVMHandler("test") as jvm:
            builder = FeaturenamesBuilder(jvm)
            with pytest.raises(ValueError):
                builder.with_features(
                    ["jkfjdklsjkl", r"mean[subregionC[znormC[f0],subregion[200ms]]]"]
                )

    def test_default_feature_errors_propogated_properly(self):
        with AutobiJVMHandler("test") as jvm:
            builder = FeaturenamesBuilder(jvm)
            with pytest.raises(ValueError):
                builder.with_default_features("jkfjdklsjkl")
