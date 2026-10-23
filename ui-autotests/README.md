# UI-автотесты Practice Automation

Учебный проект по заданию «Автоматизация тестирования Java/Python»: реальные браузерные проверки календаря, модальных окон, рекламы и динамическое заполнение Message.

## Технологии и архитектура

Python **3.12+**, Selenium 4, Pytest, allure-pytest, python-dotenv. Драйвер устанавливается встроенным Selenium Manager. Дополнительные тестовые фреймворки не нужны.

Page Object Model: тесты описывают сценарии и ожидаемые результаты; страницы содержат локаторы и операции; компоненты инкапсулируют календарь, диалог и рекламу. Нет `time.sleep()`, неявных ожиданий, повторных запусков упавших тестов или зависимостей от порядка. Каждый тест получает отдельную сессию браузера, которая закрывается через `quit()`.

## Структура

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
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── waits.py
│   ├── logger.py
│   └── data_generator.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── scripts/                  # Исследование сайта и проверка артефактов
├── allure-results/           # Создаётся при запуске, не хранится в Git
├── reports/                  # Скриншоты и JUnit, не хранится в Git
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

## Установка на Windows

Нужны установленный Python 3.12 или новее, Chrome либо Firefox, доступ в интернет. Для первого запуска Selenium Manager должен иметь доступ к загрузке совместимого драйвера. Не устанавливайте драйвер вручную без необходимости.

Команды из корня **ui-autotests** в cmd.exe:

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python.exe -m pytest --headless
```

Активация окружения необязательна: явный путь к интерпретатору исключает запуск из неправильного Python.

В текущем рабочем пространстве уже существует окружение **в родительской папке**, поэтому здесь использовалось:

```bat
cd ui-autotests
..\.venv\Scripts\python.exe -m pytest --headless
```

Для Linux/macOS: `python3.12 -m venv .venv`, затем `.venv/bin/python -m pip install -r requirements.txt` и `.venv/bin/python -m pytest --headless`.

## Настройка окружения

Скопируйте `.env.example` в `.env`. Файл читается независимо от рабочей папки. Переменные процесса имеют приоритет над `.env`.

| Параметр | Значение по умолчанию | Назначение |
|---|---|---|
| BASE_URL | https://practice-automation.com | Адрес сайта |
| BROWSER | chrome | chrome или firefox |
| HEADLESS | false | true — без видимого окна |
| EXPLICIT_WAIT | 10 | Явное ожидание в секундах |
| WINDOW_WIDTH | 1920 | Ширина окна |
| WINDOW_HEIGHT | 1080 | Высота окна |
| MESSAGE_FORM_URL | https://practice-automation.com/form-fields/ | Страница с Automation tools и Message |

Без MESSAGE_FORM_URL адрес вычисляется как BASE_URL + `/form-fields/`. Если заменяете BASE_URL на другой экземпляр сайта, удалите или измените MESSAGE_FORM_URL в `.env`.

`--headless` принудительно включает режим без окна. Неподдерживаемый браузер, некорректный URL, неправильное логическое значение и неположительные размеры/ожидания дают понятную ошибку до запуска браузера.

## Запуск

После активации своего окружения (`.venv\Scripts\activate`), из ui-autotests:

```bat
python -m pytest tests --alluredir=allure-results
python -m pytest -m calendar
python -m pytest -m modals
python -m pytest -m ads
python -m pytest -m message
python -m pytest -m negative
python -m pytest -m "calendar and positive" --headless
python -m pytest --headless --alluredir=allure-results/new-run --junitxml=reports/junit.xml
```

Не запускайте весь набор одновременно в десятках браузеров против публичного учебного сайта. Обычный последовательный прогон занимает несколько минут.

## Allure

`allure-pytest` создаёт результаты, но не устанавливает программу просмотра **Allure Commandline**. Для визуального HTML-отчёта отдельно установите Allure CLI и совместимую Java по официальной инструкции https://allurereport.org/docs/install/ . Установка системных программ в рамках проекта не производится.

```bat
allure --version
allure serve allure-results/new-run
```

Или сохраните статический отчёт:

```bat
allure generate allure-results/new-run -o allure-report --clean
allure open allure-report
```

Каждый тест имеет русское название, feature/story/severity. Общие действия оформлены шагами Allure. При ошибке setup/call, если драйвер уже создан, хук добавляет PNG и HTML **до закрытия браузера**. Если браузер вообще не запустился или сессия потеряна, скриншот получить невозможно: это не скрывается.

Тест Message прикладывает скриншот также при успехе и сохраняет `reports/message-filled.png`. Безопасные метаданные окружения записываются в `environment.properties`. DOM и скриншоты могут содержать данные страницы: не публикуйте диагностические файлы без проверки. Секреты из окружения в отчёт не копируются.

Для проверки структуры результатов:

```bat
python scripts/check_artifacts.py
```

Используйте отдельную папку для нового прогона: это исключает смешивание старых ошибок и новых результатов. Скрипт проверяет JSON, метки, шаги, наличие и ненулевой размер диагностических вложений для ошибок в подкаталогах allure-results.

## Все тестовые сценарии

Всего **38 запусков**: Calendar 9 позитивных + 5 негативных, Modals 9 + 4, Ads 7 + 3, Message 1 позитивный. Четыре варианта неправильной даты параметризованы: это четыре независимых тестовых случая с разными классами данных.

### Calendar — /calendars/

Позитивные (`tests/test_calendar_positive.py`):
1. `test_calendar_page_loads`: заголовок и доступное поле.
2. `test_datepicker_opens`: клик открывает календарь.
3. `test_select_current_month`: выбор 15-го числа текущего месяца.
4. `test_select_next_month`: следующий месяц и выбор первого числа, включая смену года.
5. `test_select_previous_month`: предыдущий месяц и выбор первого числа.
6. `test_select_today`: выбор сегодняшнего дня в сетке.
7. `test_manual_leap_date`: ручной ввод корректного 29 февраля високосного года.
8. `test_clear_and_reselect`: очистка и новый выбор даты.
9. `test_selection_closes_picker`: закрытие после выбора и сохранение значения при открытии.

Негативные (`tests/test_calendar_negative.py`):
1. `test_invalid_date_is_marked[text]`: текст вместо даты.
2. `[impossible-day]`: 31 февраля.
3. `[invalid-month]`: 13-й месяц.
4. `[non-leap-year]`: 29 февраля невисокосного года.
5. `test_invalid_date_can_be_corrected`: ошибка снимается после исправления.

Текущая дата берётся из часов браузера. Переходы используют первый день месяца и безопасны на границе года/месяца. Формат результата нормализуется в `datetime.date`. Неправильный ввод проверяется по `aria-invalid` и непустому реальному сообщению, без подмены валидации.

### Modals — /modals/

Позитивные (`tests/test_modals_positive.py`):
1. `test_modals_page_loads`: заголовок и обе кнопки.
2. `test_simple_modal_content`: открытие простого диалога, заголовок и содержимое.
3. `test_simple_modal_closes`: закрытие крестиком.
4. `test_simple_modal_reopens`: повторное открытие.
5. `test_form_modal_opens`: открытие диалога формы и доступность полей.
6. `test_form_modal_closes`: закрытие формы крестиком.
7. `test_form_modal_escape`: закрытие формы по Escape.
8. `test_form_fields_can_be_filled`: заполнение Name, Email, Message и проверка значений.
9. `test_switch_between_modals`: открытие формы после закрытия простого диалога.

Негативные (`tests/test_modals_negative.py`):
1. `test_invalid_email`: ошибочный email отмечается невалидным.
2. `test_empty_required_name`: очистка required-имени приводит к нативному `validity.valueMissing`; отправка не нужна.
3. `test_simple_modal_ignores_escape`: Escape не закрывает простой диалог — так настроен сайт.
4. `test_simple_modal_ignores_overlay`: клик вне содержимого не закрывает простой диалог.

### Ads — /ads/

Позитивные (`tests/test_ads_positive.py`):
1. `test_ads_page_loads`: основной контент и заголовок.
2. `test_ad_container_exists`: контролируемый контейнер-диалог в DOM.
3. `test_ad_appears`: автоматическое появление с ожиданием.
4. `test_ad_close_button_available`: доступность кнопки закрытия.
5. `test_ad_closes`: закрытие и исчезновение.
6. `test_content_available_after_close`: доступность контента с hit-test через elementFromPoint.
7. `test_close_keeps_navigation`: нет перехода или новых окон при закрытии.

Негативные (`tests/test_ads_negative.py`):
1. `test_repeated_close_is_safe`: повторная команда адаптера возвращает False, не кликая скрытый элемент. Это проверка идемпотентности адаптера, не обещание поддержки скрытых кликов сайтом.
2. `test_ad_overlay_does_not_dismiss`: клик оверлея не закрывает рекламу.
3. `test_closed_ad_does_not_intercept_click`: скрытый баннер не перекрывает заголовок, реальный клик проходит.

Внешние рекламные объявления, тексты, сети и переходы не проверяются. Ожидание появления занимает около пяти секунд, EXPLICIT_WAIT должен быть больше этой задержки.

### Message — /form-fields/

`test_message_field_is_filled_from_automation_tools`:
1. Открыть настраиваемый MESSAGE_FORM_URL.
2. Selenium находит `li` списка после подписи Automation tools внутри feedbackForm.
3. Получить `.text` каждого элемента, нормализовать пробелы, удалить пустые элементы и дубли с сохранением порядка.
4. Соединить через `, `.
5. Заполнить настоящее поле `[data-testid="message"]`.
6. Проверить точное значение и приложить скриншот.

**Список инструментов не захардкожен. Форма не отправляется.** При отсутствии раздела Selenium завершает тест ошибкой поиска; при пустом списке сообщение ошибки объясняет проблему.

## Допущения и места, требующие уточнения

Страницы реально открывались Selenium Chrome на Windows, DOM исследован. Локаторы не выдуманы. Однако публичный сайт может меняться независимо от проекта.

- Календарь — Jetpack date picker с `.dp`, `.dp-next`, `.dp-prev`, `.dp-day`, не jQuery UI. В компоненте есть короткая внутренняя блокировка открытия после закрытия; повторное открытие ожидается через безопасный ArrowDown, без sleep и без подмены DOM.
- Поле календаря необязательное. Нет сценария «пустая обязательная дата».
- Отдельной кнопки Today в исследованном интерфейсе нет: выбирается выделенный сегодняшний день в сетке. Не выдуманы отдельные кнопки очистки и подтверждения.
- Даты около текущего месяца доступны. Сценарий запрещённой даты не добавлен без подтверждённого требования о диапазоне.
- Модальные окна — DOM Popup Maker. У простой модалки отключены Escape/overlay close, у формы включён Escape. Дополнительной кнопки Cancel/Save, подтверждения несохранённых данных и отдельной кнопки закрытия помимо крестика нет.
- У пустого Name нативная required-валидация надёжнее предположения об aria-invalid после blur. Проверяется реальный ValidityState браузера.
- У рекламы контролируемая модалка `#pum-1272`, не внешний iframe; смена объявлений не реализована, такой тест не придуман.
- Успешная отправка контактной формы не тестируется: набор не создаёт реальные обращения на публичном сайте. Кнопки Submit не нажимаются. При разрешении владельца сайта этот сценарий следует запускать на отдельном стенде.
- Общая база поддерживает iframe, новые окна, нативные alert/confirm/prompt; компонент Dialog выбирает DOM/нативный тип по фактическому состоянию. Нативные диалоги на этих страницах не наблюдались, поэтому не объявляются проверенными отдельным UI-прогоном.

## Что проверить вручную после клонирования проекта

1. Chrome/Firefox запускается; Selenium Manager доступен через вашу сеть/прокси.
2. На `/calendars/` существует `#g1065-1-selectorenteradate`, после открытия — `.dp`, стрелки `.dp-next/.dp-prev`, дни `.dp-day`.
3. На `/modals/` есть `#simpleModal`, `#formModal`, окна `#pum-1318`, `#pum-674`; поля внутри формы доступны через `input.name`, `input.email`, `textarea[id]`.
4. На `/ads/` баннер `#pum-1272` появляется без блокировщиков, крестик `.pum-close` доступен.
5. На `/form-fields/` есть `#feedbackForm`, подпись `Automation tools`, следующий за ней `ul/li`, поле `[data-testid="message"]`.
6. При изменении сайта правьте локаторы только в pages/components, а не тестах. Текстовая привязка подписи списка нужна, поскольку у списка нет устойчивого id.
7. Отдельно выполните Firefox-прогон, если сдаёте кроссбраузерный результат.

## Фактическая проверка реализации

23 октября 2026 года, Windows, Python 3.12.9, Chrome headless:

- Финальный полный прогон: **38 passed за 168,23 секунды**, без skipped/xfail.
- Команда: `..\.venv\Scripts\python.exe -m pytest --headless --alluredir=allure-results/verified-final --junitxml=reports/junit-final.xml`.
- JUnit: `reports/junit-final.xml`.
- Allure: `allure-results/verified-final/`.
- Скриншот заполненного Message: `reports/message-filled.png`, визуально просмотрен.
- `scripts/check_artifacts.py` подтвердил feature/story/severity и шаги финальных тестов, а также PNG/HTML-вложения трёх ошибок первоначального прогона. Первоначальные ошибки исправлены; исторические результаты сохранены в отдельной папке `full-run`, не смешаны с финальными.
- Компиляция модулей через `compileall` завершилась успешно.
- Allure CLI не найден в PATH: HTML-отчёт не открывался. Firefox, нативные диалоги и режим с видимым окном не проверялись.

## Известные ограничения и проверка перед отправкой

- Успешный прогон на одном браузере не гарантирует работу будущих версий сайта.
- Firefox и режим с видимым окном поддержаны настройками, но их результат нельзя считать проверенным по headless Chrome.
- Allure JSON создаётся плагином; просмотр HTML требует отдельно установленного CLI.
- Нет проверок консоли/внешних сетевых запросов: они не входят в текущие утверждения о результате.
- Встроенные данные формы и скриншоты доступны локально в игнорируемых папках; перед публикацией проверьте отсутствие чувствительных данных.

Чек-лист сдачи:
- [ ] Установить зависимости в Python 3.12+.
- [ ] Проверить .env и доступ в сеть.
- [ ] Выполнить полный прогон в новую папку Allure.
- [ ] Убедиться в отсутствии failed/broken/неожиданных skipped.
- [ ] Открыть Allure, проверить русские названия и шаги.
- [ ] Проверить скриншот заполненного Message.
- [ ] Не добавлять .env, виртуальное окружение и диагностический DOM в Git.
- [ ] При необходимости проверить Firefox.
- [ ] Публиковать репозиторий только после отдельного решения пользователя.
