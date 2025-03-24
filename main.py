import logging
import asyncio
from aiogram import Bot, Dispatcher
from configs import config
from handlers.common import common_router
from handlers.cook import cook_router
from handlers.gpt_chat import gpt_router
from handlers.random_facts import random_router
from handlers.talks import talks_router
from handlers.quiz import quiz_router


logger = logging.getLogger(__name__)
current_lang = 'ru'


async def main() -> None:
    # Настройка параметров
    token_api = config.TOKEN_BOT
    # logging.basicConfig(format='%(filename)s:%(lineno)d %(levelname)-8s [%(asctime)s] - %(name)s - %(message)s', level=logging.INFO, filename='bot.log')
    logging.basicConfig(format='%(filename)s:%(lineno)d %(levelname)-8s [%(asctime)s] - %(name)s - %(message)s', level=logging.INFO)
    logger.info('Starting up bot')
    # Создание бота и диспетчера
    bot = Bot(token=token_api)
    disp = Dispatcher()
    # Настройка рутеров
    disp.include_routers(
        gpt_router,
        cook_router,
        quiz_router,
        random_router,
        talks_router,
        common_router,
    )
    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await disp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

