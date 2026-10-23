"""Логирование средствами стандартной библиотеки и pytest."""
import logging


def get_logger(name: str) -> logging.Logger:
    """Вернуть логгер без дублирующих обработчиков."""
    return logging.getLogger(name)
