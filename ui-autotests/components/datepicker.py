"""Компонент Jetpack date picker, исследованный на реальном сайте."""
from datetime import date
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class DatePicker:
    """Навигация без подмены значения через JavaScript."""
    ROOT = (By.CSS_SELECTOR, '.dp')
    NEXT = (By.CSS_SELECTOR, '.dp-next')
    PREVIOUS = (By.CSS_SELECTOR, '.dp-prev')
    MONTH = (By.CSS_SELECTOR, '.dp-cal-month')
    YEAR = (By.CSS_SELECTOR, '.dp-cal-year')
    DAYS = (By.CSS_SELECTOR, '.dp-day:not(.dp-edge-day)')
    TODAY = (By.CSS_SELECTOR, '.dp-day-today')

    def __init__(self, page: BasePage, field: tuple[str, str]) -> None:
        self.page = page
        self.field = field

    @allure.step('Открыть календарь')
    def open(self) -> None:
        if not self.page.is_visible(self.ROOT):
            self.page.click(self.field)
        # После закрытия компонент временно блокирует open на 100 мс.
        # ArrowDown открывает, но не переключает состояние, в отличие от клика.
        def ensure_open(_):
            if self.page.is_visible(self.ROOT):
                return True
            self.page.find(self.field).send_keys(Keys.ARROW_DOWN)
            return self.page.is_visible(self.ROOT)
        self.page.wait.until(ensure_open)
        self.page.wait_visible(self.ROOT)

    def month_label(self) -> str:
        return self.page.get_text(self.MONTH) + self.page.get_text(self.YEAR)

    @allure.step('Перейти в соседний месяц: {offset}')
    def move_month(self, offset: int) -> None:
        self.open()
        for _ in range(abs(offset)):
            old = self.month_label()
            self.page.click(self.NEXT if offset > 0 else self.PREVIOUS)
            self.page.wait.until(lambda _: self.month_label() != old)

    @allure.step('Выбрать день {day} отображаемого месяца')
    def select_day(self, day: int) -> None:
        self.open()
        cells = self.page.find_all(self.DAYS)
        cell = next((e for e in cells if e.text == str(day)), None)
        if cell is None:
            raise AssertionError(f'День {day} отсутствует в отображаемом месяце')
        cell.click()
        self.page.wait_invisible(self.ROOT)

    def today(self) -> date:
        """Дата браузера, а не часов процесса запуска тестов."""
        return date.fromisoformat(self.page.driver.execute_script(
            "const d=new Date(); return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');"))
