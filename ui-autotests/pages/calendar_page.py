"""Выбор и локальная валидация даты без отправки формы."""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from components.datepicker import DatePicker


class CalendarPage(BasePage):
    """Календарь Jetpack с форматом YYYY-MM-DD."""
    path = '/calendars/'
    FIELD = (By.ID, 'g1065-1-selectorenteradate')
    ERROR = (By.ID, 'g1065-1-selectorenteradate-text-error-message')

    @property
    def picker(self) -> DatePicker:
        return DatePicker(self, self.FIELD)

    @allure.step('Ввести дату и убрать фокус: {value}')
    def enter_date(self, value: str) -> None:
        self.type_text(self.FIELD, value)
        self.find(self.FIELD).send_keys(Keys.TAB)

    def value(self) -> str:
        return self.get_value(self.FIELD)

    def invalid(self) -> bool:
        return self.find(self.FIELD).get_attribute('aria-invalid') == 'true'

    @allure.step('Дождаться состояния валидации: ошибка={expected}')
    def wait_validation(self, expected: bool) -> None:
        self.wait.until(lambda _: self.invalid() == expected)
