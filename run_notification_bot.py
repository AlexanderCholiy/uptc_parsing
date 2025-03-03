import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from colorama import Fore, Style, init

from app.telegram.routes.notification_route import notification_route
from settings.config import bot_telegram_settings

init(autoreset=True)

bot = Bot(
    token=bot_telegram_settings.TELEGRAM_TOKEN_1,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()


async def main():
    dp.include_routers(notification_route)
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(
                Fore.RED + Style.DIM +
                'Произошла ошибка:\n' +
                Style.RESET_ALL + str(e)
            )
            await asyncio.sleep(120)


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
        asyncio.run(main())
    except KeyboardInterrupt:
        log_completion(start_time)
        is_keyboard_interrupt = True
    finally:
        if not is_keyboard_interrupt:
            log_completion(start_time)
