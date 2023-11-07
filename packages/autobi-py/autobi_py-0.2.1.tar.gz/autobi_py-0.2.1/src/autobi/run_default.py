from autobi.core import AutobiJVM


class RunDefault:
    def __init__(self, jvm: AutobiJVM):
        self._jvm = jvm
        self._object = jvm._jvm.edu.leidenuniv.AuToBIAdapter.RunDefault()

    def run(self, args: str):
        self._object.run(args)
