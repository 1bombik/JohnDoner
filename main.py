import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from private_data import TOKEN
from handler import start_handler, process_open_button, process_close_button

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.message.register(start_handler, CommandStart())
dp.callback_query.register(process_open_button, F.data == 'open')
dp.callback_query.register(process_close_button, F.data == 'close')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
