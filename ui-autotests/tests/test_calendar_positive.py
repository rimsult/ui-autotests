"""Позитивные проверки календаря без отправки формы."""
import allure
import pytest
from utils.data_generator import normalize_date, shifted_month

pytestmark = [pytest.mark.calendar, pytest.mark.positive, allure.feature('Calendar'),
              allure.story('Выбор даты'), allure.severity(allure.severity_level.NORMAL)]


@allure.title('Страница календаря загружается и поле доступно')
def test_calendar_page_loads(calendar_page):
    assert calendar_page.heading() == 'Calendars'
    assert calendar_page.wait_clickable(calendar_page.FIELD).is_displayed()


@allure.title('Клик по полю открывает календарь')
def test_datepicker_opens(calendar_page):
    calendar_page.picker.open()
    assert calendar_page.is_visible(calendar_page.picker.ROOT)


@allure.title('Выбор даты текущего месяца')
def test_select_current_month(calendar_page):
    today = calendar_page.picker.today()
    calendar_page.picker.select_day(15)
    assert normalize_date(calendar_page.value()) == today.replace(day=15)


@allure.title('Выбор даты следующего месяца, включая смену года')
def test_select_next_month(calendar_page):
    expected = shifted_month(calendar_page.picker.today(), 1)
    calendar_page.picker.move_month(1)
    calendar_page.picker.select_day(1)
    assert normalize_date(calendar_page.value()) == expected


@allure.title('Выбор даты предыдущего месяца, включая смену года')
def test_select_previous_month(calendar_page):
    expected = shifted_month(calendar_page.picker.today(), -1)
    calendar_page.picker.move_month(-1)
    calendar_page.picker.select_day(1)
    assert normalize_date(calendar_page.value()) == expected


@allure.title('Выбор сегодняшней даты в сетке календаря')
def test_select_today(calendar_page):
    expected = calendar_page.picker.today()
    calendar_page.picker.open()
    calendar_page.click(calendar_page.picker.TODAY)
    assert normalize_date(calendar_page.value()) == expected


@allure.title('Ручной ввод корректной високосной даты')
def test_manual_leap_date(calendar_page):
    calendar_page.enter_date('2024-02-29')
    calendar_page.wait_validation(False)
    assert calendar_page.value() == '2024-02-29'


@allure.title('Очистка даты и повторный выбор')
def test_clear_and_reselect(calendar_page):
    calendar_page.enter_date('2024-02-29')
    calendar_page.enter_date('')
    assert calendar_page.value() == ''
    expected = calendar_page.picker.today().replace(day=1)
    calendar_page.picker.select_day(1)
    assert normalize_date(calendar_page.value()) == expected


@allure.title('После выбора календарь закрывается, а значение сохраняется')
def test_selection_closes_picker(calendar_page):
    calendar_page.picker.select_day(10)
    assert calendar_page.wait_invisible(calendar_page.picker.ROOT)
    value = calendar_page.value()
    calendar_page.picker.open()
    assert calendar_page.value() == value
