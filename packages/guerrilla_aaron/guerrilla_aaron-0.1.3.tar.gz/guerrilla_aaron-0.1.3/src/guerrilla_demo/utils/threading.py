import threading
from threading import Thread


class ThreadWithResult(threading.Thread):
    """Extension of threading.Thread, with a `join` method which returns the thread's return value."""

    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs={},
                 *,
                 daemon=None):

        def function():
            self.result = target(*args, **kwargs)

        super().__init__(group=group, target=function, name=name, daemon=daemon)
