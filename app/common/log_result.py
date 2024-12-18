import os
import logging
from typing import Optional, Callable

from colorama import Fore, Style, init


init(autoreset=True)

LOG_DIR: str = os.path.join(os.path.dirname(__file__), '..', '..', 'log')
LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'result.log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)


def log_result(script_name: str, add_info: str = 'NaN') -> Callable:
    """Декоратор для логирования удачного или нет выполнения скрипта."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            error_msg: Optional[str] = None

            try:
                func(*args, **kwargs)
            except Exception as e:
                error_msg = str(e)
                print(
                    Fore.RED + Style.DIM +
                    'Произошла ошибка в ' + Style.RESET_ALL +
                    Fore.WHITE + Style.BRIGHT + f'{script_name}:\n' +
                    Style.RESET_ALL + error_msg
                )
            finally:
                if error_msg is None:
                    logging.info(f'{script_name} - {add_info}')
                else:
                    logging.error(f'{script_name} - {add_info}:\n' + error_msg)

        return wrapper

    return decorator
