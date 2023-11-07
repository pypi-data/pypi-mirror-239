from pathlib import Path
from math import pi
from autobi.core import takes, to_resolved_path_str


class TestWrappers:
    def test_path_stringified(self):
        original_path = Path()

        class Test:
            @takes(Path)
            def test_func(self, something: str) -> str:
                return something

        result = Test().test_func(original_path)
        assert str(original_path) == result
        assert isinstance(result, str)

    def test_path_resolved(self):
        original_path = Path()

        class Test:
            @takes(Path, converter=to_resolved_path_str)
            def test_func(self, something: str) -> str:
                return something

        result = Test().test_func(original_path)
        assert str(original_path.resolve()) == result
        assert isinstance(result, str)

    def test_float_formatted(self):
        class Test:
            @takes(float, converter=lambda x: f"{x:.2f}")
            def test_func(self, something: str) -> str:
                return something

        result = Test().test_func(pi)
        assert "3.14" == result
        assert isinstance(result, str)
