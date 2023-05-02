# AI Telegram Bot
## What is it?
* First of all, you can chat with GPT-3.5 model directly in telegram.
* All history of conversation with GPT-3.5 entered into database for each user separatly.
* If user want, he could clear the history of conversation with special command.
* Also this bot allows you to change the GPT-3.5 prompt without leaving the chat with him, right in the telegram, for each user separatly.
* In addition, it is possible to add/remove people to the white list or admin list, using the same bot.
## How to start?
1. First of all, you need to install dependecies from [requirements.txt](requirements.txt)
2. Now you need to setup PostgreSQL database (you can search the internet to find out how to do that)
3. Copy the [config.example.py](config.example.py) to **config.py**, and change the default values to yours.
4. Now you can start the bot with
```console
$ python3 -u bot.py
```
## Dependecies
* [aiogram](https://github.com/aiogram/aiogram)
* [asyncpg](https://github.com/MagicStack/asyncpg)
* [openai](https://github.com/openai/openai-python)
# Licenses
* This work - [GNU AGPL-3.0](LICENSE.md)
* aiogram & openai - MIT license
* asyncpg - Apache 2.0 license
