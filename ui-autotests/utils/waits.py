"""Явные ожидания без неявного ожидания Selenium."""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


def explicit_wait(driver: WebDriver, timeout: float) -> WebDriverWait:
    """Создать ожидание с умеренным интервалом опроса."""
    return WebDriverWait(driver, timeout, poll_frequency=0.2)
