import os
import sys
from typing import Optional, Callable, Dict
from datetime import datetime

import pandas as pd
from pandas import DataFrame
from colorama import init, Fore, Style

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CURRENT_DIR, '..', '..')))
from app.common.log_result import log_result  # noqa: E402
from app.common.log_timer import log_timer  # noqa: E402
from app.common.write_df_to_excel import write_df_to_excel  # noqa: E402
from database.db_conn import sql_queries  # noqa: E402
from database.requests.update_claims import request_update_claims  # noqa: E402
from database.requests.update_claims_states import (  # noqa: E402
    request_update_claims_states
)
from database.requests.update_claims_constants import (  # noqa: E402
    request_claims_constants_update
)
from database.requests.update_messages import (  # noqa: E402
    request_update_messages
)
from database.requests.update_messages_states import (  # noqa: E402
    request_update_messages_states
)
from database.requests.update_messages_constants import (  # noqa: E402
    request_messages_constants_update
)


init(autoreset=True)
PARSING_DATA_DIR: str = os.path.join(CURRENT_DIR, '..', '..', 'data')
os.makedirs(PARSING_DATA_DIR, exist_ok=True)
CLAIMS = DataFrame(
    columns=[
        'parsing_data',
        'claim_number',
        'claim_status',
        'claim_link',
        'claim_date',
        'claim_status_date',
        'claim_inner_number',
        'claim_response',
        'claim_address',
    ]
)
MESSAGES = DataFrame(
    columns=[
        'parsing_data',
        'message_number',
        'message_status',
        'message_date',
        'message_link',
        'message_subject',
        'message_text',
        'message_claim_number',
        'message_address',
    ]
)
CLAIMS_CONSTANTS_TYPES: Dict[str, int] = {
    'claim_date': 1030,
    'claim_link': 1040,
    'claim_inner_number': 1080,
    'claim_response': 1090,
    'claim_address': 1100,
}
MESSAGES_CONSTANTS_TYPES: Dict[str, int] = {
    'message_link': 1040,
    'message_address': 1100,
    'message_date': 2030,
    'message_subject': 2050,
    'message_text': 2060,
    'message_claim_number': 2070,
}


class PARSING:
    """Модель для описания процесса парсинга данных."""
    def __init__(
        self,
        instance_name: str,
        personal_area_id: int,
        login: str,
        password: Optional[str],
        declarant_id: int,
        declarant_name: str
    ):
        self.instance_name = instance_name
        self.personal_area_id = personal_area_id
        self.login = login
        self.password = password
        self.declarant_id = declarant_id
        self.declarant_name = declarant_name

    def parsing(
        self, func_parsing: Callable, save_df: bool = True
    ) -> Optional[DataFrame]:
        add_info = f'{self.declarant_name} ({self.login})'

        @log_timer(func_parsing.__name__)
        @log_result(func_parsing.__name__, add_info)
        def wrapped_func():
            return func_parsing(self.login, self.password)
        result_df: Optional[DataFrame] = wrapped_func()
        if result_df is None:
            return

        df_unique = result_df.drop_duplicates()
        df_unique = result_df.reset_index(drop=True)

        if save_df:
            write_df_to_excel(
                file_path=os.path.join(
                    PARSING_DATA_DIR, f'{func_parsing.__name__}.xlsx'
                ),
                df=df_unique,
                sheet_name=self.declarant_name
            )

        print(
            Fore.CYAN + Style.DIM +
            'Всего ' +
            Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
            f'{len(df_unique)}' +
            Style.RESET_ALL + Fore.CYAN + Style.DIM +
            ' заявок для ' +
            Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
            f'{func_parsing.__name__} ({self.declarant_name}).'
        )

        return df_unique

    def write_claims_data_to_db(self, claims_df: Optional[DataFrame]):
        if claims_df is None:
            return
        for index, row in claims_df.iterrows():
            claim_number: str = row['claim_number']
            claim_status: str = row['claim_status']
            parsing_data: datetime = row['parsing_data']

            # Обновляем таблицу claims:
            sql_queries(
                request_update_claims(
                    personal_area_id=self.personal_area_id,
                    declarant_id=self.declarant_id,
                    claim_number=claim_number
                )
            )

            # Обновляем таблицу claims_states:
            sql_queries(
                request_update_claims_states(
                    personal_area_id=self.personal_area_id,
                    declarant_id=self.declarant_id,
                    claim_number=claim_number,
                    claim_status=claim_status,
                    parsing_data=parsing_data
                )
            )

            # Обновляем таблицу constants:
            for claim_key, constant_type in CLAIMS_CONSTANTS_TYPES.items():
                claim_value = row.get(claim_key)
                if claim_value and not pd.isna(claim_value):
                    sql_queries(
                        request_claims_constants_update(
                            personal_area_id=self.personal_area_id,
                            declarant_id=self.declarant_id,
                            claim_number=claim_number,
                            parsing_data=parsing_data,
                            constant_type=constant_type,
                            constant_text=claim_value
                        )
                    )

            print(
                Fore.CYAN + Style.DIM +
                'Загрузка заявок для ' +
                Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                self.instance_name +
                Style.RESET_ALL + Fore.CYAN + Style.DIM +
                ' — ' +
                Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                f'{(round(100*(index + 1)/len(claims_df), 2))}%',
                end='\r'
            )
        print()

    def write_messages_data_to_db(self, messages_df: Optional[DataFrame]):
        if messages_df is None:
            return
        for index, row in messages_df.iterrows():
            message_number: str = row['message_number']
            message_status: str = row['message_status']
            parsing_data: datetime = row['parsing_data']

            # Обновляем таблицу messages:
            sql_queries(
                request_update_messages(
                    personal_area_id=self.personal_area_id,
                    declarant_id=self.declarant_id,
                    message_number=message_number
                )
            )

            # Обновляем таблицу messages_states:
            sql_queries(
                request_update_messages_states(
                    personal_area_id=self.personal_area_id,
                    declarant_id=self.declarant_id,
                    message_number=message_number,
                    message_status=message_status,
                    parsing_data=parsing_data
                )
            )

            # Обновляем таблицу messages_constants:
            for message_key, constant_type in MESSAGES_CONSTANTS_TYPES.items():
                message_value = row.get(message_key)
                if message_value and not pd.isna(message_value):
                    sql_queries(
                        request_messages_constants_update(
                            personal_area_id=self.personal_area_id,
                            declarant_id=self.declarant_id,
                            message_number=message_number,
                            parsing_data=parsing_data,
                            constant_type=constant_type,
                            constant_text=message_value
                        )
                    )

            print(
                Fore.CYAN + Style.DIM +
                'Загрузка обращений для ' +
                Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                self.instance_name +
                Style.RESET_ALL + Fore.CYAN + Style.DIM +
                ' — ' +
                Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                f'{(round(100*(index + 1)/len(messages_df), 2))}%',
                end='\r'
            )
        print()
