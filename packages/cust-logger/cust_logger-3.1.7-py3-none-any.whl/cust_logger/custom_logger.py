from logging.handlers import RotatingFileHandler
from typing import Callable
import logging
import os.path
import re


class CustomLogger:
    def __init__(
        self,
        name: str,
        logging_level: str = "DEBUG",
        logs_dir: str = "logs",
        max_MB: int = 5,
        max_count: int = 10,
        format_string: str = "%(asctime)s.%(msecs)03d [%(levelname)s] (%(module)s.%(funcName)s:%(lineno)d) %(message)s",
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

    def debug(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.debug, message, **kwargs)

    def info(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.info, message, **kwargs)

    def warning(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.warning, message, **kwargs)

    def error(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.error, message, **kwargs)

    def critical(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.critical, message, **kwargs)

    @staticmethod
    def _log(level_func: Callable, message: any, **kwargs) -> None:
        message = "- " + str(message) if not (message is None) else ""
        if kwargs:
            dict_string = re.sub(r"'(\w+)':", r"\1:", str(kwargs))
            message = f"{dict_string} {message}"
        level_func(message)
