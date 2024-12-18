import os
import sys
from typing import Union
from contextlib import closing
import logging

import psycopg2
from colorama import Style, Fore, init

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CURRENT_DIR, '..')))
from settings.config import db_settings  # noqa: E402


init(autoreset=True)

LOG_DIR: str = os.path.join(CURRENT_DIR, '..', 'log')
LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'sql.log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)


def sql_queries(request: str) -> Union[list, bool]:
    """
    Функция для выполнения запросов к базе данных PostgreSQL.

    Parameters:
    ----------
    request : str
        SQL-запрос, который нужно выполнить.

    Return:
    ------
    - list: Возвращает результаты запроса SELECT для запросов, не требующих
    COMMIT.
    - bool: Возвращает True для запросов, требующих выполнения COMMIT.
    - bool: Возвращает False в случае ошибки выполнения запроса.

    Raises:
    ------
    - Raises Exception: В случае возникновения ошибки при выполнении запроса
    результаты будут записаны в .log файл.
    """

    try:
        with closing(psycopg2.connect(
            user=db_settings.DB_USER,
            password=db_settings.DB_PSWD,
            host=db_settings.DB_HOST,
            port=db_settings.DB_PORT,
            database=db_settings.DB_NAME_TECH_PRIS
        )) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(request)

                if cursor.description:
                    results = cursor.fetchall()
                    return results
                else:
                    connection.commit()
                    return True

    except Exception as e:
        print(
            Fore.RED + Style.DIM +
            'В файле ' +
            Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
            os.path.basename(__file__) +
            Style.RESET_ALL + Fore.RED + Style.DIM +
            ' произошла ошибка при выполнении запроса к БД:\n' +
            Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
            request + '\n' +
            Style.RESET_ALL + str(e)
        )
        logging.error(
            f'\nВ файле {__file__} произошла ошибка ' +
            f'при выполнении запроса к БД:\n{request}\n{str(e)}'
        )

        return False
