"""Две DOM-модалки Popup Maker, включая локальную валидацию формы."""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from components.modal import Modal


class ModalsPage(BasePage):
    """Без успешной отправки контактных данных внешнему сайту."""
    path = '/modals/'
    SIMPLE_TRIGGER = (By.ID, 'simpleModal')
    FORM_TRIGGER = (By.ID, 'formModal')
    NAME = (By.CSS_SELECTOR, '#pum-674 input.name')
    EMAIL = (By.CSS_SELECTOR, '#pum-674 input.email')
    MESSAGE = (By.CSS_SELECTOR, '#pum-674 textarea[id]')
    ACTIVE = (By.CSS_SELECTOR, '.pum-overlay.pum-active')

    @property
    def simple(self) -> Modal:
        return Modal(self, '#pum-1318')

    @property
    def form(self) -> Modal:
        return Modal(self, '#pum-674')

    @allure.step('Открыть простое модальное окно')
    def open_simple(self) -> Modal:
        self.click(self.SIMPLE_TRIGGER)
        self.simple.wait_open()
        return self.simple

    @allure.step('Открыть модальное окно с формой')
    def open_form(self) -> Modal:
        self.click(self.FORM_TRIGGER)
        self.form.wait_open()
        return self.form

    @allure.step('Заполнить поле модалки и убрать фокус')
    def fill_and_blur(self, locator: tuple[str, str], value: str) -> None:
        self.type_text(locator, value)
        self.find(locator).send_keys(Keys.TAB)

    def wait_invalid(self, locator: tuple[str, str]) -> None:
        self.wait.until(lambda _: self.find(locator).get_attribute('aria-invalid') == 'true')
