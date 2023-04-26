from config import Config
from ai import update
from aiogram import Bot, Dispatcher, executor, types
from time import sleep

bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher(bot)
previous_questions_and_answers = []
whitelist = Config.WHITELIST
adminlist = Config.ADMINLIST
instructions = Config.INSTRUCTIONS

@dp.message_handler()
async def main(message: types.Message):
        user_id = message.from_user.id
        try:
            if user_id in whitelist or adminlist:
                await message.answer_chat_action('typing')
                new_question = message.text
                response = update(instructions, previous_questions_and_answers, new_question)
                previous_questions_and_answers.append((new_question, response))
                await message.answer(response)
            else:
                await message.answer_chat_action('typing')
                sleep(1.66)
                await message.answer("I'm under development, and no one can access me, except my creator.")
                await message.answer_chat_action('choose_sticker')
                sleep(1.33)
                await message.answer_sticker("CAACAgIAAxkBAAEIvA1kSHmXeLZRAu03uPm1k8TZ54xTbAACWUAAAuCjggc35LUFXNY5gC8E")
        except:
            await message.answer_chat_action('typing')
            sleep(1.99)
            await message.answer("I'm sorry, but some error happened during handling your request.")
            await message.answer_chat_action('typing')
            sleep(1.33)
            await message.answer_sticker("CAACAgIAAxkBAAEIvA9kSHs-b_bMbTJRFxkzFEFx8X5M5AACzz8AAuCjggd2g0I1aviuMS8E")
            await message.answer_chat_action('typing')
            sleep(1.66)
            await message.answer("Try to shorten your question.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)