import logging
import os
import inspect


class LOG:

    def __init__(self, name="", level="INFO"):
        """Initiate LOGGER.

        Args:
            name: caller
            level: Log level
        """
        self.root_logger = "ci"
        self._logger = logging.getLogger(self.root_logger)
        self.log_format = "%(asctime)s - %(levelname)s - caller-%(name)s - %(message)s"
        self.log_formatter = logging.Formatter(self.log_format)
        logging.basicConfig(format=self.log_format, level=getattr(logging, level))

        if name and name != self.root_logger:
            self._logger.name = self.logger_name(name)
        self.log_dir = "logs"

    def logger_name(self, mod):
        return f"{self.root_logger}.{mod}"

    # def set_logger_name(self, logger, name):
    #     logger._logger = name

    def configure_log_directory(self):
        os.makedirs(self.log_dir, exist_ok=True)

    @property
    def logger(self) -> logging.Logger:
        """Return the logger."""
        return self._logger

    def add_file_handler(self, test_name):
        """Add file handler

        Args:
            test_name: name of the test module
        """
        _handler = logging.FileHandler(os.path.join(self.log_dir, f"{test_name}.log"))
        _handler.set_name(self.logger_name(test_name))
        self.info(f"Created handler for {_handler.name}")
        _handler.setFormatter(self.log_formatter)
        _handler.setLevel(logging.DEBUG)
        _handler.addFilter(logging.Filter(name=self.logger_name(test_name)))
        self._logger.addHandler(_handler)

    def remove_file_handler(self, name):
        """Remove file handler."""
        for _handler in self._logger.handlers:
            if _handler.name == self.logger_name(name):
                self._logger.removeHandler(_handler)
                self.info(f"Removed handler {name} successfully..")

    def _log(self, level: str, message, *args, **kwargs) -> None:
        """
        Log the given message using the provided level along with the metadata.
        updating LOG_FORMAT with filename:line_number - message
        ex: 2022-11-15 11:37:00,346 - DEBUG - cephci.utility.log.py:227 - Completed log configuration

        *Args:
            level (str):        Log level
            message (Any):      The message that needs to be logged
        **kwargs:
            metadata (dict):    Extra information to be appended to logstash

        Returns:
            None.
        """
        log = {
            "info": self._logger.info,
            "debug": self._logger.debug,
            "warning": self._logger.warning,
            "error": self._logger.error,
            "exception": self._logger.exception,
        }
        extra = {}
        extra.update(kwargs.get("metadata", {}))
        calling_frame = inspect.stack()[2].frame
        trace = inspect.getframeinfo(calling_frame)
        file_path = trace.filename.split("/")
        files = file_path if len(file_path) == 1 else file_path[5:]
        extra.update({"LINENUM": trace.lineno, "FILENAME": ".".join(files)})
        log[level](
            f"{extra['FILENAME']}:{extra['LINENUM']} - {message}",
            *args,
            extra={},
            **kwargs,
        )

    def info(self, message, *args, **kwargs) -> None:
        """Log with info level the provided message and extra data.

        Args:
            message (Any):  The message to be logged.
            args (Any):     Dynamic list of supported arguments.
            kwargs (Any):   Dynamic list of supported keyword arguments.

        Returns:
            None
        """
        self._log("info", message, *args, **kwargs)

    def debug(self, message, *args, **kwargs) -> None:
        """Log with debug level the provided message and extra data.

        Args:
            message (str):  The message to be logged.
            args (Any):     Dynamic list of supported arguments.
            kwargs (Any):   Dynamic list of supported keyword arguments.

        Returns:
            None
        """
        self._log("debug", message, *args, **kwargs)

    def warning(self, message, *args, **kwargs) -> None:
        """Log with warning level the provided message and extra data.

        Args:
            message (Any):  The message to be logged.
            args (Any):     Dynamic list of supported arguments.
            kwargs (Any):   Dynamic list of supported keyword arguments.

        Returns:
            None
        """
        self._log("warning", message, *args, **kwargs)

    def error(self, message, *args, **kwargs) -> None:
        """Log with error level the provided message and extra data.

        Args:
            message (Any):  The message to be logged.
            args (Any):     Dynamic list of supported arguments.
            kwargs (Any):   Dynamic list of supported keyword arguments.

        Returns:
            None
        """
        self._log("error", message, *args, **kwargs)

    def exception(self, message, *args, **kwargs) -> None:
        """Log the given message under exception log level.

        Args:
            message (Any):  Message or record to be emitted.
            args (Any):     Dynamic list of supported arguments.
            kwargs (Any):   Dynamic list of supported keyword arguments.
        Returns:
            None
        """
        kwargs["exc_info"] = kwargs.get("exc_info", True)
        self._log("exception", message, *args, **kwargs)
