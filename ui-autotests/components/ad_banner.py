"""Контролируемая рекламная DOM-модалка без внешнего контента."""
import allure
from components.modal import Modal
from pages.base_page import BasePage


class AdBanner(Modal):
    """Реклама автоматически появляется с задержкой около пяти секунд."""
    def __init__(self, page: BasePage) -> None:
        super().__init__(page, '#pum-1272')

    @allure.step('Закрыть рекламу, если она видима')
    def close_if_visible(self) -> bool:
        if not self.visible():
            return False
        self.close()
        return True
