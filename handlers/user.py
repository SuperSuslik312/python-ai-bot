import base64
import io
from asyncio import sleep

from aiogram import (
    types,
    Router,
    F,
    Bot
)
from aiogram.enums import ParseMode
from aiogram.filters import (
    Command,
    CommandStart
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (
    StatesGroup,
    State
)
from aiogram.types import ErrorEvent
from aiogram.utils.chat_action import (
    ChatActionSender,
    logger
)

from ai import *
from middlewares import (
    AddUserToDB,
    Whitelist
)
from keyboards import *
from postgresql import (
    clean_history,
    reset_instructions,
    edit_instructions,
    read_instructions
)

bot = Bot(Config.BOT_TOKEN)
router = Router()
router.message.middleware(AddUserToDB())
router.message.middleware(Whitelist())
router.callback_query.middleware(Whitelist())


class Profile(StatesGroup):
    instructions = State()


@router.message(CommandStart())
async def start_bot(message: types.Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        instructions = await read_instructions(message.from_user.id)
        response = await start_conversation(instructions)
        await message.answer(response)


@router.message(Command('menu'))
async def user_menu(message: types.Message):
    await message.answer(text="Выбери действие, ня", reply_markup=user_keyboard())


@router.callback_query(F.data.startswith("user_"))
async def user_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    if action == "clear":
        await callback.message.edit_text(text="Ты уверен? Пожалуйста не надо, я же всё забуду😭",
                                         reply_markup=user_keyboard_foolproof_his())
    elif action == 'confirm-his':
        await clean_history(callback.from_user.id)
        await callback.message.edit_text(text="Ты стёр мне память, за что ты так со мной?😢",
                                         reply_markup=user_keyboard_cancel())
    elif action == 'set-prompt':
        await state.set_state(Profile.instructions)
        await callback.message.edit_text(text='Напиши в следующем сообщении что ты от меня хочешь!\n\nНапример если '
                                              'хочешь чтобы меня звали Куруми напиши "Тебя зовут Куруми" или "Твоё '
                                              'имя - Куруми" и т.д.\n\nМожешь писать несколько предложений, '
                                              'главное чтобы в одном сообщении!\n\n'
                                              'Если хочешь отменить, просто нажми "Назад"',
                                         reply_markup=user_keyboard_cancel())
    elif action == 'reset-prompt':
        await callback.message.edit_text(text="Ты уверен в своём решении?",
                                         reply_markup=user_keyboard_foolproof_ins())
    elif action == 'confirm-ins':
        await reset_instructions(callback.from_user.id)
        await callback.message.edit_text(
            text="Моё поведение сброшено до заводского, не знаю, радоваться или плакать...",
            reply_markup=user_keyboard_cancel())
    elif action == 'cancel' or action == 'no-confirm-his' or action == 'no-confirm-ins':
        await state.clear()
        await callback.message.edit_text(text="Выбери действие, ня",
                                         reply_markup=user_keyboard())
    elif action == 'cancel-panel':
        await callback.message.delete()


@router.message(Profile.instructions)
async def set_prompt(message: types.Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(instructions=message.text)
        await edit_instructions(state, message.from_user.id)
        await sleep(1.66)
        await message.answer('Ты успешно задал мне поведение, спасибо!')
        await sleep(1.33)
        await message.answer_sticker('CAACAgIAAxkBAAEIyFhkTaTnTzPFtQeYx4WaRUiYJglBnwACyj8AAuCjggcUTxrEwRdNXy8E')
        await state.clear()


@router.message(F.text)
async def main_handler(message: types.Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_id = message.from_user.id
        new_question = message.caption if message.caption else message.text
        instructions = await read_instructions(user_id)
        response = await update(instructions, user_id, new_question, None)
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)


@router.message(F.photo)
async def photo_handler(message: types.Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_id = message.from_user.id
        new_question = message.caption
        instructions = await read_instructions(user_id)
        photo_id = message.photo[-1].file_id
        photo = await bot.get_file(photo_id)
        photo_path = photo.file_path
        result: io.BytesIO = await bot.download_file(photo_path)
        photo_base64 = base64.b64encode(result.getvalue()).decode('utf-8')
        photo_uri = f"data:image/jpeg;base64,{photo_base64}"
        response = await update(instructions, user_id, new_question, photo_uri)
        result.close()
        await message.answer(response, parse_mode=ParseMode.MARKDOWN)


@router.error(F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: types.Message):
    logger.critical("Critical error caused by %s", event.exception, exc_info=True)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id, interval=1):
        await sleep(1.66)
        await message.answer("Прости пожалуйста! Во время обработки твоего запроса произошла какая-то ошибка.")
        await sleep(1.33)
        await message.answer_sticker("CAACAgIAAxkBAAEIvA9kSHs-b_bMbTJRFxkzFEFx8X5M5AACzz8AAuCjggd2g0I1aviuMS8E")
        await sleep(1.66)
        await message.answer("Попробуй очистить мне память, или, если это не поможет, свяжись с @SuperSuslik312 и "
                             "перешли ему следующее сообщение:")
        await message.answer(f"Critical error caused by\n\n{event.exception}")
