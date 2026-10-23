"""Проверяемые настройки окружения для независимых запусков."""
import os
from math import isfinite
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env', override=False)


def boolean(name: str, default: str) -> bool:
    """Отклонить опечатку вместо незаметного изменения режима запуска."""
    value = os.getenv(name, default).lower()
    if value not in {'true', 'false'}:
        raise ValueError(f'{name}: ожидается true или false, получено {value!r}')
    return value == 'true'


@dataclass(frozen=True)
class Settings:
    """Параметры браузера и адреса тестируемого сайта."""
    base_url: str
    browser: str
    headless: bool
    explicit_wait: float
    window_width: int
    window_height: int
    message_form_url: str

    @classmethod
    def from_env(cls) -> 'Settings':
        """Загрузить и проверить параметры перед запуском браузера."""
        base = os.getenv('BASE_URL', 'https://practice-automation.com').rstrip('/')
        message = os.getenv('MESSAGE_FORM_URL', base + '/form-fields/')
        for url in (base, message):
            if urlparse(url).scheme not in {'https', 'http'} or not urlparse(url).netloc:
                raise ValueError(f'Некорректный URL: {url!r}')
        settings = cls(base, os.getenv('BROWSER', 'chrome').lower(), boolean('HEADLESS', 'false'),
                       float(os.getenv('EXPLICIT_WAIT', '10')), int(os.getenv('WINDOW_WIDTH', '1920')),
                       int(os.getenv('WINDOW_HEIGHT', '1080')), message)
        if settings.browser not in {'chrome', 'firefox'}:
            raise ValueError('BROWSER должен быть chrome или firefox')
        if not isfinite(settings.explicit_wait):
            raise ValueError('EXPLICIT_WAIT должен быть конечным положительным числом')
        if min(settings.explicit_wait, settings.window_width, settings.window_height) <= 0:
            raise ValueError('Ожидание и размеры окна должны быть положительными')
        return settings
