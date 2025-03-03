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


class BOT_EMAIL_SETTINGS:
    """Почта бота."""
    EMAIL_SERVER: str = os.getenv("EMAIL_SERVER")
    BOT_EMAIL_LOGIN_1: str = os.getenv("BOT_EMAIL_LOGIN_1")
    BOT_EMAIL_PSWD_1: str = os.getenv("BOT_EMAIL_PSWD_1")


class BOT_TELEGRAM_SETTINGS:
    """Telegram бот для уведомлений"""
    TELEGRAM_TOKEN_1: str = os.getenv("TELEGRAM_TOKEN_1")
    TELEGRAM_GROUP_ID_1: int = int(os.getenv("TELEGRAM_GROUP_ID_1"))


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

    NB_MR_PBK_RB_HARDENERGY_USER_LOGIN_1: str = os.getenv(
        'MOSOBLENERGO_NB_MR_PBK_RB_HARDENERGY_USER_LOGIN_1'
    )
    NB_MR_PBK_RB_HARDENERGY_DECLARANT_ID: int = 20

    NB_MR_PBK_RB_PROMISING_TECH_USER_LOGIN_1: str = os.getenv(
        'MOSOBLENERGO_NB_MR_PBK_RB_PROMISING_TECH_USER_LOGIN_1'
    )
    NB_MR_PBK_RB_PROMISING_TECH_DECLARANT_ID: int = 21


class SK_TATARSTAN_SETTINGS:
    """Данные ЛК АО «Сетевая компания» Республики Татарстан."""
    PERSONAL_AREA_ID: int = 3

    PBK_USER_LOGIN_1: str = os.getenv('SK_TATARSTAN_PBK_USER_LOGIN_1')
    PBK_USER_PSWD_1: str = os.getenv('SK_TATARSTAN_PBK_USER_PSWD_1')
    PBK_USER_DECLARANT_ID: int = 1


class RZD_SETTINGS:
    """Данные ЛК РЖД."""
    PERSONAL_AREA_ID: int = 4

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
    # ---
    NB_MR_SRK_TELECOM_1: str = os.getenv(
        'ROSSETI_MR_NB_MR_SRK_TELECOM_1'
    )
    NB_MR_SRK_TELECOM_PSWD_1: str = os.getenv(
        'ROSSETI_MR_NB_MR_SRK_TELECOM_PSWD_1'
    )
    NB_MR_SRK_TELECOM_USER_DECLARANT_ID: int = 11

    PBK_SRK_TELECOM_1: str = os.getenv(
        'ROSSETI_MR_PBK_SRK_TELECOM_1'
    )
    PBK_SRK_TELECOM_PSWD_1: str = os.getenv(
        'ROSSETI_MR_PBK_SRK_TELECOM_PSWD_1'
    )
    PBK_SRK_TELECOM_USER_DECLARANT_ID: int = 12

    RB_SRK_TELECOM_1: str = os.getenv(
        'ROSSETI_MR_RB_SRK_TELECOM_1'
    )
    RB_SRK_TELECOM_PSWD_1: str = os.getenv(
        'ROSSETI_MR_RB_SRK_TELECOM_PSWD_1'
    )
    RB_SRK_TELECOM_USER_DECLARANT_ID: int = 13
    # ---
    NB_MR_HARDENERGY_1: str = os.getenv(
        'ROSSETI_MR_NB_MR_HARDENERGY_1'
    )
    NB_MR_HARDENERGY_PSWD_1: str = os.getenv(
        'ROSSETI_MR_NB_MR_HARDENERGY_PSWD_1'
    )
    NB_MR_HARDENERGY_USER_DECLARANT_ID: int = 14

    PBK_HARDENERGY_1: str = os.getenv(
        'ROSSETI_MR_PBK_HARDENERGY_1'
    )
    PBK_HARDENERGY_PSWD_1: str = os.getenv(
        'ROSSETI_MR_PBK_HARDENERGY_PSWD_1'
    )
    PBK_HARDENERGY_USER_DECLARANT_ID: int = 15

    RB_HARDENERGY_1: str = os.getenv(
        'ROSSETI_MR_RB_HARDENERGY_1'
    )
    RB_HARDENERGY_PSWD_1: str = os.getenv(
        'ROSSETI_MR_RB_HARDENERGY_PSWD_1'
    )
    RB_HARDENERGY_USER_DECLARANT_ID: int = 16
    # ---
    NB_MR_PBK_RB_PROMISING_TECH_1: str = os.getenv(
        'ROSSETI_MR_NB_MR_PBK_RB_PROMISING_TECH_1'
    )
    NB_MR_PBK_RB_PROMISING_TECH_PSWD_1: str = os.getenv(
        'ROSSETI_MR_NB_MR_PBK_RB_PROMISING_TECH_PSWD_1'
    )
    NB_MR_PBK_RB_PROMISING_TECH_USER_DECLARANT_ID: int = 17

    PBK_PMK_1: str = os.getenv(
        'ROSSETI_MR_PBK_PMK_1'
    )
    PBK_PMK_PSWD_1: str = os.getenv(
        'ROSSETI_MR_PBK_PMK_PSWD_1'
    )
    PBK_PMK_USER_DECLARANT_ID: int = 18

    PBK_INFRASCOM_1: str = os.getenv(
        'ROSSETI_MR_PBK_INFRASCOM_1'
    )
    PBK_INFRASCOM_PSWD_1: str = os.getenv(
        'ROSSETI_MR_PBK_INFRASCOM_PSWD_1'
    )
    PBK_INFRASCOM_USER_DECLARANT_ID: int = 19


db_settings = DB_SETTINGS()

bot_email_settings = BOT_EMAIL_SETTINGS()
bot_telegram_settings = BOT_TELEGRAM_SETTINGS()

portal_tp_settings = PORTAL_TP_SETTINGS()
mosoblenergo_settings = MOSOBLENERGO_SETTINGS()
sk_tatarstan_settings = SK_TATARSTAN_SETTINGS()
rzd_settings = RZD_SETTINGS()
oboronenergo_settings = OBORONENERGO_SETTINGS()
rosseti_mr_settings = ROSSETI_MR_SETTINGS()
