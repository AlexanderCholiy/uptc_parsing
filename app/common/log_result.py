import os
import logging
from typing import Optional, Callable

from colorama import Fore, Style, init


init(autoreset=True)

LOG_DIR: str = os.path.join(os.path.dirname(__file__), '..', '..', 'log')
LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'result.log')
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger('result_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def log_result(func_name: str, add_info: str = 'NaN') -> Callable:
    """Декоратор для логирования удачного или нет выполнения скрипта."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            error_msg: Optional[str] = None
            result = None

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error_msg = str(e)
                print(
                    Fore.RED + Style.DIM +
                    'Произошла ошибка в ' + Style.RESET_ALL +
                    Fore.WHITE + Style.BRIGHT + f'{func_name}:\n' +
                    Style.RESET_ALL + error_msg
                )
            finally:
                if error_msg is None:
                    logger.info(f'{func_name} - {add_info}')
                else:
                    logger.error(f'{func_name} - {add_info}:\n' + error_msg)

            return result

        return wrapper

    return decorator
