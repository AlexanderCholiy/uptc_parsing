from datetime import datetime
from typing import Optional

from colorama import Fore, Style, init

from app.models.parsing_model import PARSING
from app.parsing_process.mosoblenergo_claims import mosoblenergo_claims
from app.parsing_process.oboronenergo_claims import oboronenergo_claims
from app.parsing_process.oboronenergo_messages import oboronenergo_messages
from app.parsing_process.portal_tp_claims import portal_tp_claims
from app.parsing_process.portal_tp_claims_archive import (
    portal_tp_claims_archive
)
from app.parsing_process.portal_tp_claims_details import (
    portal_tp_claims_details
)
from app.parsing_process.portal_tp_messages import portal_tp_messages
from app.parsing_process.portal_tp_messages_archive import (
    portal_tp_messages_archive
)
from app.parsing_process.portal_tp_messages_details import (
    portal_tp_messages_details
)
from app.parsing_process.rosseti_mr_claims import rosseti_mr_claims
from app.parsing_process.rosseti_mr_messages import rosseti_mr_messages
from app.parsing_process.rzd_claims import rzd_claims
from app.parsing_process.sk_tatarstan_claims import sk_tatarstan_claims
from app.parsing_process.sk_tatarstan_claims_archive import (
    sk_tatarstan_claims_archive
)
from app.parsing_process.sk_tatarstan_messages import sk_tatarstan_messages
from settings.config import (mosoblenergo_settings, oboronenergo_settings,
                             portal_tp_settings, rosseti_mr_settings,
                             rzd_settings, sk_tatarstan_settings)

init(autoreset=True)

DAY_START: datetime = (
    datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
)
DAY_END: datetime = (
    datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
)
TIME_DELAY: int = 120


def run_parsing(
    save_df: bool = True,
    filter_by_last_days: Optional[int] = None,
    run_oboronenergo: bool = False,
    run_rzd: bool = False,
    run_portal_tp: bool = False,
    run_mosoblenergo: bool = False,
    run_sk_tatarstan: bool = False,
    run_rosseti_mr: bool = False
):
    """
    Parametrs:
    ---------
    - save_df (bool): Если True, данные будут сохранены в формате .xlsx в
    папке 'data'.

    - filter_by_last_days (int or None):
        Если None, будут обновлены все записи.
        Если указано значение (например 30), будут обновлены только
        актуальные записи за последние N дней.
    """
    # **************************** АО Оборонэнерго ****************************
    def oboronenergo(
        instance_name: str,
        login: str,
        password: str,
        declarant_id: int,
        declarant_name: str
    ):
        instance = PARSING(
            instance_name,
            oboronenergo_settings.PERSONAL_AREA_ID,
            login,
            password,
            declarant_id,
            declarant_name
        )
        instance.write_claims_data_to_db(
            instance.parsing(oboronenergo_claims, save_df),
            filter_by_last_days
        )
        instance.write_messages_data_to_db(
            instance.parsing(oboronenergo_messages, save_df),
            filter_by_last_days
        )

    oboronenergo_data = [
        (
            'oboronenergo_pbk_1',
            oboronenergo_settings.PBK_USER_LOGIN_1,
            oboronenergo_settings.PBK_USER_PSWD_1,
            oboronenergo_settings.PBK_USER_DECLARANT_ID,
            'PBK_1'
        )
    ]

    [oboronenergo(*params) for params in oboronenergo_data if run_oboronenergo]

    # ******************************** ОАО РЖД ********************************
    def rzd(
        instance_name: str,
        login: str,
        password: str,
        declarant_id: int,
        declarant_name: str
    ):
        instance = PARSING(
            instance_name,
            rzd_settings.PERSONAL_AREA_ID,
            login,
            password,
            declarant_id,
            declarant_name
        )
        instance.write_claims_data_to_db(
            instance.parsing(rzd_claims, save_df), filter_by_last_days
        )

    rzd_data = [
        (
            'rzd_rb_1',
            rzd_settings.RB_USER_LOGIN_1,
            rzd_settings.RB_USER_PSWD_1,
            rzd_settings.RB_USER_DECLARANT_ID,
            'RB_1'
        ),
        (
            'rzd_ooo_rb_1',
            rzd_settings.OOO_RB_USER_LOGIN_1,
            rzd_settings.OOO_RB_USER_PSWD_1,
            rzd_settings.OOO_RB_USER_DECLARANT_ID,
            'OOO_RB_1'
        ),
        (
            'rzd_ooo_rbt_1',
            rzd_settings.OOO_RBT_USER_LOGIN_1,
            rzd_settings.OOO_RBT_USER_PSWD_1,
            rzd_settings.OOO_RBT_USER_DECLARANT_ID,
            'OOO_RBT_1'
        ),
        (
            'rzd_ooo_rbt_2',
            rzd_settings.OOO_RBT_USER_LOGIN_2,
            rzd_settings.OOO_RBT_USER_PSWD_2,
            rzd_settings.OOO_RBT_USER_DECLARANT_ID,
            'OOO_RBT_2'
        )
    ]

    [rzd(*params) for params in rzd_data if run_rzd]

    # ******************************* Портал ТП *******************************
    def portal_tp(
        instance_name: str,
        login: str,
        password: str,
        declarant_id: int,
        declarant_name: str
    ):
        instance = PARSING(
            instance_name,
            portal_tp_settings.PERSONAL_AREA_ID,
            login,
            password,
            declarant_id,
            declarant_name
        )
        instance.write_claims_data_to_db(
            instance.parsing(portal_tp_claims, save_df),
            filter_by_last_days
        )
        instance.write_claims_data_to_db(
            instance.parsing(portal_tp_claims_archive, save_df),
            filter_by_last_days
        )
        instance.write_claims_data_to_db(
            instance.parsing(portal_tp_claims_details, save_df),
            None, True
        )
        instance.write_messages_data_to_db(
            instance.parsing(portal_tp_messages, save_df),
            filter_by_last_days
        )
        instance.write_messages_data_to_db(
            instance.parsing(portal_tp_messages_archive, save_df),
            filter_by_last_days
        )
        instance.write_messages_data_to_db(
            instance.parsing(portal_tp_messages_details, save_df),
            None, True
        )

    portal_tp_data = [
        (
            'portal_tp_rb_1',
            portal_tp_settings.RB_USER_LOGIN_1,
            portal_tp_settings.RB_USER_PSWD_1,
            portal_tp_settings.RB_USER_DECLARANT_ID,
            'RB_1'
        ),
        (
            'portal_tp_vrt_1',
            portal_tp_settings.VRT_USER_LOGIN_1,
            portal_tp_settings.VRT_USER_PSWD_1,
            portal_tp_settings.VRT_USER_DECLARANT_ID,
            'VRT_1'
        ),
        (
            'portal_tp_vrt_1_1',
            portal_tp_settings.VRT_1_USER_LOGIN_1,
            portal_tp_settings.VRT_1_USER_PSWD_1,
            portal_tp_settings.VRT_1_USER_DECLARANT_ID,
            'VRT_1_1'
        ),
        (
            'portal_tp_pbk_1',
            portal_tp_settings.PBK_USER_LOGIN_1,
            portal_tp_settings.PBK_USER_PSWD_1,
            portal_tp_settings.PBK_USER_DECLARANT_ID,
            'PBK_1'
        ),
        (
            'portal_tp_pbk_sib_1',
            portal_tp_settings.PBK_SIB_USER_LOGIN_1,
            portal_tp_settings.PBK_SIB_USER_PSWD_1,
            portal_tp_settings.PBK_SIB_USER_DECLARANT_ID,
            'PBK_SIB_1'
        ),
    ]

    [portal_tp(*params) for params in portal_tp_data if run_portal_tp]

    # ****************************** Мособлэнерго *****************************
    def mosoblenergo(
        instance_name: str,
        login: str,
        declarant_id: int,
        declarant_name: str
    ):
        instance = PARSING(
            instance_name,
            mosoblenergo_settings.PERSONAL_AREA_ID,
            login,
            None,
            declarant_id,
            declarant_name
        )

        instance.write_claims_data_to_db(
            instance.parsing(mosoblenergo_claims, save_df),
            filter_by_last_days
        )

    mosoblenergo_data = [
        (
            'mosoblenergo_vr_top_1',
            mosoblenergo_settings.VR_TOP_USER_LOGIN_1,
            mosoblenergo_settings.VR_TOP_USER_DECLARANT_ID,
            'VR_TOP_1'
        ),
        (
            'mosoblenergo_new_towers_mr_1',
            mosoblenergo_settings.NEW_TOWERS_MR_USER_LOGIN_1,
            mosoblenergo_settings.NEW_TOWERS_MR_USER_DECLARANT_ID,
            'NEW_TOWERS_MR_1'
        ),
        (
            'mosoblenergo_pbk_1',
            mosoblenergo_settings.PBK_USER_LOGIN_1,
            mosoblenergo_settings.PBK_USER_DECLARANT_ID,
            'PBK_1'
        ),
        (
            'mosoblenergo_rb_1',
            mosoblenergo_settings.RB_USER_LOGIN_1,
            mosoblenergo_settings.RB_USER_DECLARANT_ID,
            'RB_1'
        ),
        (
            'mosoblenergo_nb_mr_pbk_rb_hardenergy_1',
            mosoblenergo_settings.NB_MR_PBK_RB_HARDENERGY_USER_LOGIN_1,
            mosoblenergo_settings.NB_MR_PBK_RB_HARDENERGY_DECLARANT_ID,
            'NB_MR_PBK_RB_HARDENERGY'
        ),
        (
            'mosoblenergo_nb_mr_pbk_rb_promising_tech_1',
            mosoblenergo_settings.NB_MR_PBK_RB_PROMISING_TECH_USER_LOGIN_1,
            mosoblenergo_settings.NB_MR_PBK_RB_PROMISING_TECH_DECLARANT_ID,
            'NB_MR_PBK_RB_PROMISING_TECH'
        ),
    ]

    # Ночью код подтверждения приходит не всегда:
    [mosoblenergo(*params) for params in mosoblenergo_data if (
        run_mosoblenergo and DAY_START <= datetime.now() <= DAY_END
    )]

    # ***************************** СК Татарстан ******************************
    def sk_tatarstan(
        instance_name: str,
        login: str,
        password: str,
        declarant_id: int,
        declarant_name: str
    ):
        instance = PARSING(
            instance_name,
            sk_tatarstan_settings.PERSONAL_AREA_ID,
            login,
            password,
            declarant_id,
            declarant_name
        )
        instance.write_claims_data_to_db(
            instance.parsing(sk_tatarstan_claims, save_df),
            filter_by_last_days
        )
        instance.write_messages_data_to_db(
            instance.parsing(sk_tatarstan_messages, save_df),
            filter_by_last_days
        )
        instance.write_claims_data_to_db(
            instance.parsing(sk_tatarstan_claims_archive, save_df),
            filter_by_last_days
        )

    sk_tatarstan_data = [
        (
            'sk_tatarstan_pbk_1',
            sk_tatarstan_settings.PBK_USER_LOGIN_1,
            sk_tatarstan_settings.PBK_USER_PSWD_1,
            sk_tatarstan_settings.PBK_USER_DECLARANT_ID,
            'PBK_1'
        ),
    ]

    [sk_tatarstan(*params) for params in sk_tatarstan_data if run_sk_tatarstan]

    # ****************************** Россети МР *******************************
    def rosseti_mr(
        instance_name: str,
        login: str,
        password: str,
        declarant_id: int,
        declarant_name: str
    ):
        instance = PARSING(
            instance_name,
            rosseti_mr_settings.PERSONAL_AREA_ID,
            login,
            password,
            declarant_id,
            declarant_name
        )
        instance.write_claims_data_to_db(
            instance.parsing(rosseti_mr_claims, save_df),
            filter_by_last_days
        )
        instance.write_messages_data_to_db(
            instance.parsing(rosseti_mr_messages, save_df),
            filter_by_last_days
        )

    rosseti_mr_data = [
        (
            'rosseti_mr_new_towers_mr_1',
            rosseti_mr_settings.NEW_TOWERS_MR_USER_LOGIN_1,
            rosseti_mr_settings.NEW_TOWERS_MR_USER_PSWD_1,
            rosseti_mr_settings.NEW_TOWERS_MR_USER_DECLARANT_ID,
            'NEW_TOWERS_MR_1'
        ),
        (
            'rosseti_mr_ooo_rb_1',
            rosseti_mr_settings.OOO_RB_USER_LOGIN_1,
            rosseti_mr_settings.OOO_RB_USER_PSWD_1,
            rosseti_mr_settings.OOO_RB_USER_DECLARANT_ID,
            'OOO_RB_1'
        ),
        (
            'rosseti_mr_rb_1',
            rosseti_mr_settings.RB_USER_LOGIN_1,
            rosseti_mr_settings.RB_USER_PSWD_1,
            rosseti_mr_settings.RB_USER_DECLARANT_ID,
            'RB_1'
        ),
        (
            'rosseti_mr_pbk_1',
            rosseti_mr_settings.PBK_USER_LOGIN_1,
            rosseti_mr_settings.PBK_USER_PSWD_1,
            rosseti_mr_settings.PBK_USER_DECLARANT_ID,
            'PBK_1'
        ),
        (
            'rosseti_mr_ooo_capital_pole_1',
            rosseti_mr_settings.OOO_CAPITAL_POLE_USER_LOGIN_1,
            rosseti_mr_settings.OOO_CAPITAL_POLE_USER_PSWD_1,
            rosseti_mr_settings.OOO_CAPITAL_POLE_USER_DECLARANT_ID,
            'OOO_CAPITAL_POLE_1'
        ),
        (
            'rosseti_mr_nb_mr_srk_telecom_1',
            rosseti_mr_settings.NB_MR_SRK_TELECOM_1,
            rosseti_mr_settings.NB_MR_SRK_TELECOM_PSWD_1,
            rosseti_mr_settings.NB_MR_SRK_TELECOM_USER_DECLARANT_ID,
            'NB_MR_SRK_TELECOM_1'
        ),
        (
            'rosseti_mr_pbk_srk_telecom_1',
            rosseti_mr_settings.PBK_SRK_TELECOM_1,
            rosseti_mr_settings.PBK_SRK_TELECOM_PSWD_1,
            rosseti_mr_settings.PBK_SRK_TELECOM_USER_DECLARANT_ID,
            'PBK_SRK_TELECOM_1'
        ),
        (
            'rosseti_mr_rb_srk_telecom_1',
            rosseti_mr_settings.RB_SRK_TELECOM_1,
            rosseti_mr_settings.RB_SRK_TELECOM_PSWD_1,
            rosseti_mr_settings.RB_SRK_TELECOM_USER_DECLARANT_ID,
            'RB_SRK_TELECOM_1'
        ),
        (
            'rosseti_mr_nb_mr_hardenergy_1',
            rosseti_mr_settings.NB_MR_HARDENERGY_1,
            rosseti_mr_settings.NB_MR_HARDENERGY_PSWD_1,
            rosseti_mr_settings.NB_MR_HARDENERGY_USER_DECLARANT_ID,
            'NB_MR_HARDENERGY_1'
        ),
        (
            'rosseti_mr_pbk_hardenergy_1',
            rosseti_mr_settings.PBK_HARDENERGY_1,
            rosseti_mr_settings.PBK_HARDENERGY_PSWD_1,
            rosseti_mr_settings.PBK_HARDENERGY_USER_DECLARANT_ID,
            'PBK_HARDENERGY_1'
        ),
        (
            'rosseti_mr_rb_hardenergy_1',
            rosseti_mr_settings.RB_HARDENERGY_1,
            rosseti_mr_settings.RB_HARDENERGY_PSWD_1,
            rosseti_mr_settings.RB_HARDENERGY_USER_DECLARANT_ID,
            'RB_HARDENERGY_1'
        ),
        (
            'rosseti_mr_nb_mr_pbk_rb_promising_tech_1',
            rosseti_mr_settings.NB_MR_PBK_RB_PROMISING_TECH_1,
            rosseti_mr_settings.NB_MR_PBK_RB_PROMISING_TECH_PSWD_1,
            rosseti_mr_settings.NB_MR_PBK_RB_PROMISING_TECH_USER_DECLARANT_ID,
            'NB_MR_PBK_RB_PROMISING_TECH_1'
        ),
        (
            'rosseti_mr_pbk_pmk_1',
            rosseti_mr_settings.PBK_PMK_1,
            rosseti_mr_settings.PBK_PMK_PSWD_1,
            rosseti_mr_settings.PBK_PMK_USER_DECLARANT_ID,
            'PBK_PMK_1'
        ),
        (
            'rosseti_mr_pbk_infrascom_1',
            rosseti_mr_settings.PBK_INFRASCOM_1,
            rosseti_mr_settings.PBK_INFRASCOM_PSWD_1,
            rosseti_mr_settings.PBK_INFRASCOM_USER_DECLARANT_ID,
            'PBK_INFRASCOM_1'
        ),
    ]

    [rosseti_mr(*params) for params in rosseti_mr_data if run_rosseti_mr]


def log_completion(start_time: datetime):
    delta_time = round((datetime.now() - start_time).total_seconds())
    print(
        Fore.MAGENTA + Style.BRIGHT +
        f'Завершение {__file__} (Δt: {delta_time}c).'
    )


if __name__ == '__main__':
    start_time = datetime.now()
    print(Fore.MAGENTA + Style.BRIGHT + f'Запуск {__file__} ({start_time})')
    is_keyboard_interrupt: bool = False
    try:
        run_parsing(
            filter_by_last_days=90,
            run_oboronenergo=True,
            run_rzd=True,
            run_portal_tp=True,
            run_mosoblenergo=True,
            run_sk_tatarstan=True,
            run_rosseti_mr=True,
        )
    except KeyboardInterrupt:
        log_completion(start_time)
        is_keyboard_interrupt = True
    finally:
        if not is_keyboard_interrupt:
            log_completion(start_time)
