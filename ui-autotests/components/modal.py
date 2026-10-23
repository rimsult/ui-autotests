"""DOM-модалка и общий адаптер нативных диалогов."""
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class Modal:
    """Операции ограничены одним конкретным диалогом."""
    def __init__(self, page: BasePage, css: str) -> None:
        self.page = page
        self.css = css
        self.root = (By.CSS_SELECTOR, css)
        self.close_button = (By.CSS_SELECTOR, css + ' .pum-close')
        self.title = (By.CSS_SELECTOR, css + ' .pum-title')
        self.content = (By.CSS_SELECTOR, css + ' .pum-content')

    @allure.step('Дождаться открытия модального окна')
    def wait_open(self) -> None:
        self.page.wait_visible(self.root)
        self.page.wait_clickable(self.close_button)

    @allure.step('Закрыть модальное окно крестиком')
    def close(self) -> None:
        self.page.click(self.close_button)
        self.page.wait_invisible(self.root)

    @allure.step('Нажать Escape')
    def escape(self) -> None:
        ActionChains(self.page.driver).send_keys(Keys.ESCAPE).perform()

    @allure.step('Нажать на оверлей вне содержимого')
    def click_overlay(self) -> None:
        element = self.page.wait_visible(self.root)
        # Верхний левый угол оверлея находится за пределами центрального окна.
        ActionChains(self.page.driver).move_to_element_with_offset(
            element, -element.size['width'] / 2 + 5, -element.size['height'] / 2 + 5).click().perform()

    def visible(self) -> bool:
        return self.page.is_visible(self.root)

    def _remains_in_state(self, visible: bool, seconds: float) -> bool:
        """Наблюдать состояние дольше анимации закрытия, не заменяя ожидание паузой."""
        if self.visible() != visible:
            return False
        try:
            WebDriverWait(self.page.driver, seconds, poll_frequency=0.1).until(
                lambda _: self.visible() != visible)
        except TimeoutException:
            return True
        return False

    @allure.step('Убедиться, что окно не закрывается в течение {seconds} секунд')
    def remains_open(self, seconds: float = 1.2) -> bool:
        return self._remains_in_state(True, seconds)

    @allure.step('Убедиться, что окно остаётся скрытым в течение {seconds} секунд')
    def remains_closed(self, seconds: float = 1.2) -> bool:
        return self._remains_in_state(False, seconds)


class Dialog:
    """Адаптер для DOM или нативного alert/confirm/prompt без угадывания типа."""
    def __init__(self, page: BasePage, dom: Modal | None = None) -> None:
        self.page = page
        self.dom = dom

    def wait_open(self) -> str:
        return self.page.wait.until(lambda d: 'native' if EC.alert_is_present()(d)
                                    else ('dom' if self.dom and self.dom.visible() else False))

    def _dom(self) -> Modal:
        if self.dom is None:
            raise RuntimeError('DOM-компонент диалога не настроен')
        return self.dom

    def text(self) -> str:
        return self.page.get_alert_text() if self.wait_open() == 'native' else self.page.get_text(self._dom().content)

    def accept(self, text: str | None = None) -> None:
        if self.wait_open() == 'native':
            self.page.accept_alert(text)
        else:
            if text is not None:
                raise ValueError('Ввод prompt доступен только для нативного диалога')
            self._dom().close()

    def dismiss(self) -> None:
        if self.wait_open() == 'native':
            self.page.dismiss_alert()
        else:
            self._dom().close()
