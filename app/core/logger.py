import logging
import sys
from typing import Optional


def setup_logger(level: str = "INFO") -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="""
{
  "time": "%(asctime)s",
  "level": "%(levelname)s",
  "name": "%(name)s",
  "message": "%(message)s"
}
""".strip()
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name)
