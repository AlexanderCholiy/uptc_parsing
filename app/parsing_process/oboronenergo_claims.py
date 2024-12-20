import os
import sys
from datetime import datetime, date

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, StaleElementReferenceException
)
from selenium.webdriver.common.by import By

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.models.parsing_model import CLAIMS  # noqa: E402
from app.common.authorize_form import authorize_form  # noqa: E402

PARSING_DELAY: int = 5
PARSING_TIMER: int = 120


def oboronenergo_claims(login: str, password: str):
    driver = webdriver.Chrome()
    driver.get('https://oboronenergo.su/my/service/cabinet/bid/')
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)

    authorize_form(
        wait, login, password,
        '//input[@class="bx-auth-input" and @name="USER_LOGIN"]',
        '//input[@class="bx-auth-input" and @name="USER_PASSWORD"]',
        (
            "//td[@class='authorize-submit-cell even']/input[@type='submit' " +
            "and @name='Login' and @value='Войти']"
        )
    )

    def take_data_from_page():
        # Ожидание полной загрузки страницы:
        wait.until(
            lambda browser: browser.execute_script(
                'return document.readyState'
            ) == 'complete'
        )
        wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='overlay']//div[contains(@class, " +
                    "'spinner-loading')]"
                )
            )
        )
        rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr"))
        )
        for row in rows:
            try:
                cells = row.find_elements(By.XPATH, ".//td")

                if len(cells) < 7:
                    continue

                parsing_data: datetime = datetime.now()
                claim_number: str = cells[0].text.strip()
                claim_status: str = (
                    cells[5]
                    .text.strip("()").replace("'", "").split(",")[0].strip()
                )
                claim_date: str = (
                    cells[1]
                    .text.strip("()").replace("'", "").split(",")[0].strip()
                )
                claim_date: date = datetime.strptime(
                    claim_date, '%d.%m.%Y %H:%M'
                ).date()
                claim_response = cells[6].text.strip()

                new_row = {
                    'parsing_data': parsing_data,
                    'claim_number': claim_number,
                    'claim_status': claim_status,
                    'claim_date': claim_date,
                    'claim_response': claim_response,
                }

                CLAIMS.loc[len(CLAIMS)] = new_row

            except StaleElementReferenceException:
                continue

    for _ in range(100):
        try:
            take_data_from_page()
            element = WebDriverWait(driver, PARSING_DELAY).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='paginator']//a[@class='arrow']")
                )
            )
            element.click()
        except TimeoutException:
            break

    driver.quit()

    return CLAIMS
