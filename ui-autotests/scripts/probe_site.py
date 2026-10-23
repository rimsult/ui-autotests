"""Исследование контролируемых элементов сайта без отправки форм."""
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

output = Path(__file__).resolve().parents[1] / 'reports' / 'inspection'
output.mkdir(parents=True, exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--window-size=1920,1080')
options.page_load_strategy = 'eager'
with webdriver.Chrome(options=options) as driver:
    driver.set_page_load_timeout(35)
    for route in ('calendars', 'modals', 'ads', 'form-fields'):
        driver.get(f'https://practice-automation.com/{route}/')
        wait = WebDriverWait(driver, 20)
        wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, 'h1'))
        if route == 'ads':
            wait.until(lambda d: any(e.is_displayed() for e in d.find_elements(By.CSS_SELECTOR, '.pum-overlay')))
        if route == 'calendars':
            driver.find_element(By.CSS_SELECTOR, 'input.date').click()
            print('DATE_STATE', ascii(driver.execute_script("return {html:document.querySelector('input.date').outerHTML, jquery:typeof jQuery, scripts:Array.from(document.scripts).map(s=>s.src).filter(s=>s.includes('date'))}")))
        driver.save_screenshot(str(output / f'{route}-current.png'))
        (output / f'{route}-current.html').write_text(driver.page_source, encoding='utf-8')
        for e in driver.find_elements(By.CSS_SELECTOR, 'h1, input:not([type=hidden]), textarea[id], select, #ui-datepicker-div, .pum-overlay, main button, #feedbackForm, #tools'):
            if e.get_attribute('name') == 'ak_hp_textarea':
                continue
            html = e.get_attribute('outerHTML')
            if 'pum-overlay' in (e.get_attribute('class') or ''):
                html = json.dumps({'id': e.get_attribute('id'), 'visible': e.is_displayed(), 'settings': e.get_attribute('data-popmake')})
            print(route, ascii(html[:6000]))
        if route == 'form-fields':
            print('TOOLS_CONTEXT', ascii(driver.find_element(By.CSS_SELECTOR, 'main').text[-6000:]))
