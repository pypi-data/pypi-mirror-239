from logging.handlers import RotatingFileHandler
from typing import Callable, Union
import logging
import os.path


class CustomLogger:
    def __init__(
        self,
        name: str,
        logging_level: str = "DEBUG",
        logs_dir: str = "logs",
        max_MB: int = 5,
        max_count: int = 10,
        format_string: str = "%(asctime)s.%(msecs)03d [%(levelname)s] (%(module)s.%(funcName)s:%(lineno)d) - %(message)s",
        args_separator: str = " | "
    ):
        logging_level = logging.getLevelName(logging_level.upper())
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        logs_path = os.path.join(logs_dir, f"{name}.log")
        self._args_separator = args_separator

        handler = RotatingFileHandler(logs_path, maxBytes=max_MB * 1024 * 1024, backupCount=max_count)
        # handler = logging.FileHandler(f"{NAME}.log", mode="w")
        formatter = logging.Formatter(format_string, datefmt='%d-%m-%Y %H:%M:%S')

        handler.setFormatter(formatter)
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging_level)
        self._logger.addHandler(handler)

    def debug(self, message: str, *args, tag: Union[str, int] = "") -> None:
        self._log(self._logger.debug, message, *args, tag=tag)

    def info(self, message: str, *args, tag: Union[str, int] = "") -> None:
        self._log(self._logger.info, message, *args, tag=tag)

    def warning(self, message: str, *args, tag: Union[str, int] = "") -> None:
        self._log(self._logger.warning, message, *args, tag=tag)

    def error(self, message: str, *args, tag: Union[str, int] = "") -> None:
        self._log(self._logger.error, message, *args, tag=tag)

    def critical(self, message: str, *args, tag: Union[str, int] = "") -> None:
        self._log(self._logger.critical, message, *args, tag=tag)

    def _log(self, level_func: Callable, message: str, *args, tag: Union[str, int] = "") -> None:
        try:
            if args:
                message += self._args_separator + self._args_separator.join(map(str, args))
            if str(tag):
                message = str(tag) + self._args_separator + message
        except Exception as _e:
            self._logger.warning(_e)
        level_func(message)

