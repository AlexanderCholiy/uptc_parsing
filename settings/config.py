import os

from dotenv import load_dotenv


CURRENT_DIR: str = os.path.dirname(os.path.abspath(__file__))
ENV_PATH: str = os.path.join(CURRENT_DIR, '.env')
load_dotenv(ENV_PATH)


class DB_SETTINGS:
    """Параметры подключения к БД."""
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = int(os.getenv('DB_PORT'))
    DB_USER: str = os.getenv('DB_USER')
    DB_PSWD: str = os.getenv('DB_PSWD')
    DB_NAME_TECH_PRIS: str = os.getenv('DB_NAME_TECH_PRIS')
    DB_NAME_AVR: str = os.getenv('DB_NAME_AVR')
    DB_NAME_WEB: str = os.getenv('DB_NAME_WEB')


class PORTAL_TP_SETTINGS:
    """Данные ЛК ПорталТП."""
    PERSONAL_AREA_ID: int = 1

    PBK_USER_LOGIN_1: str = os.getenv('PORTAL_TP_PBK_USER_LOGIN_1')
    PBK_USER_PSWD_1: str = os.getenv('PORTAL_TP_PBK_USER_PSWD_1')
    PBK_USER_DECLARANT_ID: int = 1

    RB_USER_LOGIN_1: str = os.getenv('PORTAL_TP_RB_USER_LOGIN_1')
    RB_USER_PSWD_1: str = os.getenv('PORTAL_TP_RB_USER_PSWD_1')
    RB_USER_DECLARANT_ID: int = 2

    VRT_USER_LOGIN_1: str = os.getenv('PORTAL_TP_VRT_USER_LOGIN_1')
    VRT_USER_PSWD_1: str = os.getenv('PORTAL_TP_VRT_USER_PSWD_1')
    VRT_USER_DECLARANT_ID: int = 3

    VRT_1_USER_LOGIN_1: str = os.getenv('PORTAL_TP_VRT_1_USER_LOGIN_1')
    VRT_1_USER_PSWD_1: str = os.getenv('PORTAL_TP_VRT_1_USER_PSWD_1')
    VRT_1_USER_DECLARANT_ID: int = 4

    PBK_SIB_USER_LOGIN_1: str = os.getenv('PORTAL_TP_PBK_SIB_USER_LOGIN_1')
    PBK_SIB_USER_PSWD_1: str = os.getenv('PORTAL_TP_PBK_SIB_USER_PSWD_1')
    PBK_SIB_USER_DECLARANT_ID: int = 5


class MOSOBLENERGO_SETTINGS:
    """Данные ЛК ПорталТП."""
    PERSONAL_AREA_ID: int = 2

    PBK_USER_LOGIN_1: str = os.getenv('MOSOBLENERGO_PBK_USER_LOGIN_1')
    PBK_USER_DECLARANT_ID: int = 1

    RB_USER_LOGIN_1: str = os.getenv('MOSOBLENERGO_RB_USER_LOGIN_1')
    RB_USER_DECLARANT_ID: int = 2

    NEW_TOWERS_MR_USER_LOGIN_1: str = os.getenv(
        'MOSOBLENERGO_NEW_TOWERS_MR_USER_LOGIN_1'
    )
    NEW_TOWERS_MR_USER_DECLARANT_ID: int = 6

    VR_TOP_USER_LOGIN_1: str = os.getenv('MOSOBLENERGO_VR_TOP_USER_LOGIN_1')
    VR_TOP_USER_DECLARANT_ID: int = 10


class SK_TATARSTAN_SETTINGS:
    """Данные ЛК АО «Сетевая компания» Республики Татарстан."""
    PERSONAL_AREA_ID: int = 3

    PBK_USER_LOGIN_1: str = os.getenv('SK_TATARSTAN_PBK_USER_LOGIN_1')
    PBK_USER_PSWD_1: str = os.getenv('SK_TATARSTAN_PBK_USER_PSWD_1')
    PBK_USER_DECLARANT_ID: int = 1


class RZD_SETTINGS:
    """Данные ЛК РЖД."""
    PERSONAL_AREA_ID: int = 4

    PBK_USER_LOGIN_1: str = os.getenv('RZD_PBK_USER_LOGIN_1')
    PBK_USER_PSWD_1: str = os.getenv('RZD_PBK_USER_PSWD_1')
    PBK_USER_DECLARANT_ID: int = 1

    RB_USER_LOGIN_1: str = os.getenv('RZD_RB_USER_LOGIN_1')
    RB_USER_PSWD_1: str = os.getenv('RZD_RB_USER_PSWD_1')
    RB_USER_DECLARANT_ID: int = 2

    VRT_USER_LOGIN_1: str = os.getenv('RZD_VRT_USER_LOGIN_1')
    VRT_USER_PSWD_1: str = os.getenv('RZD_VRT_USER_PSWD_1')
    VRT_USER_DECLARANT_ID: int = 3

    OOO_RBT_USER_LOGIN_1: str = os.getenv('RZD_OOO_RBT_USER_LOGIN_1')
    OOO_RBT_USER_PSWD_1: str = os.getenv('RZD_OOO_RBT_USER_PSWD_1')
    OOO_RBT_USER_LOGIN_2: str = os.getenv('RZD_OOO_RBT_USER_LOGIN_2')
    OOO_RBT_USER_PSWD_2: str = os.getenv('RZD_OOO_RBT_USER_PSWD_2')
    OOO_RBT_USER_DECLARANT_ID: int = 7

    OOO_RB_USER_LOGIN_1: str = os.getenv('RZD_OOO_RB_USER_LOGIN_1')
    OOO_RB_USER_PSWD_1: str = os.getenv('RZD_OOO_RB_USER_PSWD_1')
    OOO_RB_USER_DECLARANT_ID: int = 8


class OBORONENERGO_SETTINGS:
    """Данные ЛК Оборонэнерго."""
    PERSONAL_AREA_ID: int = 5

    PBK_USER_LOGIN_1: str = os.getenv('OBORONENERGO_PBK_USER_LOGIN_1')
    PBK_USER_PSWD_1: str = os.getenv('OBORONENERGO_PBK_USER_PSWD_1')
    PBK_USER_DECLARANT_ID: int = 1


class ROSSETI_MR_SETTINGS:
    """Данные ЛК Россети Московский регион."""
    PERSONAL_AREA_ID: int = 6

    PBK_USER_LOGIN_1: str = os.getenv('ROSSETI_MR_PBK_USER_LOGIN_1')
    PBK_USER_PSWD_1: str = os.getenv('ROSSETI_MR_PBK_USER_PSWD_1')
    PBK_USER_DECLARANT_ID: int = 1

    RB_USER_LOGIN_1: str = os.getenv('ROSSETI_MR_RB_USER_LOGIN_1')
    RB_USER_PSWD_1: str = os.getenv('ROSSETI_MR_RB_USER_PSWD_1')
    RB_USER_DECLARANT_ID: int = 2

    NEW_TOWERS_MR_USER_LOGIN_1: str = os.getenv(
        'ROSSETI_MR_NEW_TOWERS_MR_USER_LOGIN_1'
    )
    NEW_TOWERS_MR_USER_PSWD_1: str = os.getenv(
        'ROSSETI_MR_NEW_TOWERS_MR_USER_PSWD_1'
    )
    NEW_TOWERS_MR_USER_DECLARANT_ID: int = 6

    OOO_RB_USER_LOGIN_1: str = os.getenv('ROSSETI_MR_OOO_RB_USER_LOGIN_1')
    OOO_RB_USER_PSWD_1: str = os.getenv('ROSSETI_MR_OOO_RB_USER_PSWD_1')
    OOO_RB_USER_DECLARANT_ID: int = 8

    OOO_CAPITAL_POLE_USER_LOGIN_1: str = os.getenv(
        'ROSSETI_MR_OOO_CAPITAl_POLE_USER_LOGIN_1'
    )
    OOO_CAPITAL_POLE_USER_PSWD_1: str = os.getenv(
        'ROSSETI_MR_OOO_CAPITAl_POLE_USER_PSWD_1'
    )
    OOO_CAPITAL_POLE_USER_DECLARANT_ID: int = 9


db_settings = DB_SETTINGS()
portal_tp_settings = PORTAL_TP_SETTINGS()
mosoblenergo_settings = MOSOBLENERGO_SETTINGS()
sk_tatarstan_settings = SK_TATARSTAN_SETTINGS()
rzd_settings = RZD_SETTINGS()
oboronenergo_settings = OBORONENERGO_SETTINGS()
rosseti_mr_settings = ROSSETI_MR_SETTINGS()
