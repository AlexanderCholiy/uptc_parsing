import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def scroll_down(driver:  webdriver.Chrome, delay: int = 5):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(delay)
