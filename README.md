# AI Telegram Bot
## What is it?
* First of all, you can chat with GPT-4 model directly in Telegram **without needing an OpenAI API key**.
* All history of conversation with GPT-4 entered into database for each user separatly.
* If user want, he could clear the history of conversation with special command.
* Also this bot allows you to change the GPT-4 prompt without leaving the chat with him, right in the telegram, for each user separatly.
* In addition, it is possible to add/remove people to the white list or admin list, using the same bot.
## How to start?
1. First of all you need to install dependecies from [requirements.txt](requirements.txt)
2. Now you need to setup PostgreSQL database (you can search the internet to find out how to do that)
3. Copy the [config.example.py](config.example.py) to **config.py**, and change the default values to yours.
4. Now you can start the bot with
```console
$ python3 -u bot.py
```
## Dependecies
* [aiogram](https://github.com/aiogram/aiogram)
* [asyncpg](https://github.com/MagicStack/asyncpg)
* [gpt4free](https://github.com/xtekky/gpt4free)
# License notice
Copyright (C) 2024  SuperSuslik312

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
