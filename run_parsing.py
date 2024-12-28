import time
from datetime import datetime
from typing import Optional

from colorama import init, Fore, Style

from settings.config import (
    oboronenergo_settings,
    rzd_settings,
    portal_tp_settings,
    mosoblenergo_settings,
    sk_tatarstan_settings,
    rosseti_mr_settings,
)
from app.models.parsing_model import PARSING
from app.parsing_process.oboronenergo_claims import oboronenergo_claims
from app.parsing_process.oboronenergo_messages import oboronenergo_messages
from app.parsing_process.rzd_claims import rzd_claims
from app.parsing_process.portal_tp_messages import portal_tp_messages
from app.parsing_process.portal_tp_claims import portal_tp_claims
from app.parsing_process.portal_tp_messages_details import (
    portal_tp_messages_details
)
from app.parsing_process.mosoblenergo_claims import mosoblenergo_claims
from app.parsing_process.sk_tatarstan_claims import sk_tatarstan_claims
from app.parsing_process.sk_tatarstan_messages import sk_tatarstan_messages
from app.parsing_process.sk_tatarstan_claims_archive import (
    sk_tatarstan_claims_archive
)
from app.parsing_process.rosseti_mr_claims import rosseti_mr_claims
from app.parsing_process.rosseti_mr_messages import rosseti_mr_messages


init(autoreset=True)

DAY_START: datetime = (
    datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
)
DAY_END: datetime = (
    datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
)
TIME_DELAY: int = 120


def run_parsing(
    save_df: bool = True, filter_by_last_days: Optional[int] = None
):
    """
    Parametrs:
    ---------
        save_df (bool): Если True, данные будут сохранены в формате .xlsx в
        папке 'data'.

        filter_by_last_days (int or None):
            Если None, будут обновлены все записи.
            Если указано значение (например, 30), будут обновлены только
            актуальные записи за последние N дней.
    """
    # АО Оборонэнерго:
    oboronenergo_pbk_1 = PARSING(
        'oboronenergo_pbk_1',
        oboronenergo_settings.PERSONAL_AREA_ID,
        oboronenergo_settings.PBK_USER_LOGIN_1,
        oboronenergo_settings.PBK_USER_PSWD_1,
        oboronenergo_settings.PBK_USER_DECLARANT_ID,
        declarant_name='PBK_1'
    )
    oboronenergo_pbk_1.write_claims_data_to_db(
        oboronenergo_pbk_1.parsing(oboronenergo_claims, save_df),
        filter_by_last_days
    )
    oboronenergo_pbk_1.write_messages_data_to_db(
        oboronenergo_pbk_1.parsing(oboronenergo_messages, save_df),
        filter_by_last_days
    )

    # ОАО РЖД:
    rzd_rb_1 = PARSING(
        'rzd_rb_1',
        rzd_settings.PERSONAL_AREA_ID,
        rzd_settings.RB_USER_LOGIN_1,
        rzd_settings.RB_USER_PSWD_1,
        rzd_settings.RB_USER_DECLARANT_ID,
        declarant_name='RB_1'
    )
    rzd_rb_1.write_claims_data_to_db(
        rzd_rb_1.parsing(rzd_claims, save_df), filter_by_last_days
    )

    rzd_ooo_rb_1 = PARSING(
        'rzd_ooo_rb_1',
        rzd_settings.PERSONAL_AREA_ID,
        rzd_settings.OOO_RB_USER_LOGIN_1,
        rzd_settings.OOO_RB_USER_PSWD_1,
        rzd_settings.OOO_RB_USER_DECLARANT_ID,
        'OOO_RB_1'
    )
    rzd_ooo_rb_1.write_claims_data_to_db(
        rzd_ooo_rb_1.parsing(rzd_claims, save_df), filter_by_last_days
    )

    rzd_ooo_rbt_1 = PARSING(
        'rzd_ooo_rbt_1',
        rzd_settings.PERSONAL_AREA_ID,
        rzd_settings.OOO_RBT_USER_LOGIN_1,
        rzd_settings.OOO_RBT_USER_PSWD_1,
        rzd_settings.OOO_RBT_USER_DECLARANT_ID,
        'OOO_RBT_1'
    )
    rzd_ooo_rbt_1.write_claims_data_to_db(
        rzd_ooo_rbt_1.parsing(rzd_claims, save_df), filter_by_last_days
    )

    rzd_ooo_rbt_2 = PARSING(
        'rzd_ooo_rbt_2',
        rzd_settings.PERSONAL_AREA_ID,
        rzd_settings.OOO_RBT_USER_LOGIN_2,
        rzd_settings.OOO_RBT_USER_PSWD_2,
        rzd_settings.OOO_RBT_USER_DECLARANT_ID,
        'OOO_RBT_2'
    )
    rzd_ooo_rbt_2.write_claims_data_to_db(
        rzd_ooo_rbt_2.parsing(rzd_claims, save_df), filter_by_last_days
    )

    # Портал ТП:
    portal_tp_rb_1 = PARSING(
        'portal_tp_rb_1',
        portal_tp_settings.PERSONAL_AREA_ID,
        portal_tp_settings.RB_USER_LOGIN_1,
        portal_tp_settings.RB_USER_PSWD_1,
        portal_tp_settings.RB_USER_DECLARANT_ID,
        'RB_1'
    )
    portal_tp_rb_1.write_claims_data_to_db(
        portal_tp_rb_1.parsing(portal_tp_claims, save_df),
        filter_by_last_days
    )
    portal_tp_rb_1.write_messages_data_to_db(
        portal_tp_rb_1.parsing(portal_tp_messages, save_df),
        filter_by_last_days
    )
    portal_tp_rb_1.write_messages_data_to_db(
        portal_tp_rb_1.parsing(portal_tp_messages_details, save_df),
        filter_by_last_days, True
    )

    portal_tp_vrt_1 = PARSING(
        'portal_tp_vrt_1',
        portal_tp_settings.PERSONAL_AREA_ID,
        portal_tp_settings.VRT_USER_LOGIN_1,
        portal_tp_settings.VRT_USER_PSWD_1,
        portal_tp_settings.VRT_USER_DECLARANT_ID,
        'VRT_1'
    )
    portal_tp_vrt_1.write_claims_data_to_db(
        portal_tp_vrt_1.parsing(portal_tp_claims, save_df),
        filter_by_last_days
    )
    portal_tp_vrt_1.write_messages_data_to_db(
        portal_tp_vrt_1.parsing(portal_tp_messages, save_df),
        filter_by_last_days
    )
    portal_tp_vrt_1.write_messages_data_to_db(
        portal_tp_vrt_1.parsing(portal_tp_messages_details, save_df),
        None, True
    )

    portal_tp_vrt_1_1 = PARSING(
        'portal_tp_vrt_1_1',
        portal_tp_settings.PERSONAL_AREA_ID,
        portal_tp_settings.VRT_1_USER_LOGIN_1,
        portal_tp_settings.VRT_1_USER_PSWD_1,
        portal_tp_settings.VRT_1_USER_DECLARANT_ID,
        'VRT_1_1'
    )
    portal_tp_vrt_1_1.write_claims_data_to_db(
        portal_tp_vrt_1_1.parsing(portal_tp_claims, save_df),
        filter_by_last_days
    )
    portal_tp_vrt_1_1.write_messages_data_to_db(
        portal_tp_vrt_1_1.parsing(portal_tp_messages, save_df),
        filter_by_last_days
    )
    portal_tp_vrt_1_1.write_messages_data_to_db(
        portal_tp_vrt_1_1.parsing(portal_tp_messages_details, save_df),
        None, True
    )

    portal_tp_pbk_1 = PARSING(
        'portal_tp_pbk_1',
        portal_tp_settings.PERSONAL_AREA_ID,
        portal_tp_settings.PBK_USER_LOGIN_1,
        portal_tp_settings.PBK_USER_PSWD_1,
        portal_tp_settings.PBK_USER_DECLARANT_ID,
        'PBK_1'
    )
    portal_tp_pbk_1.write_claims_data_to_db(
        portal_tp_pbk_1.parsing(portal_tp_claims, save_df),
        filter_by_last_days
    )
    portal_tp_pbk_1.write_messages_data_to_db(
        portal_tp_pbk_1.parsing(portal_tp_messages, save_df),
        filter_by_last_days
    )
    portal_tp_pbk_1.write_messages_data_to_db(
        portal_tp_pbk_1.parsing(portal_tp_messages_details, save_df),
        None, True
    )

    portal_tp_pbk_sib_1 = PARSING(
        'portal_tp_pbk_sib_1',
        portal_tp_settings.PERSONAL_AREA_ID,
        portal_tp_settings.PBK_SIB_USER_LOGIN_1,
        portal_tp_settings.PBK_SIB_USER_PSWD_1,
        portal_tp_settings.PBK_SIB_USER_DECLARANT_ID,
        'PBK_SIB_1'
    )
    portal_tp_pbk_sib_1.write_claims_data_to_db(
        portal_tp_pbk_sib_1.parsing(portal_tp_claims, save_df),
        filter_by_last_days
    )
    portal_tp_pbk_sib_1.write_messages_data_to_db(
        portal_tp_pbk_sib_1.parsing(portal_tp_messages, save_df),
        filter_by_last_days
    )
    portal_tp_pbk_sib_1.write_messages_data_to_db(
        portal_tp_pbk_sib_1.parsing(portal_tp_messages_details, save_df),
        None, True
    )

    # Мособлэнерго (ночью код подтверждения приходит не всегда):
    if DAY_START <= datetime.now() <= DAY_END:
        mosoblenergo_vr_top_1 = PARSING(
            'mosoblenergo_vr_top_1',
            mosoblenergo_settings.PERSONAL_AREA_ID,
            mosoblenergo_settings.VR_TOP_USER_LOGIN_1,
            None,
            mosoblenergo_settings.VR_TOP_USER_DECLARANT_ID,
            'VR_TOP_1'
        )
        mosoblenergo_vr_top_1.write_claims_data_to_db(
            mosoblenergo_vr_top_1.parsing(mosoblenergo_claims, save_df),
            filter_by_last_days
        )
        time.sleep(TIME_DELAY)
        mosoblenergo_new_towers_mr_1 = PARSING(
            'mosoblenergo_new_towers_mr_1',
            mosoblenergo_settings.PERSONAL_AREA_ID,
            mosoblenergo_settings.NEW_TOWERS_MR_USER_LOGIN_1,
            None,
            mosoblenergo_settings.NEW_TOWERS_MR_USER_DECLARANT_ID,
            'NEW_TOWERS_MR_1'
        )
        mosoblenergo_new_towers_mr_1.write_claims_data_to_db(
            mosoblenergo_new_towers_mr_1.parsing(mosoblenergo_claims, save_df),
            filter_by_last_days
        )
        time.sleep(TIME_DELAY)
        mosoblenergo_pbk_1 = PARSING(
            'mosoblenergo_pbk_1',
            mosoblenergo_settings.PERSONAL_AREA_ID,
            mosoblenergo_settings.PBK_USER_LOGIN_1,
            None,
            mosoblenergo_settings.PBK_USER_DECLARANT_ID,
            'PBK_1'
        )
        mosoblenergo_pbk_1.write_claims_data_to_db(
            mosoblenergo_pbk_1.parsing(mosoblenergo_claims, save_df),
            filter_by_last_days
        )
        time.sleep(TIME_DELAY)
        mosoblenergo_rb_1 = PARSING(
            'mosoblenergo_rb_1',
            mosoblenergo_settings.PERSONAL_AREA_ID,
            mosoblenergo_settings.RB_USER_LOGIN_1,
            None,
            mosoblenergo_settings.RB_USER_DECLARANT_ID,
            'RB_1'
        )
        mosoblenergo_rb_1.write_claims_data_to_db(
            mosoblenergo_rb_1.parsing(mosoblenergo_claims, save_df),
            filter_by_last_days
        )

    # СК Татарстан:
    sk_tatarstan_pbk_1 = PARSING(
        'sk_tatarstan_pbk_1',
        sk_tatarstan_settings.PERSONAL_AREA_ID,
        sk_tatarstan_settings.PBK_USER_LOGIN_1,
        sk_tatarstan_settings.PBK_USER_PSWD_1,
        sk_tatarstan_settings.PBK_USER_DECLARANT_ID,
        'PBK_1'
    )
    sk_tatarstan_pbk_1.write_claims_data_to_db(
        sk_tatarstan_pbk_1.parsing(sk_tatarstan_claims, save_df),
        filter_by_last_days
    )
    sk_tatarstan_pbk_1.write_messages_data_to_db(
        sk_tatarstan_pbk_1.parsing(sk_tatarstan_messages, save_df),
        filter_by_last_days
    )
    sk_tatarstan_pbk_1.write_claims_data_to_db(
        sk_tatarstan_pbk_1.parsing(sk_tatarstan_claims_archive, save_df),
        filter_by_last_days
    )

    # Россети МР:
    rosseti_mr_new_towers_mr_1 = PARSING(
        'rosseti_mr_new_towers_mr_1',
        rosseti_mr_settings.PERSONAL_AREA_ID,
        rosseti_mr_settings.NEW_TOWERS_MR_USER_LOGIN_1,
        rosseti_mr_settings.NEW_TOWERS_MR_USER_PSWD_1,
        rosseti_mr_settings.NEW_TOWERS_MR_USER_DECLARANT_ID,
        'NEW_TOWERS_MR_1'
    )
    rosseti_mr_new_towers_mr_1.write_claims_data_to_db(
        rosseti_mr_new_towers_mr_1.parsing(rosseti_mr_claims, save_df),
        filter_by_last_days
    )
    rosseti_mr_new_towers_mr_1.write_messages_data_to_db(
        rosseti_mr_new_towers_mr_1.parsing(rosseti_mr_messages, save_df),
        filter_by_last_days
    )

    rosseti_mr_ooo_rb_1 = PARSING(
        'rosseti_mr_ooo_rb_1',
        rosseti_mr_settings.PERSONAL_AREA_ID,
        rosseti_mr_settings.OOO_RB_USER_LOGIN_1,
        rosseti_mr_settings.OOO_RB_USER_PSWD_1,
        rosseti_mr_settings.OOO_RB_USER_DECLARANT_ID,
        'OOO_RB_1'
    )
    rosseti_mr_ooo_rb_1.write_claims_data_to_db(
        rosseti_mr_ooo_rb_1.parsing(rosseti_mr_claims, save_df),
        filter_by_last_days
    )
    rosseti_mr_ooo_rb_1.write_messages_data_to_db(
        rosseti_mr_ooo_rb_1.parsing(rosseti_mr_messages, save_df),
        filter_by_last_days
    )

    rosseti_mr_rb_1 = PARSING(
        'rosseti_mr_rb_1',
        rosseti_mr_settings.PERSONAL_AREA_ID,
        rosseti_mr_settings.RB_USER_LOGIN_1,
        rosseti_mr_settings.RB_USER_PSWD_1,
        rosseti_mr_settings.RB_USER_DECLARANT_ID,
        'RB_1'
    )
    rosseti_mr_rb_1.write_claims_data_to_db(
        rosseti_mr_rb_1.parsing(rosseti_mr_claims, save_df),
        filter_by_last_days
    )
    rosseti_mr_rb_1.write_messages_data_to_db(
        rosseti_mr_rb_1.parsing(rosseti_mr_messages, save_df),
        filter_by_last_days
    )

    rosseti_mr_pbk_1 = PARSING(
        'rosseti_mr_pbk_1',
        rosseti_mr_settings.PERSONAL_AREA_ID,
        rosseti_mr_settings.PBK_USER_LOGIN_1,
        rosseti_mr_settings.PBK_USER_PSWD_1,
        rosseti_mr_settings.PBK_USER_DECLARANT_ID,
        'PBK_1'
    )
    rosseti_mr_pbk_1.write_claims_data_to_db(
        rosseti_mr_pbk_1.parsing(rosseti_mr_claims, save_df),
        filter_by_last_days
    )
    rosseti_mr_pbk_1.write_messages_data_to_db(
        rosseti_mr_pbk_1.parsing(rosseti_mr_messages, save_df),
        filter_by_last_days
    )

    rosseti_mr_ooo_capital_pole_1 = PARSING(
        'rosseti_mr_ooo_capital_pole_1',
        rosseti_mr_settings.PERSONAL_AREA_ID,
        rosseti_mr_settings.OOO_CAPITAL_POLE_USER_LOGIN_1,
        rosseti_mr_settings.OOO_CAPITAL_POLE_USER_PSWD_1,
        rosseti_mr_settings.OOO_CAPITAL_POLE_USER_DECLARANT_ID,
        'OOO_CAPITAL_POLE_1'
    )
    rosseti_mr_ooo_capital_pole_1.write_claims_data_to_db(
        rosseti_mr_ooo_capital_pole_1.parsing(rosseti_mr_claims, save_df),
        filter_by_last_days
    )
    rosseti_mr_ooo_capital_pole_1.write_messages_data_to_db(
        rosseti_mr_ooo_capital_pole_1.parsing(rosseti_mr_messages, save_df),
        filter_by_last_days
    )


def log_completion(start_time):
    delta_time = round((datetime.now() - start_time).total_seconds())
    print(
        Fore.MAGENTA + Style.BRIGHT +
        f'Завершение {__file__} (Δt: {delta_time}c).'
    )


if __name__ == '__main__':
    start_time = datetime.now()
    print(Fore.MAGENTA + Style.BRIGHT + f'Запуск {__file__}')
    is_keyboard_interrupt: bool = False
    try:
        run_parsing(filter_by_last_days=90)
    except KeyboardInterrupt:
        log_completion(start_time)
        is_keyboard_interrupt = True
    finally:
        if not is_keyboard_interrupt:
            log_completion(start_time)
