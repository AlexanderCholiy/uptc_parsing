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
from app.models.parsing_model import MESSAGES_COLUMNS  # noqa: E402

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


def portal_tp_messages(login: str, password: str, *args) -> DataFrame:
    MESSAGES = DataFrame(columns=MESSAGES_COLUMNS)
    driver = webdriver.Chrome()
    driver.get(
        'https://xn----7sb7akeedqd.xn--p1ai/platform/portal/' +
        'tehprisEE_listEvent'
    )
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)

    portal_tp_logger.debug('Запуск сбора обращений')

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
                    "//li[@role='tab' and @data-index='2']"
                    "/a[normalize-space()='Обращения']"
                )
            )
        )
    ).click()

    portal_tp_logger.debug('Попали на страницу со списком обращений')

    messages_ids = set()

    def messages_elements(
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
        count_messages_ids = len(messages_ids)

        messages_links = messages_elements(
            BASE_SELECTOR +
            "//div[@class='listEvent__item-right-section']" +
            "//a[@class='ui-link ui-widget " +
            "listEvent__item-message__details']"
        )
        portal_tp_logger.debug(f'Получили список ссылок ({scroll_number})')

        messages_statuses = messages_elements(
            BASE_SELECTOR +
            "//div[contains(@class, 'listEvent__item-status')]"
        )
        portal_tp_logger.debug(f'Получили список статусов ({scroll_number})')

        messages_subjects = messages_elements(
            BASE_SELECTOR +
            "//div[contains(@class, 'listEvent__item-nameEntity')]"
        )
        portal_tp_logger.debug(f'Получили список названий ({scroll_number})')

        messages_numbers = messages_elements(
            BASE_SELECTOR +
            "//div[contains(@class, 'listEvent__item-number')]"
        )
        portal_tp_logger.debug(
            f'Получили список номеров обращений ({scroll_number})'
        )

        messages_dates = messages_elements(
            BASE_SELECTOR +
            "//div[contains(@class, 'listEvent__item-date')]"
        )
        portal_tp_logger.debug(
            f'Получили список дат обращений ({scroll_number})'
        )

        for message_index in range(len(messages_links)):
            try:
                message_link = messages_links[message_index].get_attribute(
                    'href'
                )

                if message_link not in messages_ids:
                    messages_ids.add(message_link)
                    parsing_data: datetime = datetime.now()
                    message_number: str = (
                        messages_numbers[message_index].text.replace('№', '').
                        strip()
                    )
                    message_number = message_number.replace('№', '').strip()
                    message_status: str = (
                        messages_statuses[message_index].text
                    )
                    message_subject: str = (
                        messages_subjects[message_index].text
                    )
                    message_date_str: str = messages_dates[message_index].text

                    day, month_str, year = message_date_str.split()
                    month: str = MONTHS[month_str]
                    message_date: date = date(
                        int(year), month, int(day)
                    )

                    new_row = {
                        'parsing_data': parsing_data,
                        'message_number': message_number,
                        'message_status': message_status,
                        'message_subject': message_subject,
                        'message_link': message_link,
                        'message_date': message_date,
                    }

            except IndexError:
                break

            else:
                MESSAGES.loc[len(MESSAGES)] = new_row

        check_end_page: bool = scroll_down(driver)

        if (
            len(MESSAGES) == 0 or len(messages_ids) == count_messages_ids
        ) and not check_end_page:
            break
        else:
            scroll_number += 1

    portal_tp_logger.info(f'Найдено {len(MESSAGES)} обращений.')

    driver.quit()

    portal_tp_logger.debug('Вышли из браузер')

    return MESSAGES
