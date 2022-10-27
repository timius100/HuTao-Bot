import asyncio
from os import mkdir, path

from loguru import logger
from vkbottle import load_blueprints_from_package
from vkbottle.bot import Bot

import create_pool
from config import VK_GROUP_TOKEN

# TODO: Image generation (wishes)

if __name__ == "__main__":
    log_path = "logs/"
    if not path.exists(log_path):
        mkdir(log_path)
    logger.add("logs/file_{time}.log", level="INFO", rotation="10 MB")

    bot = Bot(token=VK_GROUP_TOKEN)

    for bp in load_blueprints_from_package("commands"):
        bp.load(bot)

    # Create asyncpg pool
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(create_pool.init())

    # Run bot
    bot.run_forever()
