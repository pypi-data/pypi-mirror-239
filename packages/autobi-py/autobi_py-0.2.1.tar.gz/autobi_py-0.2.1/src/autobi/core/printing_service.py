import threading

from queue import Queue
from typing import Callable

PRINTING_QUEUE = Queue()


def py4j_print(item: str) -> None:
    items = item.strip("\n").split("\n")
    items = [f"PY4J | {line}" for line in items]
    print("\n".join(items))


class PrintingService(threading.Thread):
    """Deamon thread service to print (or otherwise process) items in the Printing queue.
    Process can be started or stopped with start() and stop()"""

    def __init__(self, printer: Callable[[str], None]):
        super(PrintingService, self).__init__(
            target=self._run_service,
            daemon=True,
            name=f"PY4J printer ({printer.__name__})",
        )
        self._stop_event = threading.Event()
        self._printer = printer

    def start(self):
        self._stop_event.clear()
        super(PrintingService, self).start()

    def stop(self):
        PRINTING_QUEUE.join()
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def _run_service(self):
        while not self.is_stopped():
            item = PRINTING_QUEUE.get()
            self._printer(item)
            PRINTING_QUEUE.task_done()
