"""Ошибки ввода проверяются по состоянию настоящего поля."""
import allure
import pytest

pytestmark = [pytest.mark.calendar, pytest.mark.negative, allure.feature('Calendar'),
              allure.story('Невалидные даты'), allure.severity(allure.severity_level.NORMAL)]


@allure.title('Календарь отклоняет невалидную дату: {value}')
@pytest.mark.parametrize('value', ['not-a-date', '2024-02-31', '2024-13-01', '2023-02-29'],
                         ids=['text', 'impossible-day', 'invalid-month', 'non-leap-year'])
def test_invalid_date_is_marked(calendar_page, value):
    calendar_page.enter_date(value)
    calendar_page.wait_validation(True)
    assert calendar_page.get_text(calendar_page.ERROR)


@allure.title('Исправление невалидной даты снимает ошибку')
def test_invalid_date_can_be_corrected(calendar_page):
    calendar_page.enter_date('bad-date')
    calendar_page.wait_validation(True)
    calendar_page.enter_date('2024-02-29')
    calendar_page.wait_validation(False)
    assert calendar_page.value() == '2024-02-29'
