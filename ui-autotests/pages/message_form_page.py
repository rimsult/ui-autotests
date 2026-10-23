"""Форма упражнения: список инструментов читается только из DOM."""
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MessageFormPage(BasePage):
    """Динамическое заполнение Message без отправки формы."""
    MESSAGE = (By.CSS_SELECTOR, '[data-testid="message"]')
    # У списка нет id: связь с подписью ограничена формой упражнения.
    TOOLS = (By.XPATH, "//form[@id='feedbackForm']/label[normalize-space()='Automation tools']/following-sibling::ul[1]/li")

    def open(self, url: str | None = None) -> 'MessageFormPage':
        super().open(url or self.settings.message_form_url)
        self.wait_visible(self.MESSAGE)
        return self

    @allure.step('Прочитать непустые названия Automation tools из DOM')
    def tools(self) -> list[str]:
        values = [' '.join(e.text.split()) for e in self.find_all(self.TOOLS)]
        values = list(dict.fromkeys(v for v in values if v))
        if not values:
            raise AssertionError('Раздел Automation tools найден, но не содержит непустых элементов')
        allure.attach('\n'.join(values), 'Инструменты из DOM', allure.attachment_type.TEXT)
        return values

    @allure.step('Заполнить Message инструментами через запятую')
    def fill_from_tools(self) -> str:
        value = ', '.join(self.tools())
        self.type_text(self.MESSAGE, value)
        return value
