import os
import sys
from datetime import date, datetime

from pandas import DataFrame
from selenium import webdriver
from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.common.authorize_form import authorize_form  # noqa: E402
from app.models.parsing_model import CLAIMS_COLUMNS  # noqa: E402

PARSING_DELAY: int = 5
PARSING_TIMER: int = 120


def oboronenergo_claims(login: str, password: str, *args) -> DataFrame:
    CLAIMS = DataFrame(columns=CLAIMS_COLUMNS)
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

    not_last_page: bool = True
    while not_last_page:
        try:
            take_data_from_page()
            element = WebDriverWait(driver, PARSING_DELAY).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='paginator']//a[@class='arrow']")
                )
            )
            element.click()
        except TimeoutException:
            not_last_page: bool = False

    driver.quit()

    return CLAIMS
