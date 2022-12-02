import logging
import os


class LOG:

    def __init__(self, name=""):
        self._logger = logging.getLogger("main")
        self.log_format = "%(asctime)s - caller-%(name)s - %(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
        self.log_formatter = logging.Formatter(self.log_format)
        logging.basicConfig(format=self.log_format, level=logging.INFO)

        if name and name != "main":
            self._logger.name = f"main.{name}"
        self.log_dir = "logs"

    def configure_log_directory(self):
        os.makedirs(self.log_dir, exist_ok=True)

    @property
    def logger(self) -> logging.Logger:
        """Return the logger."""
        return self._logger

    def add_file_handler(self, test_name):
        _handler = logging.FileHandler(os.path.join(self.log_dir, f"{test_name}.log"))
        _handler.set_name(f"main.{test_name}")
        self._logger.info(f"handle created for {_handler.name}")
        _handler.setFormatter(self.log_formatter)
        _handler.setLevel(logging.DEBUG)
        _handler.addFilter(logging.Filter(name=f"main.{test_name}"))
        self._logger.addHandler(_handler)

    def info(self, msg):
        self._logger.info(msg)
