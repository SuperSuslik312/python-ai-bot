from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler, current_handler

from ai import update, start_conversation
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from asyncio import sleep
from postgresql import *

from keyboards import ikb_admin, ikb_user, ikb_cancel_admin, ikb_cancel_user, ikb_confirm_his, ikb_confirm_ins


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
        if not is_whitelisted:
            await message.answer_chat_action('typing')
            await sleep(1.66)
            await message.answer(
                "I'm sorry, but you're not on the whitelist.\n\nIf yout want to chat with me, you can contact my "
                "developer @SuperSuslik312 or deploy me yourself, source code is available [here]"
                "(https://github.com/SuperSuslik312/python-ai-bot)",
                parse_mode=types.ParseMode.MARKDOWN)
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
                if not is_admin:
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


# Start the conversation with bot
@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    instructions = await read_instructions(message.from_user.id)
    await message.answer_chat_action('typing')
    response = await start_conversation(instructions)
    await message.answer(response)


@dp.message_handler(commands='menu')
async def user_menu(message: types.Message):
    await message.answer(text="Выбери действие, ня",
                         reply_markup=ikb_user)


# Admin panel
@dp.message_handler(commands='admin')
@set_key('admin')
async def admin_panel(message: types.Message):
    await message.answer(text='Добро пожаловать, админ',
                         reply_markup=ikb_admin)


@dp.callback_query_handler(state='*')
async def admin_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'add_whitelist':
        await callback.message.edit_text(text="Введи айди пользователя, которого хочешь добавить в вайтлист.",
                                         reply_markup=ikb_cancel_admin)
        await Profile.is_whitelisted.set()
    elif callback.data == 'del_whitelist':
        await callback.message.edit_text(text="Введи айди пользователя, которого хочешь удалить из вайтлиста.",
                                         reply_markup=ikb_cancel_admin)
        await Profile.no_whitelisted.set()
    elif callback.data == 'add_admin':
        await callback.message.edit_text(text="Введи айди пользователя, которого хочешь сделать админом.",
                                         reply_markup=ikb_cancel_admin)
        await Profile.is_admin.set()
    elif callback.data == 'del_admin':
        await callback.message.edit_text(text="Введи айди пользователя, у которого хочешь забрать права админа.",
                                         reply_markup=ikb_cancel_admin)
        await Profile.no_admin.set()
    elif callback.data == 'cancel_admin':
        await state.finish()
        await callback.message.edit_text(text="Предыдущее действие отменено!\nВыбери другое",
                                         reply_markup=ikb_admin)
    elif callback.data == 'clear':
        await callback.message.edit_text(text="Ты уверен? Пожалуйста не надо, я же всё забуду😭",
                                         reply_markup=ikb_confirm_his)
    elif callback.data == 'confirm_his':
        await clean_history(callback.from_user.id)
        await callback.message.edit_text(text="Ты стёр мне память, за что ты так со мной?😢",
                                         reply_markup=ikb_cancel_user)
    elif callback.data == 'set_prompt':
        await callback.message.edit_text(text='Напиши в следующем сообщении что ты от меня хочешь!\n\nНапример если '
                                              'хочешь чтобы меня звали Куруми напиши "Тебя зовут Куруми" или "Твоё '
                                              'имя - Куруми" и т.д.\n\nМожешь писать несколько предложений, '
                                              'главное чтобы в одном сообщении!\n\n'
                                              'Если хочешь отменить, просто нажми "Назад"',
                                         reply_markup=ikb_cancel_user)
        await Profile.instructions.set()
    elif callback.data == 'reset_prompt':
        await callback.message.edit_text(text="Ты уверен в своём решении?",
                                         reply_markup=ikb_confirm_ins)
    elif callback.data == 'confirm_ins':
        await reset_instructions(callback.from_user.id)
        await callback.message.edit_text(text="Моё поведение сброшено до заводского, не знаю, радоваться или плакать...",
                                         reply_markup=ikb_cancel_user)
    elif callback.data == 'cancel_user' or callback.data == 'no_confirm_his' or callback.data == 'no_confirm_ins':
        await state.finish()
        await callback.message.edit_text(text="Выбери действие, ня",
                                         reply_markup=ikb_user)
    elif callback.data == 'cancel_panel':
        await callback.message.delete()


@dp.message_handler(state=Profile.is_whitelisted)
async def whitelistadd_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_whitelisted'] = True
    await edit_whitelist(state, user_id=message.text)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.reply('Пользователь успешно добавлен в вайтлист!')
    await state.finish()


@dp.message_handler(state=Profile.no_whitelisted)
async def whitelistdel_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_whitelisted'] = False
    await edit_whitelist(state, user_id=message.text)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.reply('Пользователь успешно удалён из вайтлиста!')
    await state.finish()


@dp.message_handler(state=Profile.is_admin)
async def adminadd_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_admin'] = True
    await edit_admin(state, user_id=message.text)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.reply('Пользователь успешно получил права админа!')
    await state.finish()


@dp.message_handler(state=Profile.no_admin)
async def admindel_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_admin'] = False
    await edit_admin(state, user_id=message.text)
    await message.answer_chat_action('typing')
    await sleep(1.66)
    await message.reply('У пользователя успешно отобраны права админа!')
    await state.finish()


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


# Chatting with GPT-3.5
@dp.message_handler()
async def main(message: types.Message):
    try:
        user_id = message.from_user.id
        await message.answer_chat_action('typing')
        new_question = message.text
        instructions = await read_instructions(user_id)
        response = await update(instructions, user_id, new_question)
        await message.answer(response, parse_mode=types.ParseMode.MARKDOWN)
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
        await message.answer("Попробуй очистить мне память, или, если это не поможет, свяжись с @SuperSuslik312 и "
                             "перешли ему следующее сообщение:")
        await message.answer(e)


# Bot polling
if __name__ == '__main__':
    dp.middleware.setup(Whitelist())
    dp.middleware.setup(Adminlist())
    dp.middleware.setup(AddUserToDB())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
