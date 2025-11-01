import os
from datetime import datetime, timedelta
from typing import Callable
import functools
from logging import Logger


def run_with_lock(
    lock_file: str,
    logger: Logger,
    lock_timeout: timedelta = timedelta(hours=3)
):
    """
    Декоратор, предотвращающий параллельный запуск функции.
    Создаёт lock-файл с PID и временем старта.
    """

    def decorator(func: Callable):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock_acquired = False
            start_time = datetime.now()

            # Проверка наличия lock-файла
            if os.path.exists(lock_file):
                try:
                    with open(lock_file) as f:
                        content = f.read().strip()

                    pid_str, ts_str = content.split('|')
                    last_pid = int(pid_str)
                    last_start_time = datetime.fromisoformat(ts_str)

                    # Проверка таймаута
                    if start_time - last_start_time < lock_timeout:
                        logger.warning(
                            f'Пропуск запуска {func.__name__}: процесс ещё '
                            f'выполняется (PID={last_pid}).'
                        )
                        return
                    else:
                        logger.warning(
                            f'Lock-файл устарел, перезаписываем: {lock_file}'
                        )
                except Exception:
                    logger.exception(
                        f'Ошибка чтения lock-файла {lock_file}, перезаписываем'
                    )

            try:
                # Создание нового lock-файла
                with open(lock_file, 'w') as f:
                    f.write(f'{os.getpid()}|{start_time.isoformat()}')

                lock_acquired = True
                logger.info(f'Запуск {func.__name__} с lock')

                return func(*args, **kwargs)

            finally:
                if lock_acquired and os.path.exists(lock_file):
                    os.remove(lock_file)
                    logger.info(
                        f'Lock-файл удалён после выполнения: {lock_file}'
                    )

        return wrapper

    return decorator
