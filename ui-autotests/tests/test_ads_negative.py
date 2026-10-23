"""Пограничные действия без нестабильного внешнего контента."""
import allure
import pytest

pytestmark = [pytest.mark.ads, pytest.mark.negative, allure.feature('Ads'),
              allure.story('Безопасное взаимодействие с рекламой'), allure.severity(allure.severity_level.NORMAL)]


@allure.title('Повторная команда закрытия не пытается кликнуть скрытую рекламу')
def test_repeated_close_is_safe(ads_page):
    ads_page.banner.wait_open()
    assert ads_page.banner.close_if_visible()
    assert not ads_page.banner.close_if_visible()
    assert not ads_page.banner.visible()


@allure.title('Клик по оверлею не закрывает рекламу при отключённом overlay close')
def test_ad_overlay_does_not_dismiss(ads_page):
    ads_page.banner.wait_open()
    ads_page.banner.click_overlay()
    assert ads_page.banner.visible()


@allure.title('Скрытая реклама не перехватывает клик по основному содержимому')
def test_closed_ad_does_not_intercept_click(ads_page):
    ads_page.banner.wait_open()
    ads_page.banner.close()
    assert ads_page.heading_unobstructed()
    ads_page.click(ads_page.HEADING)
    assert not ads_page.banner.visible()
    assert ads_page.heading() == 'Ads'
