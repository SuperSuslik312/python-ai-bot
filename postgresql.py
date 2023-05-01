import asyncpg
from config import Config

database = Config.DB_NAME
user = Config.DB_USER
password = Config.DB_PASS
host = Config.DB_HOST
port = Config.DB_PORT
instructions = Config.INSTRUCTIONS

async def start_db():
    global db
    db = await asyncpg.connect(database=database, user=user, password=password, host=host, port=port)
    await db.execute("CREATE TABLE IF NOT EXISTS profile(user_id INTEGER PRIMARY KEY, is_admin BOOL NOT NULL, is_whitelisted BOOL NOT NULL, instructions TEXT, history TEXT)")

async def create(user_id):
    user = await db.fetch(f"SELECT 1 FROM profile WHERE user_id = '{user_id}'")
    if not user:
        await db.execute(f"INSERT INTO profile VALUES('{user_id}', False, False, '{instructions}', '')")

async def edit_admin(state, user_id):
    async with state.proxy() as data:
        await db.execute(f"UPDATE profile SET is_admin = '{data['is_admin']}' WHERE user_id = '{user_id}'")

async def edit_whitelist(state, user_id):
    async with state.proxy() as data:
        await db.execute(f"UPDATE profile SET is_whitelisted = '{data['is_whitelisted']}' WHERE user_id = '{user_id}'")

async def edit_instructions(state, user_id):
    async with state.proxy() as data:
        await db.execute(f"UPDATE profile SET instructions = '{data['instructions']}' WHERE user_id = '{user_id}'")

async def edit_history(history, user_id):
    await db.execute(f"UPDATE profile SET history = '{history}' WHERE user_id = '{user_id}'")

async def clean_history(user_id):
    await db.execute(f"UPDATE profile SET history = '' WHERE user_id = '{user_id}'")

async def read_admin(user_id):
    result = await db.fetchrow(f"SELECT is_admin FROM profile WHERE user_id = '{user_id}'")
    for res in result:
        return res

async def read_whitelist(user_id):
    result = await db.fetchrow(f"SELECT is_whitelisted FROM profile WHERE user_id = '{user_id}'")
    for res in result:
        return res

async def read_instructions(user_id):
    result = await db.fetchrow(f"SELECT instructions FROM profile WHERE user_id = '{user_id}'")
    for res in result:
        return res

async def read_history(user_id):
    result = await db.fetchrow(f"SELECT history FROM profile WHERE user_id = '{user_id}'")
    for res in result:
        return res

async def get_whitelist():
    result = await db.fetch(f"SELECT user_id FROM profile WHERE is_whitelisted = True")
    return result