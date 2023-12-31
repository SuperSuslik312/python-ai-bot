from aiogram import BaseMiddleware
from aiogram.enums import ParseMode
from aiogram.types import (
    TelegramObject,
    Message
)

from postgresql import (
    read_whitelist,
    read_admin,
    create
)


class AddUserToDB(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        user_id = event.from_user.id
        await create(user_id)
        return await handler(event, data)


# Check if the user in whitelist or not
class Whitelist(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        user_id = event.from_user.id
        result = await read_whitelist(user_id)
        if result:
            return await handler(event, data)
        else:
            if isinstance(event, Message):
                await event.answer(
                    "I'm sorry, but you're not on the whitelist.\n\nIf you want to chat with me, you can contact my "
                    "developer @SuperSuslik312 or deploy me yourself, source code is available [here]"
                    "(https://github.com/SuperSuslik312/python-ai-bot)",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            else:
                return


class AdminList(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        user_id = event.from_user.id
        result = await read_admin(user_id)
        if result:
            return await handler(event, data)
        else:
            if isinstance(event, Message):
                await event.answer(
                    "У тебя нет доступа к этой команде!"
                )
                return
            else:
                return
