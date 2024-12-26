import os
import sys
import time
from datetime import datetime, date

from pandas import DataFrame
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


def rosseti_mr_claims(login: str, password: str, *args) -> DataFrame:
    driver = webdriver.Chrome()
    driver.get('https://lk.rossetimr.ru/claims')
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)

    authorize_form(
        wait, login, password,
        "//*[@id='user_email']",
        "//*[@id='password-input']",
        "//button[span[text()='Войти']]"
    )

    wait.until(
        lambda browser: browser.execute_script(
            'return document.readyState'
        ) == 'complete'
    )
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@class, 'custom-combobox-toggle')]")
        )
    ).click()
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//li[contains(text(), '100')]")
        )
    ).click()

    def take_data_from_page() -> date:
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
        time.sleep(PARSING_DELAY)
        rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr"))
        )
        min_claim_date = date.today()
        for row in rows:
            try:
                cells = row.find_elements(By.XPATH, ".//td")
                parsing_data = datetime.now()
                claim_number: str = cells[4].text.strip()
                claim_status = cells[3].text.strip()
                claim_link = (
                    f'https://lk.rossetimr.ru/{row.get_attribute("href")}'
                )
                claim_date: str = cells[1].text.strip()
                claim_date: date = (
                    datetime.strptime(claim_date, '%d.%m.%Y').date()
                )
                claim_address: str = cells[7].text.split('\n')[0].strip()
                claim_inner_number: str = (
                    claim_link.split('?page')[0].split('claims/')[1].strip()
                )
                claim_number = claim_number if claim_number != '' else (
                    f'внутренний номер {claim_inner_number}'
                )

                new_row = {
                    'parsing_data': parsing_data,
                    'claim_number': claim_number,
                    'claim_status': claim_status,
                    'claim_link': claim_link,
                    'claim_date': claim_date,
                    'claim_address': claim_address,
                    'claim_inner_number': claim_inner_number
                }

                CLAIMS.loc[len(CLAIMS)] = new_row

                min_claim_date = min(claim_date, min_claim_date)

            except StaleElementReferenceException:
                continue

        return min_claim_date

    last_page: bool = False
    while not last_page:
        try:
            # if take_data_from_page() < date.today() - timedelta(days=365):
            #     break
            take_data_from_page()
            WebDriverWait(driver, PARSING_DELAY).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//a[contains(@class, 'paging_link_next link')]"
                    )
                )
            ).click()

        except TimeoutException:
            last_page = True

    driver.quit()

    return CLAIMS
