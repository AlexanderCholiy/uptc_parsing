import os
import sys
from datetime import datetime
from typing import Tuple, List

from pandas import DataFrame
from colorama import init, Fore, Style
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from database.db_conn import sql_queries  # noqa: E402
from database.requests.select_claims_details_urls import (  # noqa: E402
    select_claims_details_urls
)
from app.models.parsing_model import CLAIMS_COLUMNS  # noqa: E402
from app.common.authorize_form import authorize_form  # noqa: E402


init(autoreset=True)
PARSING_DELAY: int = 3
PARSING_TIMER: int = 10


def portal_tp_claims_details(
    login: str, password: str,
    personal_area_id: int, declarant_id: int, *args
) -> DataFrame:
    CLAIMS = DataFrame(columns=CLAIMS_COLUMNS)
    claims_numbers_urls: List[Tuple[str, str]] = sql_queries(
        select_claims_details_urls(personal_area_id, declarant_id)
    )
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)
    wait_elements = WebDriverWait(driver, PARSING_DELAY)
    find_bad_link: bool = False

    for index, claim_number_url in enumerate(claims_numbers_urls):
        claim_number: str = claim_number_url[0]
        url: str = claim_number_url[1]
        url_detail: str = (
            url.replace('accessionCard?', 'publicAccessionCard?') +
            '&formCode=ApplDetails'
        )

        driver.get(url_detail)

        if index == 0 or find_bad_link:
            authorize_form(
                wait, login, password,
                "//input[@id='workplaceTopForm:j_mail_login']",
                "//input[@id='workplaceTopForm:j_password']",
                "//button[@id='workplaceTopForm:loginBtn']"
            )

        try:
            claim_address = wait_elements.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//textarea[@data-p-label='Описание местоположения']"
                    )
                )
            ).get_attribute("innerHTML")
            if claim_address == '...':
                continue
            find_bad_link = False
        except TimeoutException:
            # Бывают не рабоче ссылки, которые не загружаются. Скорее всего
            # где-то были внесены некорректные заявки с неправильным
            # declarant_id или personal_area_id...
            # Бывает 2 различных варианта полей для местоположения.
            try:
                claim_address_panel = wait_elements.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//div[@class='ui-panel ui-widget " +
                            "ui-widget-content ui-corner-all " +
                            "panelgroup-as-accordion' and " +
                            ".//span[text()='Местоположение объекта']]"
                        )
                    )
                )
                claim_address_rows = claim_address_panel.find_elements(
                    By.XPATH, ".//input"
                )
                address_tuples: list[tuple[str]] = [
                    (
                        row.get_attribute('data-p-label'),
                        row.get_attribute('value')
                    ) for row in claim_address_rows if row.get_attribute(
                        'data-p-label'
                    ) and 'адреса вручную' not in row.get_attribute(
                        'data-p-label'
                    )
                    and row.get_attribute('value') and row.get_attribute(
                        'value'
                    ) not in ('не указано', '...')
                ]
                address_parts = [
                    f'{key}: {value}' for key, value in address_tuples if value
                ]
                claim_address = '. '.join(address_parts) + '.'
                claim_address = str(claim_address)
                find_bad_link = False
            except TimeoutException:
                print(
                    Fore.RED + Style.DIM +
                    'Проверьте ссылку в ' +
                    Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                    str(portal_tp_claims_details.__name__) + f' ({login})' +
                    Style.RESET_ALL + Fore.RED + Style.DIM +
                    ' — ' +
                    Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                    url_detail
                )
                find_bad_link = True
                driver.quit()
                driver = webdriver.Chrome()
                driver.maximize_window()
                continue

        parsing_data = datetime.now()
        new_row = {
            'parsing_data': parsing_data,
            'claim_number': claim_number,
            'claim_address': claim_address,
        }

        CLAIMS.loc[len(CLAIMS)] = new_row

    driver.quit()

    return CLAIMS
