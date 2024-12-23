import os
import sys
import re
from datetime import datetime, date

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.models.parsing_model import CLAIMS  # noqa: E402
from app.common.authorize_form import authorize_form  # noqa: E402

PARSING_DELAY: int = 5
PARSING_TIMER: int = 120


def rzd_claims(login: str, password: str):
    driver = webdriver.Chrome()
    driver.get('https://lk.energopromsbyt.ru/personal/')
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)

    # Иногда загружается не стандартая версия сайта, поэтому после регестрации
    # стоит сделать перезагрузку страницы:
    driver.refresh()

    authorize_form(
        wait, login, password,
        "//*[@id='form-text-email']",
        "//*[@id='form-text-pswd']",
        "//button[span[text()='Войти']]"
    )

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@href='/?logout=yes']"))
    )

    list_claims_data = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//td[@style='text-align:left;" +
                "border-bottom:2px solid silver;']"
            )
        )
    )

    for i in range(len(list_claims_data)):
        text = list_claims_data[i].text
        claim_number = re.search(r'№ заявки:\s*(\d+ \w)', text)
        if claim_number:
            parsing_data: datetime = datetime.now()
            claim_number: str = claim_number.group(1)
            claim_status: str = re.search(
                r'Этап рассмотрения:\s*(\S.*?)\s*Дата', text
            ).group(1)
            claim_status_date = re.search(
                r'Дата этапа:\s*(\d{2}\.\d{2}\.\d{4})', text
            )
            if claim_status_date:
                claim_status_date: str = claim_status_date.group(1)
                claim_status_date: date = datetime.strptime(
                    claim_status_date, '%d.%m.%Y'
                ).date()
            else:
                claim_status_date = None

            new_row = {
                'parsing_data': parsing_data,
                'claim_number': claim_number,
                'claim_status': claim_status,
                'claim_status_date': claim_status_date,
            }

            CLAIMS.loc[len(CLAIMS)] = new_row

    driver.quit()

    return CLAIMS
