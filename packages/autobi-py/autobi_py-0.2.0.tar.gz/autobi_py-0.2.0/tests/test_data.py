from __future__ import annotations

from pathlib import Path

from py4j.java_gateway import JavaGateway

from autobi._jar import JARPATH


class TestJar:
    def test_jar_includes(self):
        assert isinstance(JARPATH, Path)
        assert JARPATH.exists()
        assert JARPATH.is_file()
        assert JARPATH.suffix == ".jar"
        assert JARPATH.is_absolute()
        assert not JARPATH.is_reserved()

    def test_jar_loadable_autobi(self):
        gg = JavaGateway.launch_gateway(classpath=str(JARPATH))
        autobi = gg.jvm.edu.cuny.qc.speech.AuToBI.AuToBI()
        assert "toString" in dir(autobi)

    def test_jar_loadable_adapter(self):
        gg = JavaGateway.launch_gateway(classpath=str(JARPATH))
        run_default = gg.jvm.edu.leidenuniv.AuToBIAdapter.RunDefault()
        assert "run" in dir(run_default)
