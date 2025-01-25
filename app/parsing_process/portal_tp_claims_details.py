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
from selenium.common.exceptions import StaleElementReferenceException
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
PARSING_DELAY: int = 5
PARSING_TIMER: int = 30


def bad_response(login: str, url_detail: str) -> bool:
    print(
        Fore.RED + Style.DIM +
        'Проверьте ссылку в ' +
        Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
        str(portal_tp_claims_details.__name__) +
        f' ({login})' +
        Style.RESET_ALL + Fore.RED + Style.DIM +
        ' — ' +
        Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
        url_detail
    )
    return True


def claim_address_variant_1(wait_elements: WebDriverWait) -> str | None:
    """Парсинг адреса по описанию местоположения."""
    try:
        address = wait_elements.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//textarea[@data-p-label='Описание местоположения']"
                )
            )
        ).get_attribute("innerHTML")

        for substring in ['не указано', '...', 'on', '-']:
            address = address.replace(substring, '')

        return address.strip()
    except (TimeoutException, StaleElementReferenceException):
        return None


def claim_address_variant_2(wait_elements: WebDriverWait) -> str | None:
    """Парсинг адреса для точного указания местоположения."""
    try:
        claim_address_panel = wait_elements.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='ui-panel ui-widget ui-widget-content " +
                    "ui-corner-all panelgroup-as-accordion' " +
                    "and .//span[text()='Местоположение объекта']]" +
                    " | //*[contains(@id, " +
                    "'sMw_DeviceAddrRegionRef:group')][1]" +
                    " | //*[contains(@id, 'sMw_Address_object:group')][1]" +
                    " | //*[contains(@id, 'sMw_DeviceAddrIndex:group')][1]"
                )
            )
        )

        claim_address_rows = claim_address_panel.find_elements(
            By.XPATH, ".//input"
        ) + claim_address_panel.find_elements(
            By.XPATH, ".//select"
        )

        address_parts = []

        for row in claim_address_rows:
            key: str | None = row.get_attribute('data-p-label')

            if row.tag_name == 'input':
                value = row.get_attribute('value').strip() or row.text.strip()

            else:
                options = row.find_elements(By.TAG_NAME, 'option')
                selected_values = [
                    option.get_attribute(
                        "innerHTML"
                    ) for option in options if option.is_selected()
                ]
                value = next((val for val in selected_values if val), None)

            if key and 'адреса вручную' in key:
                continue

            if not value or value.lower() in (
                'не указано', '...', 'on', '-', 'нет'
            ) or (
                value.count('-') > 3
            ):
                continue

            address_parts.append(value)

        return ', '.join(address_parts)

    except (TimeoutException, StaleElementReferenceException):
        return None


def portal_tp_claims_details(
    login: str, password: str,
    personal_area_id: int, declarant_id: int, *args
) -> DataFrame:
    CLAIMS = DataFrame(columns=CLAIMS_COLUMNS)
    claims_numbers_urls: List[Tuple[str, str]] = sql_queries(
        select_claims_details_urls(personal_area_id, declarant_id, 1100)
    )

    driver = webdriver.Chrome()
    driver.maximize_window()
    find_bad_link: bool = True

    for claim_number_url in claims_numbers_urls:
        wait = WebDriverWait(driver, PARSING_TIMER)
        wait_elements = WebDriverWait(driver, PARSING_DELAY)
        claim_number: str = claim_number_url[0]
        url: str = claim_number_url[1]
        url_detail: str = (
            url.replace('accessionCard?', 'publicAccessionCard?') +
            '&formCode=ApplDetails'
        ).replace('requestStages?', 'publicAccessionCard?')

        driver.get(url_detail)

        if find_bad_link:
            find_bad_link = False
            authorize_form(
                wait, login, password,
                "//input[@id='workplaceTopForm:j_mail_login']",
                "//input[@id='workplaceTopForm:j_password']",
                "//button[@id='workplaceTopForm:loginBtn']"
            )

        claim_address_1 = claim_address_variant_1(wait_elements)
        claim_address_2 = claim_address_variant_2(wait_elements)
        if not claim_address_1 and not claim_address_2:
            find_bad_link = bad_response(login, url_detail)
            driver.quit()
            driver = webdriver.Chrome()
            driver.maximize_window()
            continue

        if claim_address_1 is None:
            claim_address = claim_address_2
        elif claim_address_2 is None:
            claim_address = claim_address_1
        else:
            claim_address = (
                f'{claim_address_2}.\nОписание местоположения: ' +
                f'{claim_address_1}.'
            )

        parsing_data = datetime.now()
        new_row = {
            'parsing_data': parsing_data,
            'claim_number': claim_number,
            'claim_address': claim_address,
        }

        CLAIMS.loc[len(CLAIMS)] = new_row

    driver.quit()

    return CLAIMS
