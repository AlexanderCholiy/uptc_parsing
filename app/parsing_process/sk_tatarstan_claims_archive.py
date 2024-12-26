import os
import sys
import time
from datetime import datetime, date

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.models.parsing_model import CLAIMS  # noqa: E402
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
    "//div[contains(@class, 'src-pages-claims-common-claims-list-tech-" +
    "connection-tc-claims-list-module__claimsContainer--SWg2X')]" +
    "//div[contains(@class, 'src-pages-claims-common-claims-list-tech-" +
    "connection-item-tc-claim-item-module__itemWrapper--__1YP')]"
)


def sk_tatarstan_claims_archive(login: str, password: str, *args) -> DataFrame:
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
                "//a[@href='/claims']/li[contains(@class, 'src-components-" +
                "common-nav-bar-nav-tab-nav-tab-module__tab--Ayvp6')]"
            )
        )
    ).click()

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@href='/claims/tech-connection']")
        )
    ).click()

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@href='/claims/tech-connection/archive']")
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
        claims_number: WebElement = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    BASE_SELECTOR +
                    "//div[contains(@class, 'src-pages-claims-common-claims" +
                    "-list-tech-connection-item-tc-claim-item-" +
                    "module__secondColumn--i6FbW')]"
                )
            )
        )

        claims_date: WebElement = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    BASE_SELECTOR +
                    "//div[contains(@class, 'src-containers-grid-template-" +
                    "container-grid-template-container-module__grid--Tv6NQ " +
                    "src-pages-claims-common-claims-list-tech-connection" +
                    "-item-tc-claim-item-module__item--kA6Rj')]" +
                    "//div[contains(@class, 'src-lib-components-items-date-" +
                    "date-item-module__date--RpKjN')]/span"
                )
            )
        )

        claims_status: WebElement = wait.until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    BASE_SELECTOR +
                    "//div[contains(@class, 'src-lib-components-toggle-" +
                    "toggle-module__toggleBlock--KAm5c')]"
                )
            )
        )

        for i in range(len(claims_number)):
            parsing_data = datetime.now()
            claim_number: str = claims_number[i].text.strip()
            try:
                claim_link: str = (
                    claims_number[i].find_element(By.XPATH, ".//a").
                    get_attribute('href')
                )
            except NoSuchElementException:
                claim_link = None
            claim_status: str = claims_status[i].text.strip()
            claim_date: str = (
                claims_date[i].text.lower().replace('г.', '').strip()
            )
            claim_day, claim_month, claim_year = claim_date.split(maxsplit=2)
            claim_month = MONTHS.get(claim_month)
            claim_date: str = f'{claim_day} {claim_month} {claim_year}'
            claim_date: date = datetime.strptime(claim_date, '%d %m %Y').date()

            new_row = {
                'parsing_data': parsing_data,
                'claim_number': claim_number,
                'claim_status': claim_status,
                'claim_link': claim_link,
                'claim_date': claim_date,
            }

            CLAIMS.loc[len(CLAIMS)] = new_row

        find_last_page = click_next_page(page_num)
        page_num += 1

    driver.quit()

    return CLAIMS
