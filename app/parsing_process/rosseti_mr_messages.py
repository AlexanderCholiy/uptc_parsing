import os
import sys
import time
from datetime import date, datetime

from pandas import DataFrame
from selenium import webdriver
from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '..', '..'))
from app.common.authorize_form import authorize_form  # noqa: E402
from app.common.logger import rosseti_mr_logger  # noqa: E402
from app.models.parsing_model import MESSAGES_COLUMNS  # noqa: E402


PARSING_DELAY: int = 5
PARSING_TIMER: int = 120


def rosseti_mr_messages(login: str, password: str, *args) -> DataFrame:
    MESSAGES = DataFrame(columns=MESSAGES_COLUMNS)
    driver = webdriver.Chrome()
    driver.get(
        'https://lk.rossetimr.ru/cabinet/messages?message_tab=appeal_messages'
    )
    driver.maximize_window()
    wait = WebDriverWait(driver, PARSING_TIMER)

    rosseti_mr_logger.debug('Запуск сбора обращений')

    authorize_form(
        wait, login, password,
        "//*[@id='user_email']",
        "//*[@id='password-input']",
        "//button[span[text()='Войти']]"
    )

    rosseti_mr_logger.debug('Прошли авторизацию')

    wait.until(
        lambda browser: browser.execute_script(
            'return document.readyState'
        ) == 'complete'
    )

    rosseti_mr_logger.debug('Дождались загрузки страницы')

    bot_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "close-iframe-bot"))
    )
    bot_btn.click()
    rosseti_mr_logger.debug('Закрыли бота')

    cookie_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "cookie-dismiss"))
    )
    cookie_btn.click()
    rosseti_mr_logger.debug('Приняли cookie')

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
        min_message_date = date.today()
        for row in rows:
            try:
                cells = row.find_elements(By.XPATH, ".//td")
                parsing_data = datetime.now()
                message_number: str = cells[1].text.strip()
                message_status = cells[3].text.strip()
                message_link = (
                    f'https://lk.rossetimr.ru/{row.get_attribute("href")}'
                )

                raw_date = cells[0].text.strip()
                raw_date = (
                    raw_date.replace('\n', '').replace(' ', '').rstrip('.')
                )
                message_date = datetime.strptime(raw_date, '%d.%m.%Y').date()

                message_address: str = cells[7].text.split('\n')[0].strip()
                message_internal_number = (
                    message_link.split('?page')[0].split('messages/')[1]
                )
                message_number = message_number if message_number != '' else (
                    f'внутренний номер {message_internal_number}'
                )
                message_claim_number: str = cells[8].text.strip()
                message_subject: str = cells[2].text.strip()
                message_text: str = cells[6].text.strip()

                new_row = {
                    'parsing_data': parsing_data,
                    'message_number': message_number,
                    'message_status': message_status,
                    'message_date': message_date,
                    'message_link': message_link,
                    'message_subject': message_subject,
                    'message_text': message_text,
                    'message_claim_number': message_claim_number,
                    'message_address': message_address,
                }

                MESSAGES.loc[len(MESSAGES)] = new_row

                min_message_date = min(message_date, min_message_date)

            except StaleElementReferenceException:
                continue

        return min_message_date

    try:
        WebDriverWait(driver, PARSING_DELAY).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='strong-shadow request-table-w1 " +
                    "table-scroll mobile-table-zai']/h1[text()=" +
                    "'У вас пока нет обращений']"
                )
            )
        )
        rosseti_mr_logger.info(f'Найдено {len(MESSAGES)} обращений.')
        driver.quit()
        rosseti_mr_logger.debug('Вышли из браузера')
        return MESSAGES
    except TimeoutException:
        pass

    page_number = 1

    try:
        WebDriverWait(driver, PARSING_DELAY).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@class, 'custom-combobox-toggle')]")
            )
        ).click()
        rosseti_mr_logger.debug('Нажали на выбор кол-ва элементов на странице')
        WebDriverWait(driver, PARSING_DELAY).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(text(), '100')]")
            )
        ).click()
        rosseti_mr_logger.debug('Выбрали 100 элементов на странице')
        last_page: bool = False
    except TimeoutException:
        rosseti_mr_logger.debug(f'Стр. {page_number}')
        take_data_from_page()
        page_number += 1
        last_page: bool = True

    while not last_page:
        try:
            # if take_data_from_page() < date.today() - timedelta(days=365):
            #     break
            take_data_from_page()
            rosseti_mr_logger.debug(f'Стр. {page_number}')
            page_number += 1

            WebDriverWait(driver, PARSING_DELAY).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//a[contains(@class, 'paging_link_next link')]"
                    )
                )
            ).click()
            rosseti_mr_logger.debug('Переключились на следующую страницу')

        except TimeoutException:
            last_page = True

    rosseti_mr_logger.info(f'Найдено {len(MESSAGES)} заявок.')

    driver.quit()

    rosseti_mr_logger.debug('Вышли из браузера')

    return MESSAGES
