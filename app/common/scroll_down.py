import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def scroll_down(driver: webdriver.Chrome, delay: int = 10) -> bool:
    """
    Прокручивает страницу вниз.

    Returns:
    -------
    True  - была выполнена прокрутка и потенциально есть ещё контент.
    False - достигнут конец страницы.
    """

    old_position = driver.execute_script("return window.pageYOffset;")

    # Выполняем скролл
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(delay)

    new_position = driver.execute_script("return window.pageYOffset;")

    # Если позиция не изменилась, значит достигли конца страницы
    return new_position > old_position
