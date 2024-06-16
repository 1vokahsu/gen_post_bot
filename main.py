import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.config import config
from handlers import basic
from aiogram.fsm.storage.redis import RedisStorage


async def run_bot():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(token=config.bot_token.get_secret_value(),
              parse_mode='HTML')
    storage = RedisStorage.from_url('redis://localhost:6379/0')
    dp = Dispatcher(bot=bot, storage=storage)
    await bot.delete_webhook(drop_pending_updates=True)
    # dp.startup.register(set_main_menu)
    dp.include_router(basic.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_bot())
