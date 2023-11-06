from autobi.core import AutobiJVMHandler
from autobi import RunDefault


class TestRunDefault:
    def test_runs_at_all(self):
        with AutobiJVMHandler("test") as jvm:
            RunDefault(jvm).run("")
