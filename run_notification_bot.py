import asyncio
from datetime import datetime

from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from colorama import Fore, Style, init

from settings.config import bot_telegram_settings
from app.telegram.routes.notification_route import notification_route


init(autoreset=True)

bot = Bot(
    token=bot_telegram_settings.TELEGRAM_TOKEN_1,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()


async def main():
    dp.include_routers(notification_route)
    await dp.start_polling(bot)


if __name__ == '__main__':
    start_time = datetime.now()
    print(Fore.MAGENTA + Style.BRIGHT + f'Запуск {__file__}')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        bot_delta_time = datetime.now() - start_time
        bot_delta_time = round(bot_delta_time.total_seconds())
        print(
            Fore.MAGENTA + Style.BRIGHT +
            f'Завершение {__file__} (Δt: {bot_delta_time} c).'
        )
