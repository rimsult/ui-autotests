# UI-автотесты Practice Automation

Проект на Python 3.12+, Selenium, Pytest и Allure для проверки Calendar, Modals, Ads и заполнения Message динамическим списком Automation tools.

**Код, описание 40 тестовых случаев, настройки и подробная инструкция находятся во вложенном каталоге [ui-autotests](ui-autotests/README.md).**

## Быстрый запуск в Windows (cmd.exe)

Предварительно установите [Git](https://git-scm.com/downloads/), [Python 3.12+](https://www.python.org/downloads/) и Google Chrome. Нужен доступ в интернет: Selenium Manager загружает драйвер, тесты обращаются к публичному сайту.

```bat
git clone https://github.com/rimsult/ui-autotests.git
cd ui-autotests
cd ui-autotests
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
if not exist .env copy .env.example .env
.venv\Scripts\python.exe scripts/run_browser_tests.py --browser chrome --run-name reviewer-chrome-01
```

Два перехода `cd` нужны: первый открывает репозиторий, второй — каталог проекта с `requirements.txt` и `pytest.ini`. Для следующего прогона используйте новое имя, например `reviewer-chrome-02`. Для Firefox замените `--browser chrome` на `--browser firefox` и установите Firefox. Если используете Python новее 3.12, замените `py -3.12` на соответствующую установленную версию.

## HTML-отчёт

Для Allure CLI дополнительно установите Java. Из того же каталога проекта:

```bat
java -version
.venv\Scripts\python.exe scripts/install_allure.py
```

Установщик выводит путь к локальному Allure и записывает его в `.tools/allure-path.txt`. Если установлен Allure 2.46.1, выполните:

```bat
java -classpath ".tools\allure-2.46.1\lib\*" io.qameta.allure.CommandLine generate allure-results/reviewer-chrome-01 -o reports/allure-reviewer-chrome-01
.tools\allure-2.46.1\bin\allure.bat open reports/allure-reviewer-chrome-01
```

Если установщик выбрал другую версию, замените `2.46.1` в обеих командах на выведенную версию. Allure 2.46.1 работает с Java 8+. Для запуска самих тестов Java и Allure CLI не нужны.

Окружения, локальные инструменты, `.env` и результаты прогонов не поставляются: они создаются на компьютере проверяющего. Открывайте отчёт через `allure open`, а не двойным кликом по `index.html`.

Полные команды для Windows и Linux/macOS, сценарии, настройки и ограничения описаны в [README проекта](ui-autotests/README.md). Набор не отправляет контактную форму на публичном сайте; поддержка браузера в настройках не заменяет отдельный прогон в нём.
