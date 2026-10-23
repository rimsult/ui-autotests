"""Сохранить настройки и поведение рекламного окна для проверки сценариев."""
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from config.settings import Settings
from pages.ads_page import AdsPage


def main() -> None:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    try:
        driver.set_window_size(1920, 1080)
        page = AdsPage(driver, Settings.from_env()).open()
        banner = page.banner
        root = page.find(banner.root)
        print('ATTRIBUTES', root.get_attribute('outerHTML')[:1800])
        banner.wait_open()
        print('RECT', root.rect)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        print('ESCAPE_VISIBLE', banner.visible())
        driver.save_screenshot(str(Path('reports/ad-behavior.png')))
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
