import threading

import os

from pathlib import Path


class ThreadMagic(type):

    _instances = {}

    global_lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            with self.global_lock:
                if self not in self._instances:
                    self._instances[self] = super(ThreadMagic, self).__call__(
                        *args, **kwargs
                    )
        return self._instances[self]


class FlaskAppConfig(metaclass=ThreadMagic):

    @property
    def STATIC_WEBROOT(self):
        webroot = Path() / "webroot"
        return f"{webroot.absolute()}"

    @property
    def DEBUG(self):
        return os.environ.get("DEBUG", "0")

    @property
    def FLASK_ENV(self):
        return os.environ.get("FLASK_ENV")

    def get_flask_kwargs(self, name: str):
        flask_kwargs = dict(
            import_name=name,
            static_url_path="",
            static_folder=self.STATIC_WEBROOT,
        )
        # print("nice args", flask_kwargs)
        return flask_kwargs
