"""Проверяется только управляемая страницей реклама."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from components.ad_banner import AdBanner


class AdsPage(BasePage):
    """Контейнер, закрытие, доступность основного контента."""
    path = '/ads/'
    CONTENT = (By.CSS_SELECTOR, 'main')
    HEADING = (By.CSS_SELECTOR, 'h1')

    @property
    def banner(self) -> AdBanner:
        return AdBanner(self)

    def heading_unobstructed(self) -> bool:
        """Проверить реальный hit-test, а не только наличие элемента в DOM."""
        self.scroll_to(self.HEADING)
        return bool(self.driver.execute_script(
            "const e=arguments[0],r=e.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return t===e||e.contains(t);",
            self.find(self.HEADING)))
