import random
import time

from loguru import logger
from vkbottle.bot import BotLabeler, Message, rules

import create_pool
from item_names import ADVENTURE_EXP, PRIMOGEM
from utils import count_quests_time, exists, exp_to_level, get_item, give_exp, give_item

bl = BotLabeler()
bl.auto_rules = [rules.PeerRule(from_chat=True)]
bl.vbml_ignore_case = True


@bl.message(text=(
    "!начать поручения", "[<!>|<!>] Начать поручения"
))
async def start_daily_quests(message: Message):
    """
    Player will be able to start quests only if:
    He is registered;
    doing_quest == False;
    daily_quests_time + 86400 seconds (24 hours) < current unix time
    """
    if not await exists(message):
        return
    pool = create_pool.pool
    async with pool.acquire() as pool:
        result = await pool.fetchrow(
            "SELECT "
            "daily_quests_time, "
            "doing_quest, "
            "inventory "
            "FROM players WHERE user_id=$1 AND peer_id=$2",
            message.from_id, message.peer_id
        )
        started_time: int = result['daily_quests_time']
        doing_quest: int = result['doing_quest']

        if started_time + 86400 < int(time.time()) and doing_quest is False:
            logger.info(f"{message.from_id} начал поручения в беседе {message.peer_id}")
            await pool.execute(
                "UPDATE players SET "
                "daily_quests_time=$1, "
                "doing_quest=true "
                "WHERE user_id=$2 AND peer_id=$3",
                int(time.time()), message.from_id, message.peer_id,
            )

            experience = await get_item(ADVENTURE_EXP, message.from_id, message.peer_id)
            quest_time = count_quests_time(experience['count'])
            return (
                "Вы начали выполнять поручения. "
                f"Возвращайтесь через {int(quest_time/60)} минут"
                f"{'у' if quest_time/60 == 1.0 else 'ы' if quest_time/60 < 5.0 else ''}!"
            )
        else:
            return (
                "Вы уже начали поручения или выполнили их!"
            )


@bl.message(text=(
    "!закончить поручения",
    "!завершить поручения",
    "[<!>|<!>] Завершить поручения"
))
async def complete_daily_quests(message: Message):
    """
    Player will be able to end quests only if: 
        He is registered;
        doing_quest == true;
        daily_quests_time + 1200 seconds (20 minutes) < current unix time
    """
    if not await exists(message):
        return
    pool = create_pool.pool
    async with pool.acquire() as pool:
        result = await pool.fetchrow(
            "SELECT "
            "daily_quests_time, "
            "doing_quest, "
            "inventory "
            "FROM players WHERE user_id=$1 AND peer_id=$2",
            message.from_id, message.peer_id
        )

        started_time: int = result['daily_quests_time']
        doing_quest: int = result['doing_quest']

        experience = await get_item(ADVENTURE_EXP, message.from_id, message.peer_id)
        quest_time = count_quests_time(experience['count'])

        if started_time + quest_time < int(time.time()):
            if doing_quest:
                primogems_reward = random.randint(160, 1600)
                experience_reward = random.randint(1200, 1700)
                logger.info(f"{message.from_id} закончил поручения в беседе {message.peer_id}")
                await pool.execute(
                    "UPDATE players SET doing_quest=false "
                    "WHERE user_id=$1 AND peer_id=$2",
                    message.from_id, message.peer_id
                )
                await give_exp(experience_reward, message.from_id, message.peer_id, message.ctx_api)
                await give_item(message.from_id, message.peer_id, PRIMOGEM, primogems_reward)

                return (
                    "Сегодня Катерина выплатила вам премию в размере "
                    f"{primogems_reward} примогемов и {experience_reward} опыта!"
                )
            else:
                return (
                    "Вы не начали поручения/уже выполнили их!"
                )
        else:
            seconds_left = started_time+quest_time-int(time.time())
            minutes_left = int(seconds_left/60)
            if minutes_left > 0:
                ending = f"{minutes_left} минут"
            else:
                ending = f"{seconds_left} секунд"
            return (
                "Вы сможете закончить поручения только через "
                f"{ending}!"
            )
