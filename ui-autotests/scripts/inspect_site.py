"""Исследование реального DOM без отправки форм."""
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

root = Path(__file__).resolve().parents[1]
output = root / "reports" / "inspection"
output.mkdir(parents=True, exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1440,1000")
with webdriver.Chrome(options=options) as driver:
    for route in ("calendars", "modals", "ads", "form-fields"):
        driver.get(f"https://practice-automation.com/{route}/")
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        if route == "ads":
            WebDriverWait(driver, 20).until(lambda d: any(e.is_displayed() for e in d.find_elements(By.CSS_SELECTOR, ".pum-overlay")))
        (output / f"{route}.html").write_text(driver.page_source, encoding="utf-8")
        driver.save_screenshot(str(output / f"{route}.png"))
        elements = driver.find_elements(By.CSS_SELECTOR, "input, button, textarea, select, .pum-overlay, .pum-content, .pum-close")
        data = [{"tag": e.tag_name, "id": e.get_attribute("id"), "type": e.get_attribute("type"), "text": e.text, "html": e.get_attribute("outerHTML")[:1800]} for e in elements]
        (output / f"{route}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(route, json.dumps(data, ensure_ascii=True))
