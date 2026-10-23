"""Вывод разметки календаря и результатов локальной валидации."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.page_load_strategy = 'eager'
with webdriver.Chrome(options=options) as d:
    d.get('https://practice-automation.com/calendars/')
    w = WebDriverWait(d, 20)
    field = w.until(lambda x: x.find_element(By.CSS_SELECTOR, 'input.date'))
    field.click()
    w.until(lambda x: x.find_element(By.CSS_SELECTOR, '.dp').is_displayed())
    print('PICKER', ascii(d.find_element(By.CSS_SELECTOR, '.dp').get_attribute('outerHTML')))
    print('SHADOW', ascii(d.execute_script("return Array.from(document.querySelectorAll('*')).filter(e=>e.shadowRoot).map(e=>({tag:e.tagName, html:e.shadowRoot.innerHTML}));")))
    print('IFRAMES', ascii([e.get_attribute('outerHTML') for e in d.find_elements(By.TAG_NAME, 'iframe')]))
    print('FIELD_PARENT', ascii(field.find_element(By.XPATH, '..').get_attribute('outerHTML')[:22000]))
    for value in ('not-a-date', '2024-02-31', '2024-13-01', '2024-02-29'):
        field.clear()
        field.send_keys(value, Keys.TAB)
        print(value, ascii(field.get_attribute('outerHTML')), ascii(d.find_element(By.CSS_SELECTOR, 'main').text[-800:]))
