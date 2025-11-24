import os
import sys
from datetime import datetime
from typing import List, Tuple

from colorama import Fore, Style, init
from pandas import DataFrame
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.common.authorize_form import authorize_form  # noqa: E402
from app.models.parsing_model import MESSAGES_COLUMNS  # noqa: E402
from database.db_conn import sql_queries  # noqa: E402
from database.requests.select_messages_details_urls import \
    select_messages_details_urls  # noqa: E402

init(autoreset=True)
PARSING_DELAY: int = 5
PARSING_TIMER: int = 30


def portal_tp_messages_details(
    login: str, password: str,
    personal_area_id: int, declarant_id: int, *args
) -> DataFrame:
    MESSAGES = DataFrame(columns=MESSAGES_COLUMNS)
    messages_numbers_urls: List[Tuple[str, str]] = sql_queries(
        select_messages_details_urls(personal_area_id, declarant_id, 1020)
    )

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)
    find_bad_link: bool = False

    for index, message_number_url in enumerate(messages_numbers_urls):
        message_number: str = message_number_url[0]
        url: str = message_number_url[1]
        url_detail: str = (
            url.replace('requestStages?', 'publicAccessionCard?') +
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
            message_filial = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//span[@class='ui-autocomplete " +
                        "dataObjectControllerInstanceFields__Filial__" +
                        "Value_reference_input']//input[@type='text']"
                    )
                )
            ).get_attribute('value')
            find_bad_link = False
        except TimeoutException:
            # Бывают не рабоче ссылки, которые не загружаются. Скорее всего
            # где-то были внесены некорректные обращения с неправильным
            # declarant_id или personal_area_id...
            print(
                Fore.RED + Style.DIM +
                'Проверьте ссылку в ' +
                Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                str(portal_tp_messages_details.__name__) + f' ({login})' +
                Style.RESET_ALL + Fore.RED + Style.DIM +
                ' — ' +
                Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                url_detail
            )
            find_bad_link = True
            driver.quit()
            driver = webdriver.Chrome()
            driver.maximize_window()
            wait = WebDriverWait(driver, PARSING_TIMER)
            continue

        message_grid = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//span[@class='ui-autocomplete " +
                    "dataObjectControllerInstanceFields__DZO__" +
                    "Value_reference_input']//input[@type='text']"
                )
            )
        ).get_attribute('value')

        try:
            message_text = WebDriverWait(driver, PARSING_DELAY).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//textarea[contains(@id, " +
                        "'wp:dataObjectControllerInstance_sections:" +
                        "sMw_ClaimAnswers:pMw_ClaimAnswers:" +
                        "dataObjectController" +
                        "InstanceFields__ClaimAnswers__Value_0_:" +
                        "dataObjectControllerInstanceFields__ClaimAnswers" +
                        "__Value_0_Fields__Comment__Value')]"
                    )
                )
            ).get_attribute('title')
        except TimeoutException:
            message_text = None

        parsing_data = datetime.now()
        new_row = {
            'parsing_data': parsing_data,
            'message_number': message_number,
            'message_grid': message_grid,
            'message_filial': message_filial,
            'message_text': message_text,
        }

        MESSAGES.loc[len(MESSAGES)] = new_row

    driver.quit()

    return MESSAGES
