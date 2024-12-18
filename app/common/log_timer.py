import os
import logging
from datetime import datetime, timedelta
from typing import Callable

from colorama import Fore, Style, init


init(autoreset=True)

LOG_DIR: str = os.path.join(os.path.dirname(__file__), '..', '..', 'log')
LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'timer.log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)


def log_timer(func: Callable):
    """Декоратор для подсчёта времени выполнения функции."""
    def wrapper(*args, **kwargs) -> Callable:
        start: datetime = datetime.now()
        func(*args, **kwargs)
        execution_time: timedelta = datetime.now() - start
        if execution_time.total_seconds() >= 60:
            print(
                Fore.CYAN + Style.DIM +
                f'Функция {Fore.WHITE + Style.BRIGHT + func.__name__} ' +
                Style.RESET_ALL + Fore.CYAN + Style.DIM +
                'выполнялась ' +
                Fore.WHITE + Style.BRIGHT +
                f'{execution_time // timedelta(minutes=1)} ' +
                Style.RESET_ALL + Fore.CYAN + Style.DIM + 'минут(ы).'
            )
            log_message: str = (
                f'Функция {func.__name__} выполнялась ' +
                f'{execution_time // timedelta(minutes=1)} минут(ы).'
            )
        elif execution_time.total_seconds() >= 1:
            print(
                Fore.CYAN + Style.DIM +
                f'Функция {Fore.WHITE + Style.BRIGHT + func.__name__} ' +
                Style.RESET_ALL + Fore.CYAN + Style.DIM +
                'выполнялась ' +
                Fore.WHITE + Style.BRIGHT +
                f'{round(execution_time.total_seconds(), 1)} ' +
                Style.RESET_ALL + Fore.CYAN + Style.DIM + 'секунд(ы).'
            )
            log_message: str = (
                f'Функция {func.__name__} выполнялась ' +
                f'{round(execution_time.total_seconds(), 1)} секунд(ы).'
            )
        else:
            print(
                Fore.CYAN + Style.DIM +
                f'Функция {Fore.WHITE + Style.BRIGHT + func.__name__} ' +
                Style.RESET_ALL + Fore.CYAN + Style.DIM +
                'выполнялась ' +
                Fore.WHITE + Style.BRIGHT +
                f'{round(execution_time.total_seconds(), 3)} ' +
                Style.RESET_ALL + Fore.CYAN + Style.DIM + 'микросекунд(ы).'
            )
            log_message: str = (
                f'Функция {func.__name__} выполнялась ' +
                f'{round(execution_time.total_seconds(), 3)} микросекунд(ы).'
            )

        logging.info(log_message)

    return wrapper
