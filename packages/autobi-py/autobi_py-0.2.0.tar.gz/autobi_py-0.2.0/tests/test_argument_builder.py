import pytest

from autobi.core import AutobiJVMHandler
from autobi import ArgumentBuilder, RunDefault

from pathlib import Path


# The order is not guaranteed, so we only just test a few on their own
# and hope the rest works, too
class TestArgsBuilderStrings:
    def test_args_output(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = builder.with_output_file(Path()).to_args_string()
            assert args == f"-out_file={str(Path().resolve())}"

    def test_args_wav(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = builder.with_input_wav(Path()).to_args_string()
            assert args == f"-wav_file={str(Path().resolve())}"

    def test_args_textgrid(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = builder.with_input_TextGrid(Path()).to_args_string()
            assert args == f"-input_file={str(Path().resolve())}"

    def test_args_charset(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = builder.with_charset("hello").to_args_string()
            assert args == f"-charset=hello"


class TestArgsBuilderRuns:
    def test_args_output_run(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = builder.with_output_file(Path()).to_args_string()
            RunDefault(jvm).run(args)

    def test_args_wav_run(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = builder.with_input_wav(Path()).to_args_string()
            RunDefault(jvm).run(args)

    def test_args_textgrid_run(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = builder.with_input_TextGrid(Path()).to_args_string()
            RunDefault(jvm).run(args)

    def test_args_charset_run(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = builder.with_charset("hello").to_args_string()
            RunDefault(jvm).run(args)

    def test_args_combined_run(self):
        with AutobiJVMHandler("test") as jvm:
            builder = ArgumentBuilder(jvm)
            args = (
                builder.with_output_file(Path())
                .with_input_wav(Path())
                .with_input_TextGrid(Path())
                .with_charset("hello")
                .to_args_string()
            )
            RunDefault(jvm).run(args)
