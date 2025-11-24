import os
import sys
from datetime import date, datetime

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from app.common.logger import portal_tp_logger

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.common.authorize_form import authorize_form  # noqa: E402
from app.common.scroll_down import scroll_down  # noqa: E402
from app.models.parsing_model import CLAIMS_COLUMNS  # noqa: E402

PARSING_TIMER: int = 180
MONTHS: dict = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}
BASE_SELECTOR: str = "//li[@class='ui-datascroller-item']"


def portal_tp_claims(login: str, password: str, *args) -> DataFrame:
    CLAIMS = DataFrame(columns=CLAIMS_COLUMNS)
    driver = webdriver.Chrome()
    driver.get(
        'https://xn----7sb7akeedqd.xn--p1ai/platform/portal/' +
        'tehprisEE_listEvent'
    )
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)

    portal_tp_logger.debug('Запуск сбора заявок')

    authorize_form(
        wait, login, password,
        "//input[@id='workplaceTopForm:j_mail_login']",
        "//input[@id='workplaceTopForm:j_password']",
        "//button[@id='workplaceTopForm:loginBtn']"
    )

    portal_tp_logger.debug('Прошли авторизацию')

    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                (
                    "//li[@role='tab' and @data-index='1']"
                    "/a[normalize-space()='Заявки']"
                )
            )
        )
    ).click()

    portal_tp_logger.debug('Попали на страницу со списком заявок')

    claims_ids = set()

    def claims_elements(
        xpath_selector, display_filter: bool = True
    ) -> list[WebElement]:
        elements: list[WebElement] = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath_selector))
        )
        if display_filter:
            elements: list[WebElement] = [
                i for i in elements if i.is_displayed()
            ]
        return elements

    scroll_down(driver)

    scroll_number = 1

    while True:
        count_claims_ids = len(claims_ids)

        claims_links = claims_elements(
            BASE_SELECTOR +
            "//div[@class='listEvent__item-right-section']" +
            "//a[@class='ui-link ui-widget " +
            "listEvent__item-message__details']"
        )
        portal_tp_logger.debug(f'Получили список ссылок ({scroll_number})')

        claims_statuses = claims_elements(
            BASE_SELECTOR +
            "//div[contains(@class, 'listEvent__item-status')]"
        )
        portal_tp_logger.debug(
            f'Получили список статусов ({scroll_number})'
        )

        claims_numbers = claims_elements(
            BASE_SELECTOR +
            "//div[contains(@class, 'listEvent__item-number')]"
        )
        portal_tp_logger.debug(
            f'Получили список номеров заявок ({scroll_number})'
        )

        claims_dates = claims_elements(
            BASE_SELECTOR +
            "//div[contains(@class, 'listEvent__item-date')]"
        )
        portal_tp_logger.debug(
            f'Получили список дат заявок ({scroll_number})'
        )

        for claim_index in range(len(claims_links)):
            try:
                claim_link = claims_links[claim_index].get_attribute('href')

                if claim_link not in claims_ids:
                    claims_ids.add(claim_link)
                    parsing_data: datetime = datetime.now()
                    claim_number: str = (
                        claims_numbers[claim_index].text.replace('№', '').
                        strip()
                    )
                    claim_status: str = claims_statuses[claim_index].text
                    claim_date_str: str = claims_dates[claim_index].text

                    day, month_str, year = claim_date_str.split()
                    month: str = MONTHS[month_str]
                    claim_date: date = date(
                        int(year), month, int(day)
                    )

                    new_row = {
                        'parsing_data': parsing_data,
                        'claim_number': claim_number,
                        'claim_status': claim_status,
                        'claim_date': claim_date,
                        'claim_link': claim_link,
                    }

            except IndexError:
                break

            else:
                CLAIMS.loc[len(CLAIMS)] = new_row

        check_end_page: bool = scroll_down(driver)

        if (
            len(CLAIMS) == 0 or len(claims_ids) == count_claims_ids
        ) and not check_end_page:
            break
        else:
            scroll_number += 1

    portal_tp_logger.info(f'Найдено {len(CLAIMS)} заявок.')

    driver.quit()

    portal_tp_logger.debug('Вышли из браузер')

    return CLAIMS
