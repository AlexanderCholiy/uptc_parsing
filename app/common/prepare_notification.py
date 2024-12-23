import os
import pandas as pd
from datetime import datetime


LOG_DIR: str = os.path.join(os.path.dirname(__file__), '..', '..', 'log')
LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'result.log')
NOTIFICATION_LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'notification.log')


def parse_log_line(line: str) -> dict:
    line: list[str] = line.split(' - ')
    timestamp: datetime = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S,%f')
    result: str = 'success' if line[1] != 'ERROR' else 'error'
    source: str = line[2].strip()
    executor: str = line[3].strip()
    is_send = False if line[4].strip() == 'not sent' else True

    return {
        'timestamp': timestamp,
        'result': result,
        'source': source,
        'executor': executor,
        'is_send': is_send,
    }


def prepare_notification() -> pd.DataFrame:
    try:
        with open(NOTIFICATION_LOG_FILE_PATH, 'r') as file:
            log_lines = file.readlines()
    except FileNotFoundError:
        return pd.DataFrame

    log_df = pd.DataFrame([parse_log_line(line) for line in log_lines])

    updated_lines = [line.replace('not sent', 'sent') for line in log_lines]

    with open(NOTIFICATION_LOG_FILE_PATH, 'w') as file:
        file.writelines(updated_lines)

    return log_df


if __name__ == '__main__':
    prepare_notification()
