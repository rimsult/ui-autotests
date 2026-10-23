"""Запуск Pytest с явным выбором браузера без изменения .env."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main() -> int:
    """Передать браузер дочернему процессу и вернуть код результата Pytest."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', choices=('chrome', 'firefox'), default='chrome')
    parser.add_argument('--run-name', default='cli-check')
    args = parser.parse_args()
    if not args.run_name.replace('-', '').replace('_', '').isalnum():
        parser.error('Имя прогона должно содержать только буквы, цифры, дефисы и подчёркивания')
    root = Path(__file__).resolve().parents[1]
    results = root / 'allure-results' / args.run_name
    if results.exists():
        parser.error('Папка результатов уже существует; выберите новое имя прогона')
    environment = os.environ.copy()
    environment.update(BROWSER=args.browser, HEADLESS='true', PYTHONIOENCODING='utf-8')
    return subprocess.call(
        [sys.executable, '-m', 'pytest', '--headless',
         f'--alluredir=allure-results/{args.run_name}',
         f'--junitxml=reports/junit-{args.run_name}.xml'],
        cwd=root, env=environment,
    )


if __name__ == '__main__':
    raise SystemExit(main())
