"""Позитивные проверки календаря без отправки формы."""
import allure
import pytest
from pages.calendar_page import CalendarPage
from utils.data_generator import normalize_date, shifted_month

pytestmark = [pytest.mark.calendar, pytest.mark.positive, allure.feature('Calendar'),
              allure.story('Выбор даты'), allure.severity(allure.severity_level.NORMAL)]


@allure.title('Страница календаря загружается и поле доступно')
def test_calendar_page_loads(calendar_page: CalendarPage) -> None:
    assert calendar_page.heading() == 'Calendars'
    assert calendar_page.wait_clickable(calendar_page.FIELD).is_displayed()


@allure.title('Клик по полю открывает календарь')
def test_datepicker_opens(calendar_page: CalendarPage) -> None:
    assert calendar_page.is_hidden(calendar_page.picker.ROOT)
    calendar_page.click(calendar_page.FIELD)
    assert calendar_page.wait_visible(calendar_page.picker.ROOT).is_displayed()


@allure.title('Выбор даты текущего месяца')
def test_select_current_month(calendar_page: CalendarPage) -> None:
    today = calendar_page.picker.today()
    calendar_page.picker.select_day(15)
    assert normalize_date(calendar_page.value()) == today.replace(day=15)


@allure.title('Выбор даты следующего месяца')
def test_select_next_month(calendar_page: CalendarPage) -> None:
    expected = shifted_month(calendar_page.picker.today(), 1)
    calendar_page.picker.move_month(1)
    calendar_page.picker.select_day(1)
    assert normalize_date(calendar_page.value()) == expected


@allure.title('Выбор даты предыдущего месяца')
def test_select_previous_month(calendar_page: CalendarPage) -> None:
    expected = shifted_month(calendar_page.picker.today(), -1)
    calendar_page.picker.move_month(-1)
    calendar_page.picker.select_day(1)
    assert normalize_date(calendar_page.value()) == expected


@allure.title('Выбор сегодняшней даты в сетке календаря')
def test_select_today(calendar_page: CalendarPage) -> None:
    expected = calendar_page.picker.today()
    calendar_page.picker.open()
    calendar_page.click(calendar_page.picker.TODAY)
    assert normalize_date(calendar_page.value()) == expected


@allure.title('Ручной ввод корректной високосной даты')
def test_manual_leap_date(calendar_page: CalendarPage) -> None:
    calendar_page.enter_date('2024-02-29')
    calendar_page.wait_validation(False)
    assert calendar_page.value() == '2024-02-29'


@allure.title('Очистка даты и повторный выбор')
def test_clear_and_reselect(calendar_page: CalendarPage) -> None:
    calendar_page.enter_date('2024-02-29')
    calendar_page.enter_date('')
    assert calendar_page.value() == ''
    expected = calendar_page.picker.today().replace(day=1)
    calendar_page.picker.select_day(1)
    assert normalize_date(calendar_page.value()) == expected


@allure.title('После выбора календарь закрывается, а значение сохраняется')
def test_selection_closes_picker(calendar_page: CalendarPage) -> None:
    expected = calendar_page.picker.today().replace(day=10)
    calendar_page.picker.select_day(10)
    assert calendar_page.wait_invisible(calendar_page.picker.ROOT)
    assert normalize_date(calendar_page.value()) == expected
    calendar_page.picker.open()
    assert normalize_date(calendar_page.value()) == expected


@allure.title('Переход из декабря в январь и обратно сохраняет правильный год')
def test_year_boundary_navigation(calendar_page: CalendarPage) -> None:
    today = calendar_page.picker.today()
    calendar_page.picker.move_month(12 - today.month)
    calendar_page.picker.move_month(1)
    calendar_page.picker.select_day(1)
    with allure.step('Проверить 1 января следующего года'):
        assert normalize_date(calendar_page.value()) == today.replace(year=today.year + 1, month=1, day=1)
    calendar_page.picker.move_month(-1)
    calendar_page.picker.select_day(1)
    with allure.step('Проверить возврат к 1 декабря исходного года'):
        assert normalize_date(calendar_page.value()) == today.replace(month=12, day=1)
