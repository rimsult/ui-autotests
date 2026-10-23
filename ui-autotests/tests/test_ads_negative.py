"""Неподдерживаемые способы закрытия и защита фонового содержимого."""
import allure
import pytest
from selenium.common.exceptions import ElementClickInterceptedException
from pages.ads_page import AdsPage

pytestmark = [pytest.mark.ads, pytest.mark.negative, allure.feature('Ads'),
              allure.story('Ограничения взаимодействия с рекламой'),
              allure.severity(allure.severity_level.NORMAL)]


@allure.title('Escape не закрывает рекламное окно')
def test_ad_ignores_escape(ads_page: AdsPage) -> None:
    ads_page.banner.wait_open()
    ads_page.banner.escape()
    with allure.step('Проверить, что окно остаётся открытым после обработки Escape'):
        assert ads_page.banner.remains_open()


@allure.title('Нажатие оверлея не закрывает рекламное окно')
def test_ad_overlay_does_not_dismiss(ads_page: AdsPage) -> None:
    ads_page.banner.wait_open()
    ads_page.banner.click_overlay()
    with allure.step('Проверить, что клик вне содержимого не закрывает окно'):
        assert ads_page.banner.remains_open()


@allure.title('Открытая реклама блокирует клик по фоновому содержимому')
def test_open_ad_blocks_background_click(ads_page: AdsPage) -> None:
    ads_page.banner.wait_open()
    address = ads_page.driver.current_url
    handles = ads_page.driver.window_handles
    with allure.step('Проверить отклонение настоящего Selenium-клика по фону'):
        with pytest.raises(ElementClickInterceptedException):
            ads_page.click(ads_page.HEADING)
        assert ads_page.banner.remains_open()
        assert ads_page.driver.current_url == address
        assert ads_page.driver.window_handles == handles


@allure.title('Скрытая реклама не перехватывает клик по основному содержимому')
def test_closed_ad_does_not_intercept_click(ads_page: AdsPage) -> None:
    ads_page.banner.wait_open()
    ads_page.banner.close()
    with allure.step('Проверить отсутствие невидимого перекрытия и выполнить клик'):
        assert ads_page.heading_unobstructed()
        ads_page.click(ads_page.HEADING)
        assert ads_page.banner.remains_closed()
        assert ads_page.heading() == 'Ads'
