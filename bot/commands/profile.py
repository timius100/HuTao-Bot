from vkbottle.bot import Blueprint, Message
from vkbottle.http import AiohttpClient
from loguru import logger
from player_exists import exists
from utils import get_default_header
import create_pool

bp = Blueprint("Profile")
bp.labeler.vbml_ignore_case = True


@bp.on.chat_message(text=("!персонаж", "!перс"))
async def profile(message: Message):
    if not await exists(message):
        return
    pool = create_pool.pool
    async with pool.acquire() as pool:
        result = await pool.fetchrow(
            "SELECT "
            "nickname, "
            "primogems, "
            "standard_wishes, "
            "event_wishes, "
            "legendary_rolls_standard, "
            "legendary_rolls_event, "
            "uid "
            "FROM players WHERE user_id=$1 and peer_id=$2",
            message.from_id, message.peer_id
        )

    nickname = result["nickname"]
    primogems = result["primogems"]
    standard_wishes = result["standard_wishes"]
    event_wishes = result["event_wishes"]
    legendary_standard_guarantee = result["legendary_rolls_standard"]
    legendary_event_guarantee = result["legendary_rolls_event"]
    UID = result["uid"]

    return (
        f"&#128100; Ник: {nickname}\n"
        f"&#129689; Примогемы: {primogems}\n"
        f"&#127852; Стандартных молитв: {standard_wishes}\n"
        f"&#127846; Молитв события: {event_wishes}\n\n"

        f"&#10133; Гарант в стандартном баннере: {legendary_standard_guarantee}\n"
        f"&#10133; Гарант в ивентовом баннере: {legendary_event_guarantee}\n\n"

        f"&#128100; Айди в Genshin Impact: {UID}"
    )


@bp.on.chat_message(text=("!геншин инфо", "!геншин инфо <UID:int>"))
async def genshin_info(message: Message, UID: int = None):
    if not await exists(message):
        return

    if UID is None:
        pool = create_pool.pool
        async with pool.acquire() as pool:
            UID = await pool.fetchrow(
                "SELECT uid FROM players WHERE user_id=$1 AND peer_id=$2",
                message.from_id, message.peer_id
            )

        if UID is None:
            return (
                "Вы не установили свой UID! "
                "Его можно установить с помощью команды \"!установить айди <UID>\""
            )

        UID = UID['uid']

    http_client = AiohttpClient()

    try:
        player_info = await http_client.request_json(
            f"https://enka.network/u/{UID}/__data.json",
            headers=get_default_header()
        )
        logger.info(f"https://enka.network/u/{UID}/__data.json вернул это: {player_info}")
    except Exception as e:
        logger.error(e)
        return (
            "Похоже, что сервис enka.network сейчас не работает!\n"
            "Если же это не так, пожалуйста, сообщите об этой ошибке [id322615766|мне]"
        )

    if len(player_info) == 0:
        return (
            "Ээээ... Информацию об этом UID не получилось найти, "
            "похоже этот аккаунт в геншине был забанен/удален\n"
            "(или это ошибка enka.network)"
        )

    try:
        player_info = player_info['playerInfo']
        nickname = player_info['nickname']
        adv_rank = player_info['level']
        signature = player_info['signature']
        world_level = player_info['worldLevel']
    except KeyError as e:
        logger.error(e)
        return "Похоже, что enka.network изменил свое апи, попробуйте позже"

    return (
        f"Айди в Genshin Impact: {UID}\n"
        f"Ник: {nickname}\n"
        f"Ранг приключений: {adv_rank}\n"
        f"Описание: \"{signature}\"\n"
        f"Уровень мира: {world_level}"
    )
