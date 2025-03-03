import logging
import os
from typing import Callable, Optional

from colorama import Fore, Style, init

init(autoreset=True)

LOG_DIR: str = os.path.join(os.path.dirname(__file__), '..', '..', 'log')
LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'result.log')
NOTIFICATION_LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'notification.log')
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger('result_logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s __ %(levelname)s __ %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

notification_logger = logging.getLogger('notification_logger')
notification_logger.setLevel(logging.DEBUG)
notification_file_handler = logging.FileHandler(
    NOTIFICATION_LOG_FILE_PATH, encoding='utf-8'
)
notification_file_handler.setLevel(logging.DEBUG)
notification_formatter = logging.Formatter(
    '%(asctime)s __ %(levelname)s __ %(message)s'
)
notification_file_handler.setFormatter(notification_formatter)
notification_logger.addHandler(notification_file_handler)


def log_result(func_name: str, add_info: str = 'NaN') -> Callable:
    """
    Декоратор для логирования удачного или нет выполнения скрипта.
    Не используйте " __ " в названиях аргументов!
    """
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
                    Fore.WHITE + Style.BRIGHT +
                    f'{func_name} ({add_info}):\n' +
                    Style.RESET_ALL + error_msg
                )
            finally:
                if error_msg is None:
                    logger.info(f'{func_name} __ {add_info}')
                    notification_logger.info(
                        f'{func_name} __ {add_info} __ not sent'
                    )
                else:
                    logger.error(f'{func_name} __ {add_info}:\n' + error_msg)
                    notification_logger.error(
                        f'{func_name} __ {add_info} __ not sent'
                    )

            return result

        return wrapper

    return decorator
