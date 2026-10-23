"""Неверные данные и неподдерживаемые способы закрытия."""
import allure
import pytest
from pages.modals_page import ModalsPage

pytestmark = [pytest.mark.modals, pytest.mark.negative, allure.feature('Modals'),
              allure.story('Ограничения и валидация'), allure.severity(allure.severity_level.NORMAL)]


@allure.title('Некорректный email отмечается ошибкой')
def test_invalid_email(modals_page: ModalsPage) -> None:
    modals_page.open_form()
    modals_page.fill_and_blur(modals_page.EMAIL, 'not-an-email')
    modals_page.wait_invalid(modals_page.EMAIL)
    with allure.step('Проверить отклонение email средствами браузера'):
        assert not modals_page.validity(modals_page.EMAIL)['valid']


@allure.title('Пустое обязательное имя отмечается ошибкой после очистки')
def test_empty_required_name(modals_page: ModalsPage) -> None:
    modals_page.open_form()
    modals_page.fill_and_blur(modals_page.NAME, 'Имя')
    modals_page.fill_and_blur(modals_page.NAME, '')
    with allure.step('Проверить required-валидацию без отправки формы'):
        assert modals_page.validity(modals_page.NAME)['valueMissing']
        assert not modals_page.validity(modals_page.NAME)['valid']


@allure.title('Escape не закрывает простое модальное окно')
def test_simple_modal_ignores_escape(modals_page: ModalsPage) -> None:
    modal = modals_page.open_simple()
    modal.escape()
    assert modal.remains_open()
    assert modals_page.get_text(modal.title) == 'Simple Modal'


@allure.title('Нажатие оверлея не закрывает простое модальное окно')
def test_simple_modal_ignores_overlay(modals_page: ModalsPage) -> None:
    modal = modals_page.open_simple()
    modal.click_overlay()
    assert modal.remains_open()
