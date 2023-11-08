from __future__ import annotations

from logging import getLogger, INFO, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger


def create_logger(log_path: Path | str, filename: str) -> Logger:
    filename = Path(filename).stem  # NOTE: if filename == __file__ => some_main.py -> some_main
    if isinstance(log_path, str):
        log_path = Path(log_path)

    logger = getLogger()
    logger.setLevel(INFO)
    if not log_path.exists():
        log_path.mkdir()

    file_name = log_path / f"{filename}.log"

    formatter = Formatter("%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s")
    rotating_handler = RotatingFileHandler(file_name, maxBytes=1024 * 1024 * 100, backupCount=10, encoding="utf-8")
    rotating_handler.setFormatter(formatter)

    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(rotating_handler)

    return logger
