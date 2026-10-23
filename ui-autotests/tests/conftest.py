"""Браузерные фикстуры и диагностика ошибок до закрытия сессии."""
import os
import sys
from pathlib import Path
from collections.abc import Generator, Iterator
from typing import Any
import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from config.settings import Settings
from pages.base_page import BasePage
from pages.calendar_page import CalendarPage
from pages.modals_page import ModalsPage
from pages.ads_page import AdsPage
from pages.message_form_page import MessageFormPage


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption('--headless', action='store_true', help='Запуск без видимого окна браузера')


@pytest.fixture(scope='session')
def settings(request: pytest.FixtureRequest) -> Settings:
    if sys.version_info < (3, 12):
        raise pytest.UsageError('Нужен Python 3.12 или новее')
    if request.config.getoption('--headless'):
        os.environ['HEADLESS'] = 'true'
    return Settings.from_env()


@pytest.fixture
def driver(settings: Settings) -> Iterator[WebDriver]:
    """Создать отдельную сессию Selenium Manager и закрыть её после теста."""
    options = webdriver.ChromeOptions() if settings.browser == 'chrome' else webdriver.FirefoxOptions()
    options.page_load_strategy = 'eager'
    if settings.headless:
        options.add_argument('--headless=new' if settings.browser == 'chrome' else '-headless')
    factory = webdriver.Chrome if settings.browser == 'chrome' else webdriver.Firefox
    browser = factory(options=options)
    try:
        browser.implicitly_wait(0)
        browser.set_page_load_timeout(45)
        browser.set_window_size(settings.window_width, settings.window_height)
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def message_page(driver: WebDriver, settings: Settings) -> MessageFormPage:
    return MessageFormPage(driver, settings).open()


@pytest.fixture
def calendar_page(driver: WebDriver, settings: Settings) -> CalendarPage:
    return CalendarPage(driver, settings).open()


@pytest.fixture
def modals_page(driver: WebDriver, settings: Settings) -> ModalsPage:
    return ModalsPage(driver, settings).open()


@pytest.fixture
def ads_page(driver: WebDriver, settings: Settings) -> AdsPage:
    return AdsPage(driver, settings).open()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]) -> Generator[None, Any, None]:
    """Добавить диагностику, сохранив исходную причину падения теста."""
    outcome = yield
    report = outcome.get_result()
    if report.failed and 'driver' in item.funcargs:
        page = BasePage(item.funcargs['driver'], item.funcargs['settings'])
        for attach in (page.attach_screenshot_to_allure, page.attach_page_source_to_allure):
            try:
                attach()
            except WebDriverException as error:
                allure.attach(str(error), 'Ошибка сбора диагностики', allure.attachment_type.TEXT)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Записать параметры запуска без секретов и содержимого окружения."""
    directory = session.config.getoption('--alluredir')
    if directory:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        try:
            current = Settings.from_env()
        except ValueError:
            return
        (path / 'environment.properties').write_text(
            f'Python={sys.version.split()[0]}\nBrowser={current.browser}\n'
            f'Headless={str(current.headless).lower()}\n', encoding='utf-8')
