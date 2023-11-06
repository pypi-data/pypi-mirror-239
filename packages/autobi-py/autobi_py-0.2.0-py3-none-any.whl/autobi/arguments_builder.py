from __future__ import annotations

from autobi.core import (
    AutobiJVM,
    takes,
    to_resolved_path_str,
    to_java_bool,
    to_java_float,
)
from .dataset_builder import DatasetBuilder
from pathlib import Path


class ArgumentBuilder:
    def __init__(self, jvm: AutobiJVM):
        self._jvm = jvm
        self._object = jvm._jvm.edu.leidenuniv.AuToBIAdapter.AuToBIArgumentsBuilder()

    @takes(Path, converter=to_resolved_path_str)
    def with_input_TextGrid(self, textgrid: str) -> ArgumentBuilder:
        self._object.withInputTextGrid(textgrid)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_input_wav(self, wav: str) -> ArgumentBuilder:
        self._object.withInputWav(wav)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_output_file(self, outfile: str) -> ArgumentBuilder:
        self._object.withOutputFile(outfile)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_output_arff_file(self, output_arff_file: str) -> ArgumentBuilder:
        self._object.withOutputArffFile(output_arff_file)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_pitch_accent_detector(self, detector: str) -> ArgumentBuilder:
        self._object.withPitchAccentDetector(detector)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_pitch_accent_classifier(self, classifier: str) -> ArgumentBuilder:
        self._object.withPitchAccentClassifier(classifier)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_intonal_phrase_boundary_detector(self, detector: str) -> ArgumentBuilder:
        self._object.withIntonalPhraseBoundaryDetector(detector)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_intermediate_phrase_boundary_detector(
        self, detector: str
    ) -> ArgumentBuilder:
        self._object.withIntermediatePhraseBoundaryDetector(detector)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_boundary_tone_classifier(self, classifier: str) -> ArgumentBuilder:
        self._object.withBoundaryToneClassifier(classifier)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_phrase_accent_classifier(self, classifier: str) -> ArgumentBuilder:
        self._object.withPhraseAccentClassifier(classifier)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_log4j_configfile(self, configfile: str) -> ArgumentBuilder:
        self._object.withLog4jConfigFile(configfile)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_cprom_file(self, configfile: str) -> ArgumentBuilder:
        self._object.withCpromFile(configfile)
        return self

    @takes(Path, converter=to_resolved_path_str)
    def with_rhapsodie_file(self, configfile: str) -> ArgumentBuilder:
        self._object.withRhapsodieFile(configfile)
        return self

    def with_silence_regex(self, name: str) -> ArgumentBuilder:
        self._object.withSilenceRegex(name)
        return self

    def with_words_tiername(self, name: str) -> ArgumentBuilder:
        self._object.withWordsTierName(name)
        return self

    def with_breaks_tiername(self, name: str) -> ArgumentBuilder:
        self._object.withBreaksTierName(name)
        return self

    def with_charset(self, new_charset: str) -> ArgumentBuilder:
        self._object.withCharset(new_charset)
        return self

    def with_end_idx(self, idx: str) -> ArgumentBuilder:
        self._object.withEndIDX(idx)
        return self

    def with_ortho_idx(self, idx: str) -> ArgumentBuilder:
        self._object.withOrthoIDX(idx)
        return self

    def with_start_idx(self, idx: str) -> ArgumentBuilder:
        self._object.withStartIDX(idx)
        return self

    @takes(float, converter=to_java_float)
    def with_silence_threshold(self, threshold: str) -> ArgumentBuilder:
        self._object.withSilenceThreshold(threshold)
        return self

    @takes(bool, converter=to_java_bool)
    def with_distributions(self, distributions: str) -> ArgumentBuilder:
        self._object.withDistributions(distributions)
        return self

    def to_args_string(self) -> str:
        return str(self._object.toArgsString())

    def build_dataset(self) -> DatasetBuilder:
        return DatasetBuilder(self._jvm, self.to_args_string())
