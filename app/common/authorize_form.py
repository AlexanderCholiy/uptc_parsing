import time
import random

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def type_with_delay(element: WebElement, text, delay=0.1):
    """Ввод текста с задержкой."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(delay - 0.05, delay + 0.05))


def authorize_form(
    wait: WebDriverWait, login: str, password: str,
    login_field_selector: str, password_field_selector: str,
    enter_button_selector: str
):
    """Авторизация на сайте."""
    login_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, login_field_selector))
    )
    login_field.clear()
    type_with_delay(login_field, login)

    password_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, password_field_selector))
    )
    password_field.clear()
    type_with_delay(password_field, password)

    time.sleep(1)

    wait.until(
        EC.element_to_be_clickable((By.XPATH, enter_button_selector))
    ).click()
