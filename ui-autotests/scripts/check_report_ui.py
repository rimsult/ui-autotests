"""Проверить интерфейс готового Allure-отчёта через локальный HTTP-сервер."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main() -> None:
    """Открыть Suites, проверить поиск и сохранить скриншот без изменения отчёта."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path, help='Каталог с index.html отчёта')
    args = parser.parse_args()
    report = args.report.resolve()
    if not (report / 'index.html').is_file():
        parser.error('В каталоге нет index.html; сначала сгенерируйте отчёт')
    handler = partial(SimpleHTTPRequestHandler, directory=str(report))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    browser = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        browser = webdriver.Chrome(options=options)
        browser.set_page_load_timeout(45)
        browser.set_window_size(1440, 1000)
        wait = WebDriverWait(browser, 10)
        browser.get(f'http://127.0.0.1:{server.server_port}/')
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#suites"]'))).click()
        wait.until(EC.url_contains('#suites'))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input')))
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[normalize-space(text())="tests"]')))
        screenshot = report.parent / f'{report.name}-suites.png'
        if not browser.save_screenshot(str(screenshot)):
            raise RuntimeError('Не удалось сохранить скриншот отчёта')
        print(f'PASS: Suites открыт, поиск и дерево результатов видимы. Скриншот: {screenshot}')
    finally:
        try:
            if browser is not None:
                browser.quit()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == '__main__':
    main()
