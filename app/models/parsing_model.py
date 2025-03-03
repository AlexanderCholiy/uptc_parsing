import os
import sys
from datetime import date, timedelta
from typing import Callable, Dict, List, Optional

import pandas as pd
from colorama import Fore, Style, init
from pandas import DataFrame

CURRENT_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CURRENT_DIR, '..', '..')))
from app.common.log_result import log_result  # noqa: E402
from app.common.log_timer import log_timer  # noqa: E402
from app.common.write_df_to_excel import write_df_to_excel  # noqa: E402
from database.db_conn import sql_queries  # noqa: E402
from database.requests.add_related_claims_with_messages import \
    add_related_claims_with_messages  # noqa: E402
from database.requests.update_claims_constants import \
    request_update_claims_constants  # noqa: E402
from database.requests.update_claims_numbers import \
    request_update_claims_numbers  # noqa: E402
from database.requests.update_claims_states import \
    request_update_claims_states  # noqa: E402
from database.requests.update_messages_constants import \
    request_update_messages_constants  # noqa: E402
from database.requests.update_messages_numbers import \
    request_update_messages_numbers  # noqa: E402
from database.requests.update_messages_states import \
    request_update_messages_states  # noqa: E402

init(autoreset=True)
PARSING_DATA_DIR: str = os.path.join(CURRENT_DIR, '..', '..', 'data')
os.makedirs(PARSING_DATA_DIR, exist_ok=True)
CLAIMS_COLUMNS: List[str] = [
    'parsing_data',
    'claim_number',
    'claim_status',
    'claim_link',
    'claim_date',
    'claim_status_date',
    'claim_inner_number',
    'claim_response',
    'claim_address',
    'claim_documents_link',
]

MESSAGES_COLUMNS: List[str] = [
    'parsing_data',
    'message_number',
    'message_status',
    'message_date',
    'message_link',
    'message_subject',
    'message_text',
    'message_claim_number',
    'message_address',
    'message_filial',
    'message_grid',
]

CLAIMS_CONSTANTS_TYPES: Dict[str, int] = {
    'claim_date': 1030,
    'claim_link': 1040,
    'claim_inner_number': 1080,
    'claim_response': 1090,
    'claim_address': 1100,
    'claim_documents_link': 1050,
}
MESSAGES_CONSTANTS_TYPES: Dict[str, int] = {
    'message_grid': 1010,
    'message_filial': 1020,
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
        """
        Каждый DataFrame, который возвращает func_parsing должен быть определен
        локально!
        """
        add_info = f'{self.declarant_name} - {self.login}'

        @log_timer(func_parsing.__name__)
        @log_result(func_parsing.__name__, add_info)
        def wrapped_func():
            return func_parsing(
                self.login, self.password,
                self.personal_area_id, self.declarant_id
            )
        result_df: Optional[DataFrame] = wrapped_func()
        if result_df is None:
            return

        df_unique = result_df.drop_duplicates().reset_index(drop=True)

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
            ' записей для ' +
            Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
            f'{func_parsing.__name__} ({self.declarant_name}).'
        )

        return df_unique

    def _write_data_to_db(
        self,
        data_type: str,
        df: Optional[DataFrame],
        constants_types: dict,
        date_column_name: str,
        filter_by_last_days: Optional[int],
        only_constants: bool,
        request_update_fn: Callable,
        request_update_states_fn: Callable,
        request_update_constants_fn: Callable,
    ):
        if df is None:
            return

        if filter_by_last_days is not None and not (
            df[date_column_name].isna().all()
        ):
            cutoff_date = date.today() - timedelta(days=filter_by_last_days)
            df = (
                df[
                    (df[date_column_name].isna())
                    | (df[date_column_name] >= cutoff_date)
                ].reset_index(drop=True)
            )

        for index, row in df.iterrows():
            number = row[f'{data_type}_number']
            status = row[f'{data_type}_status']
            parsing_data = row['parsing_data']

            if not only_constants:
                if not sql_queries(
                    request_update_fn(
                        self.personal_area_id, self.declarant_id, number
                    )
                ):
                    continue

            if not only_constants and not pd.isna(status):
                sql_queries(
                    request_update_states_fn(
                        self.personal_area_id, self.declarant_id,
                        number, status, parsing_data
                    )
                )

            for key, constant_type in constants_types.items():
                constant_value = row.get(key)
                if constant_value and not pd.isna(constant_value):
                    constant_value = constant_value.replace(
                        "'", "`"
                    ) if isinstance(constant_value, str) else constant_value

                    sql_queries(
                        request_update_constants_fn(
                            self.personal_area_id, self.declarant_id,
                            number, parsing_data, constant_type, constant_value
                        )
                    )

            print(
                Fore.CYAN + Style.DIM +
                f'Загрузка {data_type} для ' +
                Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                self.instance_name +
                Style.RESET_ALL + Fore.CYAN + Style.DIM +
                ' — ' +
                Style.RESET_ALL + Fore.WHITE + Style.BRIGHT +
                f'{(round(100*(index + 1)/len(df), 2))}%',
                end='\r'
            )
        print()

    def write_claims_data_to_db(
        self,
        claims_df: Optional[DataFrame],
        filter_by_last_days: Optional[int] = None,
        only_constants: bool = False
    ):
        self._write_data_to_db(
            data_type='claim',
            df=claims_df,
            constants_types=CLAIMS_CONSTANTS_TYPES,
            date_column_name='claim_date',
            filter_by_last_days=filter_by_last_days,
            only_constants=only_constants,
            request_update_fn=request_update_claims_numbers,
            request_update_states_fn=request_update_claims_states,
            request_update_constants_fn=request_update_claims_constants
        )

    def write_messages_data_to_db(
        self,
        messages_df: Optional[DataFrame],
        filter_by_last_days: Optional[int] = None,
        only_constants: bool = False
    ):
        self._write_data_to_db(
            data_type='message',
            df=messages_df,
            constants_types=MESSAGES_CONSTANTS_TYPES,
            date_column_name='message_date',
            filter_by_last_days=filter_by_last_days,
            only_constants=only_constants,
            request_update_fn=request_update_messages_numbers,
            request_update_states_fn=request_update_messages_states,
            request_update_constants_fn=request_update_messages_constants
        )
        if not only_constants:
            sql_queries(
                add_related_claims_with_messages(
                    self.personal_area_id, self.declarant_id
                )
            )
