"""Даты без зависимости от длины текущего месяца."""
from datetime import date


def shifted_month(value: date, offset: int) -> date:
    """Первый день месяца со сдвигом, включая переход года."""
    index = value.year * 12 + value.month - 1 + offset
    year, month = divmod(index, 12)
    return date(year, month + 1, 1)


def normalize_date(value: str) -> date:
    """Преобразовать ISO-дату в значение для сравнения."""
    return date.fromisoformat(value.strip())
