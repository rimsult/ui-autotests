"""Проверки контролируемой рекламы, без проверки внешних объявлений."""
import allure
import pytest

pytestmark = [pytest.mark.ads, pytest.mark.positive, allure.feature('Ads'),
              allure.story('Появление и закрытие рекламы'), allure.severity(allure.severity_level.NORMAL)]


@allure.title('Страница рекламы загружается с основным содержимым')
def test_ads_page_loads(ads_page):
    assert ads_page.heading() == 'Ads'
    assert ads_page.get_text(ads_page.CONTENT)


@allure.title('Рекламный контейнер существует в DOM')
def test_ad_container_exists(ads_page):
    assert ads_page.find(ads_page.banner.root).get_attribute('role') == 'dialog'


@allure.title('Реклама автоматически появляется после загрузки')
def test_ad_appears(ads_page):
    ads_page.banner.wait_open()
    assert ads_page.banner.visible()


@allure.title('Кнопка закрытия рекламы доступна для клика')
def test_ad_close_button_available(ads_page):
    ads_page.banner.wait_open()
    assert ads_page.wait_clickable(ads_page.banner.close_button).get_attribute('aria-label') == 'Close'


@allure.title('Кнопка закрытия скрывает рекламу')
def test_ad_closes(ads_page):
    ads_page.banner.wait_open()
    ads_page.banner.close()
    assert not ads_page.banner.visible()


@allure.title('После закрытия рекламы основной контент остаётся доступен')
def test_content_available_after_close(ads_page):
    ads_page.banner.wait_open()
    ads_page.banner.close()
    assert ads_page.heading_unobstructed()
    assert ads_page.heading() == 'Ads'


@allure.title('Закрытие рекламы не открывает новые окна и не меняет адрес')
def test_close_keeps_navigation(ads_page):
    ads_page.banner.wait_open()
    address = ads_page.driver.current_url
    handles = ads_page.driver.window_handles
    ads_page.banner.close()
    assert ads_page.driver.current_url == address
    assert ads_page.driver.window_handles == handles
