import os
import subprocess
from datetime import date, timedelta, datetime

from colorama import Fore, Style, init

from settings.config import db_settings
from app.common.log_result import logger
from app.common.log_timer import log_timer


init(autoreset=True)
CURRENT_DIR: str = os.path.dirname(__file__)
DUMP_PATH: str = os.path.join('E:\\', 'PostgreSQL', '10', 'bin', 'pg_dump.exe')
TODAY: date = date.today()
DB_NAME_TECH_PRIS: str = db_settings.DB_NAME_TECH_PRIS
DB_NAME_AVR: str = db_settings.DB_NAME_AVR
DUMPS_DIR_TECH_PRIS: str = os.path.join(
    CURRENT_DIR, 'database', 'dumps', DB_NAME_TECH_PRIS
)
DUMPS_DIR_AVR: str = os.path.join(
    CURRENT_DIR, 'database', 'dumps', DB_NAME_AVR
)
OUTPUT_FILE_TECH_PRIS: str = os.path.join(
    DUMPS_DIR_TECH_PRIS, f'{TODAY}__{DB_NAME_TECH_PRIS}.dump'
)
OUTPUT_FILE_AVR: str = os.path.join(
    DUMPS_DIR_AVR, f'{TODAY}__{DB_NAME_AVR}.dump'
)


def dump_postgresql_db(
    dump_path: str, db_name: str, user: str, password: str, output_file: str,
    host: str = 'localhost', port: int | str = 5432
):
    """
    Создание дампа базы данных PostgreSQL на windows командой:
    $env:PGPASSWORD='password';
    & "dump_path" -h host -p port -U postgres -F c -b -v -f output_file db_name

    Parameters:
    ----------
    - dump_path: путь к файлу PostgreSQL, предазначенной для создания резервных
    копий базы данных.

    """
    os.environ['PGPASSWORD'] = password
    command = [
        str(dump_path),
        '-h', host,
        '-p', str(port),
        '-U', user,
        '-F', 'c',
        '-b',
        # '-v',
        '-f', output_file,
        db_name
    ]

    try:
        subprocess.run(command, check=True)
        logger.info(f'новая резервная копия БД {db_name}')
        print(
            Fore.BLUE + Style.DIM + 'Дамп базы данных ' +
            Fore.WHITE + Style.BRIGHT + db_name +
            Fore.BLUE + Style.DIM + ' успешно создан в ' +
            Fore.WHITE + Style.BRIGHT + output_file
        )
    except subprocess.CalledProcessError as e:
        logger.error(
            f'при создании резервной копии БД {db_name} возникла ошибка:\n{e}'
        )
        print(
            Fore.RED + Style.DIM + 'Ошибка при создании дампа базы данных ' +
            Fore.WHITE + Style.BRIGHT + f'{db_name}:\n' +
            Fore.RED + Style.DIM + str(e)
        )


def remove_old_dumps(dumps_number: int, dumps_max_date: date, directory_path):
    files_names: list[str] = os.listdir(directory_path)
    if len(files_names) < dumps_number:
        return
    for file_name in files_names:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            try:
                file_date: date = datetime.strptime(
                    file_name.split('__')[0], '%Y-%m-%d'
                ).date()

                if file_date < dumps_max_date:
                    os.remove(file_path)
            except ValueError:
                print(
                    Fore.RED + Style.DIM +
                    'Неправильный формат даты в имени файла: ' +
                    Fore.WHITE + Style.BRIGHT + file_name
                )


@log_timer('dump_db')
def main():
    for dump_dir, output_file, db_name in [
        (DUMPS_DIR_TECH_PRIS, OUTPUT_FILE_TECH_PRIS, DB_NAME_TECH_PRIS),
        (DUMPS_DIR_AVR, OUTPUT_FILE_AVR, DB_NAME_AVR)
    ]:
        os.makedirs(dump_dir, exist_ok=True)
        dump_postgresql_db(
            DUMP_PATH,
            db_name,
            db_settings.DB_USER,
            db_settings.DB_PSWD,
            output_file,
            db_settings.DB_HOST,
            db_settings.DB_PORT
        )
        remove_old_dumps(30, TODAY - timedelta(days=30), dump_dir)    


if __name__ == '__main__':
    main()
