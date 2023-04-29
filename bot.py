from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler, current_handler

from config import Config
from ai import update, start_conversation
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from time import sleep
from sqlite import *

def set_key(key: str = None):
    def decorator(func):
        setattr(func, 'key', key)
        return func
    return decorator

async def on_startup(_):
    await start_db()

bot = Bot(Config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
previous_questions_and_answers = []
whitelist = Config.ADMINLIST + Config.WHITELIST
adminlist = Config.ADMINLIST
instructions = Config.INSTRUCTIONS

class Whitelist(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        await create(user_id=message.from_user.id)

    async def on_process_message(self, message: types.Message, data: dict):
        if message.from_user.id not in whitelist:
            await message.answer_chat_action('typing')
            sleep(1.66)
            await message.answer("I'm under development, and no one can access me, except my creator.")
            await message.answer_chat_action('choose_sticker')
            sleep(1.33)
            await message.answer_sticker("CAACAgIAAxkBAAEIvA1kSHmXeLZRAu03uPm1k8TZ54xTbAACWUAAAuCjggc35LUFXNY5gC8E")
            raise CancelHandler()

class Adminlist(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data:dict):
        await create(user_id=message.from_user.id)
    async def on_process_message(self, message: types.Message, data: dict):
        handler =  current_handler.get()
        if handler:
            key = getattr(handler, 'key', None)
            if key == 'admin':
                user_id = message.from_user.id
                if user_id not in adminlist:
                    await message.answer_chat_action('typing')
                    sleep(1.66)
                    await message.answer('У тебя нет доступа к этой команде!')
                    raise CancelHandler()

class Profile(StatesGroup):
    is_admin = State()
    no_admin = State()
    is_whitelisted = State()
    no_whitelisted = State()

# Cancel any of command
@dp.message_handler(commands='cancel', state='*')
@set_key('admin')
async def cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.answer('Ты прервал текущее действие!')

# Start the conversation with bot
@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    await message.answer_chat_action('typing')
    response = start_conversation(instructions)
    await message.answer(response)

# Add some user to whitelist
@dp.message_handler(commands='whitelistadd')
@set_key('admin')
async def whitelistadd(message: types.Message):
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.answer('Введи айди пользователя, которого хочешь добавить в вайтлист.')
    await Profile.is_whitelisted.set()

@dp.message_handler(state=Profile.is_whitelisted)
async def whitelistadd_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
        data['is_whitelisted'] = 1
        print(data)
    await edit_whitelist(state, user_id=message.text)
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.reply('Пользователь успешно добавлен в вайтлист!')
    await state.finish()

# Delete some user from whitelist
@dp.message_handler(commands='whitelistdel')
@set_key('admin')
async def whitelistdel(message: types.Message):
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.answer('Введи айди пользователя, которого хочешь удалить из вайтлиста.')
    await Profile.no_whitelisted.set()

@dp.message_handler(state=Profile.no_whitelisted)
async def whitelistdel_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
        data['is_whitelisted'] = 0
        print(data)
    await edit_whitelist(state, user_id=message.text)
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.reply('Пользователь успешно удалён из вайтлиста!')
    await state.finish()

# Add some user to adminlist
@dp.message_handler(commands='adminadd')
@set_key('admin')
async def adminadd(message: types.Message):
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.answer('Введи айди пользователя, которого хочешь сделать админом.')
    await Profile.is_admin.set()

@dp.message_handler(state=Profile.is_admin)
async def adminadd_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
        data['is_admin'] = 1
        print(data)
    await edit_admin(state, user_id=message.text)
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.reply('Пользователь успешно получил права админа!')
    await state.finish()

# Delete some user from adminlist
@dp.message_handler(commands='admindel')
@set_key('admin')
async def admindel(message: types.Message):
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.answer('Введи айди пользователя, у которого хочешь забрать права админа.')
    await Profile.no_admin.set()

@dp.message_handler(state=Profile.no_admin)
async def admindel_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
        data['is_admin'] = 0
        print(data)
    await edit_admin(state, user_id=message.text)
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.reply('У пользователя успешно отобраны права админа!')
    await state.finish()

@dp.message_handler(commands='clear')
async def clear_history(message: types.Message):
    previous_questions_and_answers.clear()
    await message.answer_chat_action('typing')
    sleep(1.66)
    await message.answer('Моя память успешно очищена, теперь я ничего не помню, ты доволен?')
    await message.answer_chat_action('choose_sticker')
    sleep(1.33)
    await message.answer_sticker('CAACAgIAAxkBAAEIxMxkTDRAFYTvAUjeNeoc3PmmYba0tQAC7QsAAnkNSEhOUKpeKsKv6i8E')

# Chatting with GPT-3.5
@dp.message_handler()
async def main(message: types.Message):
    try:
        await message.answer_chat_action('typing')
        new_question = message.text
        response = update(instructions, previous_questions_and_answers, new_question)
        previous_questions_and_answers.append((new_question, response))
        await message.answer(response)
    except Exception as e:
        print(e)
        await message.answer_chat_action('typing')
        sleep(1.66)
        await message.answer("Прости пожалуйста! Во время обработки твоего запроса произошла какая-то ошибка.")
        await message.answer_chat_action('choose_sticker')
        sleep(1.33)
        await message.answer_sticker("CAACAgIAAxkBAAEIvA9kSHs-b_bMbTJRFxkzFEFx8X5M5AACzz8AAuCjggd2g0I1aviuMS8E")
        await message.answer_chat_action('typing')
        sleep(1.66)
        await message.answer("Попробуй укоротить вопрос, очистить мне память, или, если ничего не поможет, свяжись с @SuperSuslik312")

# Bot polling
if __name__ == '__main__':
    dp.middleware.setup(Whitelist())
    dp.middleware.setup(Adminlist())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)