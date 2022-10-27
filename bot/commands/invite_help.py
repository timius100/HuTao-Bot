from vkbottle.bot import Blueprint, Message

from config import GROUP_ID

bp = Blueprint("Invite event")
bp.labeler.vbml_ignore_case = True

HELP_LINK = "https://github.com/timius100/HuTao-Bot#команды"


@bp.on.message(action="chat_invite_user")
async def invite_event_reaction(message: Message):
    """React when bot is invited to a chat"""
    if message.action.member_id == -GROUP_ID:
        return (
            "Добро пожаловать в Тейват!\n"
            "Теперь мне необходимо дать права на чтение сообщений "
            "и админку для корректной работы!\n"
            "Репозиторий со всеми командами:\n"
            + HELP_LINK
        )


@bp.on.message(text="!помощь")
async def help_handler(message: Message):
    await message.answer(
        "Основные команыды:\n"
        "!начать - создать профиль\n"
        "!перс - просмотреть персонажа\n"
        "!установить ник [никнейм] - устанавливает ник для вашего персонажа\n"
        "Все остальные команды можно посмотреть в репозитории:\n"
        + HELP_LINK,
        attachment="photo-193964161_457239344"
    )


@bp.on.private_message(text="Начать")
async def start_private_handler(message: Message):
    """
    This handler only works in private messages
    """
    return (
        "Что бы я начал работать, меня надо добавить в любую беседу, и выдать "
        "там доступ к переписке!\n"
        "Команды можно посмотреть тут:\n"
        + HELP_LINK
    )
