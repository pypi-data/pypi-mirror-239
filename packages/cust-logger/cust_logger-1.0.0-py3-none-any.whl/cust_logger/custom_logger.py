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
        args_separator: str = " | ",
        tag_separator: str = " - "
    ):
        logging_level = logging.getLevelName(logging_level.upper())
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        logs_path = os.path.join(logs_dir, f"{name}.log")
        self._args_separator = args_separator
        self._tag_separator = tag_separator

        handler = RotatingFileHandler(logs_path, maxBytes=max_MB * 1024 * 1024, backupCount=max_count)
        # handler = logging.FileHandler(f"{NAME}.log", mode="w")
        formatter = logging.Formatter(format_string, datefmt='%d-%m-%Y %H:%M:%S')

        handler.setFormatter(formatter)
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging_level)
        self._logger.addHandler(handler)

    def debug(self, *args, tag: Union[str, int] = None) -> None:
        self._log(self._logger.debug, *args, tag=tag)

    def info(self, *args, tag: Union[str, int] = None) -> None:
        self._log(self._logger.info, *args, tag=tag)

    def warning(self, *args, tag: Union[str, int] = None) -> None:
        self._log(self._logger.warning, *args, tag=tag)

    def error(self, *args, tag: Union[str, int] = None) -> None:
        self._log(self._logger.error, *args, tag=tag)

    def critical(self, *args, tag: Union[str, int] = None) -> None:
        self._log(self._logger.critical, *args, tag=tag)

    def _log(self, level_func: Callable, *args, tag: Union[str, int] = None) -> None:
        message = self._args_separator.join(map(str, args))
        if str(tag):
            message = str(tag) + self._tag_separator + message
        level_func(message)

