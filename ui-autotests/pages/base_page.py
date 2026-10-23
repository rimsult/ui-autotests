"""Общие операции Selenium, без знаний о конкретных упражнениях."""
from typing import Self
from urllib.parse import urljoin
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from config.settings import Settings
from utils.waits import explicit_wait
from utils.logger import get_logger

Locator = tuple[str, str]


class BasePage:
    """Базовая страница с явными ожиданиями и диагностикой."""
    HEADING: Locator = (By.CSS_SELECTOR, 'h1')
    path = '/'

    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        self.driver = driver
        self.settings = settings
        self.wait = explicit_wait(driver, settings.explicit_wait)
        self.logger = get_logger(type(self).__name__)

    @allure.step('Открыть страницу')
    def open(self, url: str | None = None) -> Self:
        target = url or urljoin(self.settings.base_url + '/', self.path.lstrip('/'))
        self.logger.info('Открытие %s', target)
        self.driver.get(target)
        self.wait_visible(self.HEADING)
        return self

    @allure.step('Найти элемент {locator} в DOM')
    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: Locator) -> list[WebElement]:
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step('Нажать элемент {locator}')
    def click(self, locator: Locator) -> None:
        self.wait_clickable(locator).click()

    @allure.step('Заполнить поле {locator}')
    def type_text(self, locator: Locator, text: str) -> None:
        element = self.wait_clickable(locator)
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.BACKSPACE)
        if text:
            element.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        return self.wait_visible(locator).text.strip()

    def get_value(self, locator: Locator) -> str:
        value = self.find(locator).get_property('value')
        return '' if value is None else str(value)

    def is_visible(self, locator: Locator) -> bool:
        return any(e.is_displayed() for e in self.driver.find_elements(*locator))

    def is_hidden(self, locator: Locator) -> bool:
        return not self.is_visible(locator)

    def wait_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator: Locator) -> bool:
        return bool(self.wait.until(EC.invisibility_of_element_located(locator)))

    def scroll_to(self, locator: Locator) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center',behavior:'instant'});", self.find(locator))

    def switch_to_iframe(self, locator: Locator) -> None:
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()

    def switch_to_new_window(self, previous_handles: list[str]) -> None:
        self.wait.until(EC.new_window_is_opened(previous_handles))
        handle = next(h for h in self.driver.window_handles if h not in previous_handles)
        self.driver.switch_to.window(handle)

    def close_extra_windows(self, original_handle: str) -> None:
        for handle in self.driver.window_handles:
            if handle != original_handle:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(original_handle)

    @allure.step('Подтвердить нативный диалог')
    def accept_alert(self, text: str | None = None) -> None:
        alert = self.wait.until(EC.alert_is_present())
        if text is not None:
            alert.send_keys(text)
        alert.accept()

    def dismiss_alert(self) -> None:
        self.wait.until(EC.alert_is_present()).dismiss()

    def get_alert_text(self) -> str:
        return self.wait.until(EC.alert_is_present()).text

    def attach_screenshot_to_allure(self, name: str = 'Скриншот') -> None:
        allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)

    def attach_page_source_to_allure(self) -> None:
        allure.attach(self.driver.page_source, name='DOM страницы', attachment_type=allure.attachment_type.HTML)

    @allure.step('Проверить заголовок страницы')
    def heading(self) -> str:
        return self.get_text(self.HEADING)
