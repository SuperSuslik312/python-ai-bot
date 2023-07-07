from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler, current_handler

from ai import update, start_conversation
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from asyncio import sleep
from postgresql import *

# Simple decorator for admin commands
def set_key(key: str = None):
    def decorator(func):
        setattr(func, 'key', key)
        return func
    return decorator

# Start connection with database
async def on_startup(_):
    await start_db()

bot = Bot(Config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Add user to database if he is not there
class AddUserToDB(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        await create(message.from_user.id)

# Check if the user in whitelist or not
class Whitelist(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        is_whitelisted = await read_whitelist(message.from_user.id)
        if is_whitelisted != True:
            await message.answer_chat_action('typing')
            await sleep(1.66)
            await message.answer("I'm sorry, but you're not on the whitelist.\n\nBut you can view the source code of me on [github](https://github.com/SuperSuslik312/python-ai-bot).", parse_mode=types.ParseMode.MARKDOWN)
            await message.answer_chat_action('choose_sticker')
            await sleep(1.33)
            await message.answer_sticker("CAACAgIAAxkBAAEIvA1kSHmXeLZRAu03uPm1k8TZ54xTbAACWUAAAuCjggc35LUFXNY5gC8E")
            raise CancelHandler()

# Check if the user is admin or not
class Adminlist(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        if handler:
            key = getattr(handler, 'key', None)
            if key == 'admin':
                is_admin = await read_admin(message.from_user.id)
                if is_admin != True:
                    await message.answer_chat_action('typing')
                    await sleep(1.66)
                    await message.answer('У тебя нет доступа к этой команде!')
                    raise CancelHandler()

# Temp storage
class Profile(StatesGroup):
    is_admin = State()
    no_admin = State()
    is_whitelisted = State()
    no_whitelisted = State()
    instructions = State()

# Cancel any of command
@dp.message_handler(commands='cancel', state='*')
async def cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer('Ты прервал текущее действие!')

# Start the conversation with bot
@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    instructions = await read_instructions(message.from_user.id)
    await message.answer_chat_action('typing')
    response = start_conversation(instructions)
    await message.answer(response)

# Add some user to whitelist
@dp.message_handler(commands='whitelistadd')
@set_key('admin')
async def whitelistadd(message: types.Message):
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer('Введи айди пользователя, которого хочешь добавить в вайтлист.')
    await Profile.is_whitelisted.set()

@dp.message_handler(state=Profile.is_whitelisted)
async def whitelistadd_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_whitelisted'] = True
    await edit_whitelist(state, user_id=message.text)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.reply('Пользователь успешно добавлен в вайтлист!')
    await state.finish()

# Delete some user from whitelist
@dp.message_handler(commands='whitelistdel')
@set_key('admin')
async def whitelistdel(message: types.Message):
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer('Введи айди пользователя, которого хочешь удалить из вайтлиста.')
    await Profile.no_whitelisted.set()

@dp.message_handler(state=Profile.no_whitelisted)
async def whitelistdel_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_whitelisted'] = False
    await edit_whitelist(state, user_id=message.text)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.reply('Пользователь успешно удалён из вайтлиста!')
    await state.finish()

# Add some user to adminlist
@dp.message_handler(commands='adminadd')
@set_key('admin')
async def adminadd(message: types.Message):
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer('Введи айди пользователя, которого хочешь сделать админом.')
    await Profile.is_admin.set()

@dp.message_handler(state=Profile.is_admin)
async def adminadd_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_admin'] = True
    await edit_admin(state, user_id=message.text)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.reply('Пользователь успешно получил права админа!')
    await state.finish()

# Delete some user from adminlist
@dp.message_handler(commands='admindel')
@set_key('admin')
async def admindel(message: types.Message):
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer('Введи айди пользователя, у которого хочешь забрать права админа.')
    await Profile.no_admin.set()

@dp.message_handler(state=Profile.no_admin)
async def admindel_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_admin'] = False
    await edit_admin(state, user_id=message.text)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.reply('У пользователя успешно отобраны права админа!')
    await state.finish()

# Set the system prompt for AI
@dp.message_handler(commands='setprompt')
async def setprompt(message: types.Message):
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer('Напиши в следующем сообщении что ты от меня хочешь!\n\nНапример если хочешь чтобы меня звали Куруми напиши "Тебя зовут Куруми" или "Твоё имя - Куруми" и т.д.\n\nМожешь писать несколько предложений, главное чтобы в одном сообщении!\n\nТакже ты можешь отменить это действие если нажмёшь /cancel')
    await Profile.instructions.set()

@dp.message_handler(state=Profile.instructions)
async def setprompt_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['instructions'] = message.text
    await edit_instructions(state, message.from_user.id)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer('Ты успешно задал мне поведение, спасибо!')
    await message.answer_chat_action('choose_sticker')
    await sleep(1.33)
    await message.answer_sticker('CAACAgIAAxkBAAEIyFhkTaTnTzPFtQeYx4WaRUiYJglBnwACyj8AAuCjggcUTxrEwRdNXy8E')
    await state.finish()

# Get the user ids from database that in whitelist !!! Not actually completed
@dp.message_handler(commands='whitelistget')
@set_key('admin')
async def whitelistget(message: types.Message):
    user_ids = await get_whitelist()
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer(user_ids)

# Clear the bot's memory
@dp.message_handler(commands='clear')
async def clear_history(message: types.Message):
    await clean_history(message.from_user.id)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.answer('Моя память успешно очищена, теперь я ничего не помню, ты доволен?')
    await message.answer_chat_action('choose_sticker')
    await sleep(1.33)
    await message.answer_sticker('CAACAgIAAxkBAAEIxMxkTDRAFYTvAUjeNeoc3PmmYba0tQAC7QsAAnkNSEhOUKpeKsKv6i8E')

# Chatting with GPT-3.5
@dp.message_handler()
async def main(message: types.Message):
    try:
        user_id = message.from_user.id
        await message.answer_chat_action('typing')
        new_question = message.text
        instructions = await read_instructions(user_id)
        response = await update(instructions, user_id, new_question)
        await message.answer(response)
    except Exception as e:
        print(e)
        await message.answer_chat_action('typing')
        await sleep(1.66)
        await message.answer("Прости пожалуйста! Во время обработки твоего запроса произошла какая-то ошибка.")
        await message.answer_chat_action('choose_sticker')
        await sleep(1.33)
        await message.answer_sticker("CAACAgIAAxkBAAEIvA9kSHs-b_bMbTJRFxkzFEFx8X5M5AACzz8AAuCjggd2g0I1aviuMS8E")
        await message.answer_chat_action('typing')
        await sleep(1.66)
        await message.answer("Попробуй очистить мне память, или, если это не поможет, свяжись с @SuperSuslik312 и перешли ему следующее сообщение:")
        await message.answer(e)

# Bot polling
if __name__ == '__main__':
    dp.middleware.setup(Whitelist())
    dp.middleware.setup(Adminlist())
    dp.middleware.setup(AddUserToDB())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)