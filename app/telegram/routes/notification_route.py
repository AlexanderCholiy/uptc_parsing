import os
import sys

import asyncio
import pandas as pd
from aiogram import Router

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from app.common.prepare_notification import prepare_notification  # noqa: E402


DELAY: int = 3600
notification_route = Router()


async def send_notification():
    from run_notification_bot import bot, bot_telegram_settings
    while True:
        await asyncio.sleep(DELAY)
        df = prepare_notification()

        if df.empty:
            continue

        df['timestamp'] = pd.to_datetime(
            df['timestamp']
        ).dt.strftime('%Y-%m-%d %H:%M')
        df['timestamp'] = df['timestamp'].astype(str)

        filtered_df: pd.DataFrame = (
            df[~df['is_send']].reset_index(drop=True)
        )

        if len(filtered_df) == 0:
            continue
        
        filtered_df = filtered_df.rename(
            columns={
                'timestamp': 'Дата и время',
                'source': 'Скрипт',
                'executor': 'Заявитель',
                'result': 'Статус',
            }
        )
        del filtered_df['is_send']
        # Нельзя в tg отправить слишком длинное сообщение:
        rows_per_part = 20
        for i in range(0, len(filtered_df), rows_per_part):
            part_df: pd.DataFrame = filtered_df.iloc[i:i + rows_per_part]
            part_df = part_df.to_markdown(index=False, tablefmt='plain')
            text = f"*Результаты парсинга:*```\n{part_df}\n```\n"
            await bot.send_message(
                bot_telegram_settings.TELEGRAM_GROUP_ID_1, text
            )


@notification_route.startup()
async def start_send_notification():
    asyncio.create_task(send_notification())
