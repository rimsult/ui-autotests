"""Неверные данные и запрещённые способы закрытия."""
import allure
import pytest

pytestmark = [pytest.mark.modals, pytest.mark.negative, allure.feature('Modals'),
              allure.story('Ограничения и валидация'), allure.severity(allure.severity_level.NORMAL)]


@allure.title('Некорректный email отмечается ошибкой')
def test_invalid_email(modals_page):
    modals_page.open_form()
    modals_page.fill_and_blur(modals_page.EMAIL, 'not-an-email')
    modals_page.wait_invalid(modals_page.EMAIL)
    assert not modals_page.find(modals_page.EMAIL).get_property('validity')['valid']


@allure.title('Пустое обязательное имя отмечается ошибкой после очистки')
def test_empty_required_name(modals_page):
    modals_page.open_form()
    modals_page.fill_and_blur(modals_page.NAME, 'Имя')
    modals_page.fill_and_blur(modals_page.NAME, '')
    with allure.step('Проверить нативную required-валидацию без отправки формы'):
        assert modals_page.find(modals_page.NAME).get_property('validity')['valueMissing']
        assert not modals_page.find(modals_page.NAME).get_property('validity')['valid']


@allure.title('Escape не закрывает простую модалку: отключено настройками сайта')
def test_simple_modal_ignores_escape(modals_page):
    modal = modals_page.open_simple()
    modal.escape()
    # Следующая команда проходит после обработки события клавиатуры браузером.
    assert modal.visible()
    assert modals_page.get_text(modal.title) == 'Simple Modal'


@allure.title('Нажатие оверлея не закрывает простую модалку')
def test_simple_modal_ignores_overlay(modals_page):
    modal = modals_page.open_simple()
    modal.click_overlay()
    assert modal.visible()
