"""Отдельное обязательное упражнение со списком инструментов."""
import allure
import pytest
from config.settings import ROOT

pytestmark = [pytest.mark.message, pytest.mark.positive, allure.feature('MessageForm'),
              allure.story('Заполнение из Automation tools'), allure.severity(allure.severity_level.CRITICAL)]


@allure.title('Message заполняется списком Automation tools, прочитанным со страницы')
def test_message_field_is_filled_from_automation_tools(message_page):
    expected = message_page.fill_from_tools()
    with allure.step('Проверить точное значение Message без отправки формы'):
        assert message_page.get_value(message_page.MESSAGE) == expected
    message_page.scroll_to(message_page.MESSAGE)
    message_page.attach_screenshot_to_allure('Заполненное поле Message')
    directory = ROOT / 'reports'
    directory.mkdir(exist_ok=True)
    message_page.driver.save_screenshot(str(directory / 'message-filled.png'))
