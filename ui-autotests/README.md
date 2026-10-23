# UI-автотесты Practice Automation

Проект автоматизирует проверку календаря, модальных окон и рекламного окна на [Practice Automation](https://practice-automation.com). Отдельный сценарий считывает список Automation tools и заполняет им поле Message. Подходит для задания «Автоматизация тестирования Java/Python».

## Технологии и организация кода

- Python **3.12+**.
- Selenium **4.41.0** и встроенный Selenium Manager для подбора драйвера.
- Pytest **9.0.2**, allure-pytest **2.15.3**, python-dotenv **1.2.1**.
- Page Object Model: сценарии и проверки находятся в тестах; локаторы и действия — в страницах и компонентах.
- Каждый тест получает отдельный браузер. Сессия закрывается через `quit()` в `finally`.
- Используются явные ожидания `WebDriverWait`, без `time.sleep()`, неявных ожиданий и автоматического перезапуска упавших тестов.

## Структура проекта

```text
ui-autotests/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── calendar_page.py
│   ├── modals_page.py
│   ├── ads_page.py
│   └── message_form_page.py
├── components/
│   ├── __init__.py
│   ├── datepicker.py
│   ├── modal.py
│   └── ad_banner.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_calendar_positive.py
│   ├── test_calendar_negative.py
│   ├── test_modals_positive.py
│   ├── test_modals_negative.py
│   ├── test_ads_positive.py
│   ├── test_ads_negative.py
│   └── test_message_form.py
├── utils/                    # Ожидания, журналирование, подготовка дат
├── config/settings.py       # Загрузка и проверка настроек
├── scripts/                 # Запуск, установка CLI и проверка отчётов
├── allure-results/          # Результаты запусков, создаются автоматически
├── reports/                 # HTML, JUnit и скриншоты
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

## Установка

Нужны Python 3.12 или новее, установленный Chrome либо Firefox и доступ к сайту. При первом запуске Selenium Manager загружает совместимый драйвер: разрешите доступ через прокси или межсетевой экран.

Сначала установите [Git](https://git-scm.com/downloads/), [Python 3.12+](https://www.python.org/downloads/) и Chrome либо Firefox. Java нужна только для формирования и открытия Allure HTML, не для запуска Pytest.

Команды для Windows ниже рассчитаны на **cmd.exe**, а не PowerShell. Для новой копии проекта выполните:

```bat
git clone https://github.com/rimsult/ui-autotests.git
cd ui-autotests
cd ui-autotests
py -3.12 --version
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
if not exist .env copy .env.example .env
.venv\Scripts\activate.bat
python -m pytest --headless
```

Два перехода `cd ui-autotests` намеренные: первый открывает скачанный репозиторий, второй — вложенный каталог с `requirements.txt` и `pytest.ini`. Если репозиторий уже скачан, не клонируйте его повторно: откройте вложенный каталог проекта и начните с `py -3.12 --version`.

Все последующие команды выполняются из вложенного **ui-autotests**, после активации окружения. Условное копирование сохраняет уже настроенный `.env`. Если используете Python новее 3.12, замените `py -3.12` на соответствующую установленную версию.

Активацию можно пропустить, если вместо `python` указывать `.venv\Scripts\python.exe`. Если окружение создано в родительском каталоге, используйте `..\.venv\Scripts\python.exe`.

Linux/macOS:

```text
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
source .venv/bin/activate
python -m pytest --headless
```

Проверка интерфейса через `check_report_ui.py` использует Chrome независимо от браузера тестового прогона. Все пути в инструкциях относительные: имя пользователя и расположение скачанного репозитория значения не имеют.

## Настройка

`.env` читается из каталога проекта независимо от рабочей папки. Переменные процесса имеют приоритет.

| Переменная | Значение по умолчанию | Назначение |
|---|---|---|
| BASE_URL | https://practice-automation.com | Адрес сайта |
| BROWSER | chrome | `chrome` или `firefox` |
| HEADLESS | false | Запуск без окна при `true` |
| EXPLICIT_WAIT | 10 | Положительное конечное число секунд |
| WINDOW_WIDTH | 1920 | Ширина окна, положительное целое число |
| WINDOW_HEIGHT | 1080 | Высота окна, положительное целое число |
| MESSAGE_FORM_URL | https://practice-automation.com/form-fields/ | Форма с Message и Automation tools |

Если `MESSAGE_FORM_URL` не задан, используется `BASE_URL` + `/form-fields/`. При смене стенда измените оба адреса либо удалите `MESSAGE_FORM_URL` из `.env`. Некорректные настройки отклоняются до создания браузера. Для рекламы оставьте ожидание больше задержки её появления — около 4,5 секунды плюс анимация и время загрузки.

## Запуск тестов

После активации окружения:

```bat
python -m pytest tests --headless --alluredir=allure-results/run-01 --junitxml=reports/junit-run-01.xml
python -m pytest -m calendar --headless
python -m pytest -m modals --headless
python -m pytest -m ads --headless
python -m pytest -m message --headless
python -m pytest -m negative --headless
python -m pytest -m positive --headless
python -m pytest -m "calendar and positive" --headless
```

Чтобы увидеть окно, задайте `HEADLESS=false` в `.env` и не передавайте `--headless`. Для Firefox задайте `BROWSER=firefox`. Маркеры строгие: опечатка в имени маркера считается ошибкой.

Для полного headless-прогона с выбором браузера без изменения `.env`:

```bat
python scripts/run_browser_tests.py --browser chrome --run-name chrome-01
python scripts/run_browser_tests.py --browser firefox --run-name firefox-01
```

Скрипт создаёт `allure-results/<имя>` и `reports/junit-<имя>.xml`. Используйте новое имя для каждого запуска: существующие результаты не перезаписываются. Последовательный прогон занимает несколько минут; не создавайте избыточную нагрузку на публичный сайт.

## Allure-отчёты

`allure-pytest` сохраняет результаты, но HTML формирует отдельный **Allure Commandline**. Нужна Java, совместимая с установленной версией CLI. Для Allure 2.46.1 подходит Java 8+. Инструкции: https://allurereport.org/docs/install/ .

Локальная установка Allure 2 без изменения системного PATH:

```bat
java -version
python scripts/install_allure.py
```

Скрипт загружает официальный последний релиз Allure 2 из GitHub в `.tools`; путь выводится в терминал и сохраняется в `.tools/allure-path.txt`. Подставьте выведенную версию вместо `2.46.1`, если установлен другой выпуск. Локальные инструменты не включаются в Git.

Полный цикл с новым именем прогона (если `chrome-01` уже использовалось выше, выберите другое имя во всех командах блока):

```bat
python scripts/run_browser_tests.py --browser chrome --run-name chrome-01
java -classpath ".tools\allure-2.46.1\lib\*" io.qameta.allure.CommandLine generate allure-results/chrome-01 -o reports/allure-chrome-01
.tools\allure-2.46.1\bin\allure.bat open reports/allure-chrome-01
```

Если CLI установлен в PATH, доступны короткие команды:

```bat
allure generate allure-results/chrome-01 -o reports/allure-chrome-01
allure open reports/allure-chrome-01
allure serve allure-results/chrome-01
```

Открывайте HTML через `allure open`, а не двойным кликом по `index.html`: отчёт загружает данные по HTTP.

В отчёте есть русские названия, feature/story/severity, шаги и результат. При падении setup/call прикладываются PNG и исходный HTML до закрытия браузера. Если браузер не создан или его сессия потеряна, получить скриншот невозможно; ошибка диагностики прикладывается отдельно. Message сохраняет скриншот также при успехе: `reports/message-filled.png`. Файл `environment.properties` содержит Python, браузер и headless-режим.

Проверки артефактов и интерфейса отчёта:

```bat
python scripts/check_artifacts.py allure-results/chrome-01
python scripts/verify_cli_run.py chrome-01
python scripts/check_report_ui.py reports/allure-chrome-01
```

Первая команда проверяет метки, шаги и наличие вложений, вторая сопоставляет состав тестов и число успешных результатов JUnit/Allure/HTML. Третья открывает Suites в Chrome через временный локальный сервер и сохраняет скриншот рядом с отчётом. Она проверяет наличие поля поиска и дерева результатов, а не работу фильтрации. Сервер и браузер закрываются после проверки.

### Диагностика проверки интерфейса отчёта

`browser_check_ui` — вспомогательная проверка страницы во встроенном браузере среды разработки, а не тест из Pytest. Её красный статус сам по себе не означает падение UI-набора. Результаты тестов смотрите в выводе Pytest, JUnit и Allure, а причину сбоя проверки — в её сообщении.

- **`Unknown attribute "exact"`** означает ошибку синтаксиса селектора проверки. Для перехода в Suites используйте CSS `a[href="#suites"]` или `role=link[name="Suites"]` без `[exact=true]`. Suites — ссылка, не заголовок. В `scripts/check_report_ui.py` уже используется CSS-селектор ссылки.
- **`External resource blocked by browser policy: www.googletagmanager.com/gtag/js`** означает, что встроенный браузер запретил внешнюю аналитику Allure. Это не ошибка локальных JSON с результатами. При этом отчёт может оставаться работоспособным: проверяйте переход в Suites, поле поиска и дерево тестов. Не нужно отключать сетевую защиту или править сгенерированный отчёт ради статуса проверки.
- При открытии `index.html` через `file://` данные могут не загрузиться. Открывайте отчёт командой `open`, приведённой выше, либо выполните независимую локальную проверку:

```bat
python scripts/check_report_ui.py reports/allure-chrome-01
python scripts/verify_cli_run.py chrome-01
```

Эти команды выполняются после собственного прогона и генерации HTML из раздела Allure. Готовые результаты и отчёты не поставляются в репозитории. Первая команда завершается с ненулевым кодом при ошибке интерфейса и сохраняет `reports/allure-chrome-01-suites.png` при успехе. Вторая сверяет сохранённые результаты; ни одна из них не запускает тесты сайта повторно. Успех этих проверок не отменяет возможное ограничение внешней сети во встроенном браузере.

## Тестовые сценарии

Всего **40 тестовых случаев** с учётом параметризации.

| Раздел | Позитивные | Негативные |
|---|---:|---:|
| Calendar | 10 | 5 |
| Modals | 9 | 4 |
| Ads | 7 | 4 |
| Message | 1 | — |

### Calendar — `/calendars/`

Позитивные, `tests/test_calendar_positive.py`:

1. `test_calendar_page_loads` — заголовок и доступность поля даты.
2. `test_datepicker_opens` — клик по полю открывает календарь.
3. `test_select_current_month` — выбор 15-го числа текущего месяца.
4. `test_select_next_month` — переход вперёд и выбор первого числа.
5. `test_select_previous_month` — переход назад и выбор первого числа.
6. `test_select_today` — выбор сегодняшней даты в сетке.
7. `test_manual_leap_date` — ручной ввод 29 февраля високосного года.
8. `test_clear_and_reselect` — очистка и повторный выбор.
9. `test_selection_closes_picker` — закрытие после выбора и сохранение ожидаемой даты при открытии.
10. `test_year_boundary_navigation` — переход декабрь → январь следующего года → декабрь исходного года независимо от месяца запуска.

Негативные, `tests/test_calendar_negative.py`:

1. `test_invalid_date_is_marked[text]` — текст вместо даты.
2. `[impossible-day]` — 31 февраля.
3. `[invalid-month]` — 13-й месяц.
4. `[non-leap-year]` — 29 февраля невисокосного года.
5. `test_invalid_date_can_be_corrected` — снятие ошибки после исправления.

Неправильный ввод проверяется по реальному значению поля, `aria-invalid` и видимому сообщению. Текущая дата берётся из браузера. Расчёты учитывают год; даты нормализуются в `datetime.date`.

### Modals — `/modals/`

Позитивные, `tests/test_modals_positive.py`:

1. `test_modals_page_loads` — заголовок и две кнопки открытия.
2. `test_simple_modal_content` — заголовок и содержимое простого окна.
3. `test_simple_modal_closes` — закрытие крестиком.
4. `test_simple_modal_reopens` — повторное открытие.
5. `test_form_modal_opens` — заголовок и доступность полей формы.
6. `test_form_modal_closes` — закрытие формы крестиком.
7. `test_form_modal_escape` — закрытие формы по Escape.
8. `test_form_fields_can_be_filled` — заполнение Name, Email, Message и сравнение значений.
9. `test_switch_between_modals` — открытие формы после закрытия простого окна.

Негативные, `tests/test_modals_negative.py`:

1. `test_invalid_email` — невалидный email отклоняется.
2. `test_empty_required_name` — очищенное обязательное имя имеет `valueMissing` и `valid=false`.
3. `test_simple_modal_ignores_escape` — Escape не закрывает простое окно.
4. `test_simple_modal_ignores_overlay` — клик вне содержимого не закрывает простое окно.

Проверки запрета закрытия наблюдают состояние 1,2 секунды, дольше анимации, через явное ожидание смены состояния. Они не ограничены мгновенной проверкой после действия.

### Ads — `/ads/`

Позитивные, `tests/test_ads_positive.py`:

1. `test_ads_page_loads` — заголовок и основное содержимое.
2. `test_ad_container_exists` — контейнер с ролью dialog в DOM.
3. `test_ad_appears` — автоматическое появление.
4. `test_ad_close_button_available` — доступный крестик с подписью Close.
5. `test_ad_closes` — закрытие и исчезновение.
6. `test_content_available_after_close` — основной контент не перекрыт, проверка через `elementFromPoint`.
7. `test_close_keeps_navigation` — закрытие не меняет URL и список окон.

Негативные и защитные UI-сценарии, `tests/test_ads_negative.py`:

1. `test_ad_ignores_escape` — неподдерживаемый Escape не закрывает рекламу.
2. `test_ad_overlay_does_not_dismiss` — клик по оверлею не закрывает рекламу.
3. `test_open_ad_blocks_background_click` — настоящий Selenium-клик по фону отклоняется с `ElementClickInterceptedException`; окно остаётся открытым, навигация не меняется.
4. `test_closed_ad_does_not_intercept_click` — проверка отсутствия невидимого оверлея: после закрытия настоящий клик по фону проходит, реклама остаётся скрытой.

Первые три проверяют отклонение действий интерфейсом; четвёртый — защитную регрессию после закрытия. Проверки не заменяются вызовом идемпотентного Python-адаптера и не зависят от внешнего рекламного контента.

### Message — `/form-fields/`

`test_message_field_is_filled_from_automation_tools`:

1. Открывает `MESSAGE_FORM_URL`.
2. Находит через Selenium элементы `li` списка после подписи Automation tools внутри `feedbackForm`.
3. Читает `.text`, нормализует пробелы, удаляет пустые строки и дубли с сохранением порядка.
4. Независимо формирует ожидаемую строку через `, `.
5. Заполняет поле Message списком, повторно считанным со страницы.
6. Сравнивает значение с ожидаемым и прикладывает скриншот.

**Названия инструментов не захардкожены. Форма не отправляется.** При пустом списке тест сообщает причину; отсутствие раздела приводит к ошибке поиска. URL можно заменить в `.env`.

## Допущения и ограничения

Локаторы подобраны по DOM сайта. Публичный сайт может изменяться независимо от тестов; успешный прогон не гарантирует работу будущей версии.

- Календарь Jetpack использует `.dp`, `.dp-next`, `.dp-prev`, `.dp-day`. Повторное открытие кратковременно блокируется самим компонентом; вспомогательная операция ожидает открытие с ArrowDown. Отдельный тест открытия проверяет только настоящий клик, без обхода клавиатурой.
- Поле даты необязательное, ограниченный диапазон дат не задан. Проверки пустой обязательной даты и запрещённых дат неприменимы. Отдельных кнопок Today, Clear и Confirm нет; используются сетка и ручная очистка.
- Модальные окна реализованы в DOM через Popup Maker. Простое окно не закрывается по Escape и оверлею; форма закрывается по Escape. Дополнительных Cancel/Save и подтверждения потери данных нет.
- Проверяются заполнение и клиентская валидация формы. Успешная отправка и серверный результат не проверяются: на публичном сайте это создаёт реальные обращения. Для такого сценария нужен отдельный разрешённый стенд. Набор не заявляет покрытие серверной отправки.
- Реклама — контролируемый DOM-диалог `#pum-1272`, не внешний iframe. Смена объявлений отсутствует. Проверки внешних рекламных сетей, содержимого и переходов не выполняются.
- BasePage поддерживает iframe, новые окна и нативные alert/confirm/prompt; Dialog объединяет DOM- и нативный варианты. Нативные диалоги на этих страницах не используются, их наличие в базе не означает UI-покрытия на сайте.
- Проверки сохранения состояния имеют ограниченное окно наблюдения, а не обещают бесконечное отсутствие повторного открытия.
- Chrome и Firefox поддерживаются настройками; результат одного браузера не подтверждает другой. Рекомендуется запускать нужную конфигурацию перед передачей работы.
- `.tools`, `.env`, окружение и результаты не входят в Git. DOM и скриншоты могут содержать данные страницы: проверьте их перед передачей.

## Что проверить вручную после клонирования

1. Python 3.12+, браузер и Java для CLI доступны. Драйвер может загрузиться через используемую сеть.
2. На `/calendars/` есть `#g1065-1-selectorenteradate` и элементы `.dp` после открытия.
3. На `/modals/` есть `#simpleModal`, `#formModal`, окна `#pum-1318`, `#pum-674` и поля `input.name`, `input.email`, `textarea[id]` внутри формы.
4. На `/ads/` без блокировщика появляется `#pum-1272`, доступен `.pum-close`.
5. На `/form-fields/` есть `#feedbackForm`, подпись Automation tools, следующий список `ul/li` и `[data-testid="message"]`.
6. При изменении DOM обновите локаторы в `pages/` и `components/`, не переносите их в тесты. XPath для списка инструментов нужен, поскольку у списка нет устойчивого id.
