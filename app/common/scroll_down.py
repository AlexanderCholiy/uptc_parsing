import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def scroll_down(driver: webdriver.Chrome, delay: int = 5) -> bool:
    """
    Returns:
    -------
    - True: прокрутка выполнена.
    - False: достигли конца страницы.
    """
    current_scroll_position = driver.execute_script(
        "return window.pageYOffset;"
    )
    window_height = driver.execute_script("return window.innerHeight;")
    document_height = driver.execute_script(
        "return document.body.scrollHeight;"
    )

    if current_scroll_position + window_height < document_height:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(delay)
        current_scroll_position = driver.execute_script(
            "return window.pageYOffset;"
        )
        window_height = driver.execute_script("return window.innerHeight;")
        document_height = driver.execute_script(
            "return document.body.scrollHeight;"
        )
        return True
    else:
        return False
