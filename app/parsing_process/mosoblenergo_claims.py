import os
import sys
import time
import pytz
from datetime import datetime, date

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.models.parsing_model import CLAIMS  # noqa: E402
from settings.config import bot_email_settings  # noqa: E402
from app.common.take_code_from_email import take_code_from_email  # noqa: E402

PARSING_DELAY: int = 5
PARSING_TIMER: int = 120
PAGE_COUNT: int = 20
MAX_PAGE_COUNT: int = 208

BUTTON_CONSULTANT_CLOSE: str = (
    "//span[@class='webim-action webim-ico webim-ico-cross']"
)
BUTTON_LOGIN: str = "//input[@id='bx_auth_login']"
BUTTON_PASSWORD: str = "//input[@id='bx_auth_confirm_code']"
LIST_NAVIGATION: str = (
    "//li[@ng-repeat='item in menu  | filter: { menu: true }']"
)
LIST_PAGE_SWITCHER: str = (
    "//ul[@class='pagination pagination--desktop']/" +
    "li[@class='pagination__item ng-scope']"
)
LIST_APP_COMPANY: str = (
    "//div[@class='application-body']//span[@ng-bind='bid.NameApplicant']"
)
LIST_APP_NUM: str = (
    "//div[@class='application-head__title-box']" +
    "//span[@ng-bind='bid.ClaimNumber']"
)
LIST_APP_DATA: str = (
    "//div[@class='application-head__title-box']/span" +
    "[@class='application-head__title-box--date']/span[@class='ng-binding']"
)
LIST_APP_STATUS: str = (
    "//div[@class='application-head__info']/span[@ng-bind='bid.Status']"
)
LIST_APP_CATEGORY: str = (
    "//div[@class='application-body']/span[@ng-bind='bid.CategoryName']"
)
LIST_APP_ADRESS: str = (
    "//div[@class='application-body']" +
    "//span[@ng-bind='bid.ObjectTP.Address.AddressString']"
)
LIST_APP_COMPANY: str = (
    "//div[@class='application-body']//span[@ng-bind='bid.NameApplicant']"
)
LIST_APP_LINK: str = (
    "//div[@class='application ng-scope']/ul[@class='application-nav']" +
    "/li[@ng-show='!bid.AllowEdit']/a[@class='application-nav__link']"
)


def mosoblenergo_claims(login: str, password: str):
    driver = webdriver.Chrome()
    driver.get('https://moetp.ru/desktop/personal-applications/#login')
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)

    wait.until(EC.element_to_be_clickable((By.XPATH, BUTTON_CONSULTANT_CLOSE)))
    element = wait.until(
        EC.presence_of_element_located((By.XPATH, BUTTON_CONSULTANT_CLOSE))
    )
    element.click()
    element = wait.until(
        EC.presence_of_element_located((By.XPATH, BUTTON_LOGIN))
    )
    element.send_keys(login)
    time.sleep(2)
    element.send_keys(Keys.ENTER)

    confirmation_code = take_code_from_email(
        bot_email_settings.BOT_EMAIL_LOGIN_1,
        bot_email_settings.BOT_EMAIL_PSWD_1,
        bot_email_settings.EMAIL_SERVER,
        datetime.now(pytz.timezone('Europe/Moscow')),
        [
            'portal03@mosoblenergo.ru',
            'portal04@mosoblenergo.ru',
            'y.martynova@newtowers.ru',
        ],
        ['y.martynova@newtowers.ru']
    )
    if not confirmation_code:
        raise ValueError('Error receiving verification code.')
    element = wait.until(
        EC.presence_of_element_located((By.XPATH, BUTTON_PASSWORD))
    )
    element.send_keys(confirmation_code)
    element.send_keys(Keys.ENTER)

    wait.until(EC.element_to_be_clickable((By.XPATH, LIST_NAVIGATION)))
    element = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, LIST_NAVIGATION))
    )[2]
    element.click()

    for i in range(PAGE_COUNT):
        wait.until(
            EC.visibility_of_all_elements_located((By.XPATH, LIST_APP_COMPANY))
        )
        app_pages = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, LIST_PAGE_SWITCHER))
        )
        claims_number = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, LIST_APP_NUM))
        )
        claims_date = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, LIST_APP_DATA))
        )
        claims_status = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, LIST_APP_STATUS))
        )
        claims_link = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, LIST_APP_LINK))
        )

        for j in range(len(claims_number)):
            parsing_data = datetime.now()
            claim_link: list = (
                claims_link[j].get_attribute('href').split('desktop')
            )
            claim_link: str = f"{claim_link[0]}desktop/{claim_link[1]}"
            claim_inner_number: str = (
                claim_link[-13:-6].replace('n', '').replace('/', '')
            )

            claim_number = (
                claims_number[j].text
            ) if claims_number[j].text else (
                f'новая заявка ({claim_inner_number})'
            )

            claim_status: str = claims_status[j].text.strip()
            claim_date: str = claims_date[j].text.strip()
            claim_date: date = datetime.strptime(
                claim_date, '%d.%m.%Y'
            ).date()

            new_row = {
                'parsing_data': parsing_data,
                'claim_number': claim_number,
                'claim_status': claim_status,
                'claim_link': claim_link,
                'claim_date': claim_date,
                'claim_inner_number': claim_inner_number,
            }

            CLAIMS.loc[len(CLAIMS)] = new_row

        # От 2 до 6 страницы:
        if 0 <= i <= 4 and i <= (PAGE_COUNT - 2):
            app_pages[i].click()

        # От 7 до PAGE_COUNT - 3 страницы:
        elif 5 <= i <= (PAGE_COUNT - 2) and i < MAX_PAGE_COUNT - 4:
            app_pages[5].click()

        # Страница MAX_PAGE_COUNT - 2:
        elif PAGE_COUNT >= (MAX_PAGE_COUNT - 2) and i == MAX_PAGE_COUNT - 4:
            app_pages[6].click()

        # Страница MAX_PAGE_COUNT - 1:
        elif PAGE_COUNT >= (MAX_PAGE_COUNT - 1) and i == MAX_PAGE_COUNT - 3:
            app_pages[7].click()

        # Страница MAX_PAGE_COUNT:
        elif PAGE_COUNT == MAX_PAGE_COUNT and i == MAX_PAGE_COUNT - 2:
            app_pages[8].click()

    driver.quit()

    return CLAIMS
