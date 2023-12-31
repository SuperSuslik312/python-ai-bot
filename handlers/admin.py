from asyncio import sleep

from aiogram import (
    types,
    Router,
    F,
    Bot
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State
)
from aiogram.utils.chat_action import ChatActionSender

from config import Config
from middlewares import (
    AddUserToDB,
    Whitelist,
    AdminList
)
from postgresql import (
    edit_whitelist,
    edit_admin,
    get_whitelist
)
from keyboards import *

bot = Bot(Config.BOT_TOKEN)
router = Router()
router.message.middleware(AddUserToDB())
router.message.middleware(Whitelist())
router.message.middleware(AdminList())
router.callback_query.middleware(Whitelist())
router.callback_query.middleware(AdminList())


class Profile(StatesGroup):
    is_admin = State()
    no_admin = State()
    is_whitelisted = State()
    no_whitelisted = State()


@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    await message.answer(text='Добро пожаловать, админ', reply_markup=admin_keyboard())


@router.callback_query(F.data.startswith("admin_"))
async def admin_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    if action == 'add-whitelist':
        await state.set_state(Profile.is_whitelisted)
        await callback.message.edit_text(text="Введи айди пользователя, которого хочешь добавить в вайтлист.",
                                         reply_markup=admin_keyboard_cancel())
    elif action == 'del-whitelist':
        await state.set_state(Profile.no_whitelisted)
        await callback.message.edit_text(text="Введи айди пользователя, которого хочешь удалить из вайтлиста.",
                                         reply_markup=admin_keyboard_cancel())
    elif action == 'add-admin':
        await state.set_state(Profile.is_admin)
        await callback.message.edit_text(text="Введи айди пользователя, которого хочешь сделать админом.",
                                         reply_markup=admin_keyboard_cancel())
    elif action == 'del-admin':
        await state.set_state(Profile.no_admin)
        await callback.message.edit_text(text="Введи айди пользователя, у которого хочешь забрать права админа.",
                                         reply_markup=admin_keyboard_cancel())
    elif action == 'cancel':
        await state.clear()
        await callback.message.edit_text(text="Предыдущее действие отменено!\nВыбери другое",
                                         reply_markup=admin_keyboard())
    elif action == 'cancel-panel':
        await callback.message.delete()
    
    
@router.message(Profile.is_whitelisted)
async def whitelist_add(message: types.Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(is_whitelisted=True)
        await edit_whitelist(state, user_id=int(message.text))
        await sleep(1.66)
        await message.reply('Пользователь успешно добавлен в вайтлист!')
        await state.clear()


@router.message(Profile.no_whitelisted)
async def whitelist_del(message: types.Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(is_whitelisted=False)
        await edit_whitelist(state, user_id=int(message.text))
        await sleep(1.66)
        await message.reply('Пользователь успешно удалён из вайтлиста!')
        await state.clear()


@router.message(Profile.is_admin)
async def admin_add(message: types.Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(is_admin=True)
        await edit_admin(state, user_id=int(message.text))
        await sleep(1.66)
        await message.reply('Пользователь успешно получил права админа!')
        await state.clear()


@router.message(Profile.no_admin)
async def admin_del(message: types.Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(is_admin=False)
        await edit_admin(state, user_id=int(message.text))
        await sleep(1.66)
        await message.reply('У пользователя успешно отобраны права админа!')
        await state.clear()


@router.message(Command('whitelistget'))
async def whitelist_get(message: types.Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_ids = await get_whitelist()
        await sleep(1.66)
        await message.answer(user_ids)
