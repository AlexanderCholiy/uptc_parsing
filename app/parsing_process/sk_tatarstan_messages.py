import os
import sys
import time
from datetime import datetime, date

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.models.parsing_model import MESSAGES  # noqa: E402
from app.common.authorize_form import authorize_form  # noqa: E402


PARSING_DELAY: int = 5
PARSING_TIMER: int = 120
PAGE_COUNT: int = 6
MONTHS = {
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
    'декабря': 12
}
BASE_SELECTOR: str = (
    "//div[contains(@class, 'src-components-appeals-appeal-list-appeal-" +
    "list-module__container--rfqtI')]"
)


def sk_tatarstan_messages(login: str, password: str, *args) -> DataFrame:
    driver = webdriver.Chrome()
    driver.get('https://pdo.gridcom-rt.ru/auth')
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)
    authorize_form(
        wait, login, password,
        "//input[@class='src-lib-components-text-input-text-input-" +
        "module__input--T3izK' and @name='UserName']",
        "//input[@class='src-lib-components-text-input-text-input-" +
        "module__input--T3izK src-pages-authorization-page-authorization-" +
        "page-module__passwordInput--_Csh8' and @name='Password']",
        "//button[text()='Войти']"
    )

    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[@href='/appeals']/li[contains(@class, 'src-components-" +
                "common-nav-bar-nav-tab-nav-tab-module__tab--Ayvp6')]"
            )
        )
    ).click()

    def click_next_page(page_num: int) -> bool:
        # Без задержки может не дойти до последней страницы:
        time.sleep(1)
        try:
            page_element: WebElement = (
                WebDriverWait(driver, PARSING_DELAY).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//li/a[@role='button' and @tabindex='0' and " +
                            f"@aria-label='Page {page_num}']"
                        )
                    )
                )
            )
            page_element.click()
            return False
        except TimeoutException:
            return True

    find_last_page: bool = False
    page_num: int = 2
    while not find_last_page:
        messages_number: WebElement = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    BASE_SELECTOR +
                    "//div[contains(@class, 'src-components-appeals-appeal-" +
                    "list-list-item-number-list-item-number-" +
                    "module__listNumberBox--QDD9X')]"
                )
            )
        )

        messages_date: WebElement = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    BASE_SELECTOR +
                    "//div[@class='src-containers-grid-template-container-" +
                    "grid-template-container-module__grid--Tv6NQ " +
                    "src-components-appeals-appeal-list-appeal-list-item-" +
                    "appeal-list-item-module__item--Uu_4B']"
                )
            )
        )

        messages_status: WebElement = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    BASE_SELECTOR +
                    "//div[contains(@class, 'src-components-appeals-appeal-" +
                    "list-list-item-status-list-item-" +
                    "status-module__container--cyDud')]"
                )
            )
        )

        messages_subject: WebElement = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    BASE_SELECTOR +
                    "//h4[contains(@class, 'src-components-appeals" +
                    "-appeal-list-list-item-category-list-item-category-" +
                    "module__category--n4_cw')]"
                )
            )
        )

        messages_text: WebElement = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    BASE_SELECTOR +
                    "//p[contains(@class, 'src-components-appeals-appeal" +
                    "-list-list-item-category-list-item-category-" +
                    "module__typeAppealText--Ml1rO')]"
                )
            )
        )

        for i in range(len(messages_number)):
            parsing_data = datetime.now()
            message_number: str = messages_number[i].text.strip()
            message_status: str = messages_status[i].text.strip()
            message_subject: str = messages_subject[i].text.strip()
            message_text: str = messages_text[i].text.strip()
            message_date: str = (
                messages_date[i].text.split('\n')[0].
                lower().replace('г.', '').strip()
            )
            message_day, message_month, message_year = (
                message_date.split(maxsplit=2)
            )
            message_month = MONTHS.get(message_month)
            message_date: str = f'{message_day} {message_month} {message_year}'
            message_date: date = datetime.strptime(
                message_date, '%d %m %Y'
            ).date()

            new_row = {
                'parsing_data': parsing_data,
                'message_number': message_number,
                'message_status': message_status,
                'message_subject': message_subject,
                'message_text': message_text,
                'message_date': message_date,
            }

            MESSAGES.loc[len(MESSAGES)] = new_row

        find_last_page = click_next_page(page_num)
        page_num += 1

    driver.quit()

    return MESSAGES
