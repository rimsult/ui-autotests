"""Открытие, закрытие и заполнение настоящих DOM-диалогов."""
import allure
import pytest

pytestmark = [pytest.mark.modals, pytest.mark.positive, allure.feature('Modals'),
              allure.story('Жизненный цикл модального окна'), allure.severity(allure.severity_level.NORMAL)]


@allure.title('Страница модальных окон загружается')
def test_modals_page_loads(modals_page):
    assert modals_page.heading() == 'Modals'
    assert modals_page.wait_clickable(modals_page.SIMPLE_TRIGGER).is_enabled()
    assert modals_page.wait_clickable(modals_page.FORM_TRIGGER).is_enabled()


@allure.title('Простое окно открывается с заголовком и содержимым')
def test_simple_modal_content(modals_page):
    modal = modals_page.open_simple()
    assert modals_page.get_text(modal.title) == 'Simple Modal'
    assert modals_page.get_text(modal.content)


@allure.title('Простое окно закрывается крестиком')
def test_simple_modal_closes(modals_page):
    modal = modals_page.open_simple()
    modal.close()
    assert not modal.visible()


@allure.title('Простое окно можно открыть повторно')
def test_simple_modal_reopens(modals_page):
    modals_page.open_simple().close()
    assert modals_page.open_simple().visible()


@allure.title('Окно формы открывается с доступными полями')
def test_form_modal_opens(modals_page):
    modal = modals_page.open_form()
    assert modals_page.get_text(modal.title) == 'Modal Containing A Form'
    for locator in (modals_page.NAME, modals_page.EMAIL, modals_page.MESSAGE):
        assert modals_page.wait_clickable(locator).is_enabled()


@allure.title('Окно формы закрывается крестиком')
def test_form_modal_closes(modals_page):
    modal = modals_page.open_form()
    modal.close()
    assert not modal.visible()


@allure.title('Окно формы закрывается по Escape')
def test_form_modal_escape(modals_page):
    modal = modals_page.open_form()
    modal.escape()
    assert modals_page.wait_invisible(modal.root)


@allure.title('Поля формы сохраняют введённые значения без отправки')
def test_form_fields_can_be_filled(modals_page):
    modals_page.open_form()
    values = [(modals_page.NAME, 'Тестовый пользователь'), (modals_page.EMAIL, 'qa@example.org'),
              (modals_page.MESSAGE, 'Проверка интерфейса без отправки')]
    for locator, value in values:
        modals_page.fill_and_blur(locator, value)
        assert modals_page.get_value(locator) == value


@allure.title('После закрытия простого окна можно открыть окно формы')
def test_switch_between_modals(modals_page):
    modals_page.open_simple().close()
    assert modals_page.open_form().visible()
    assert not modals_page.simple.visible()
