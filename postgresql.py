import asyncpg
from config import Config

database = Config.DB_NAME
db_user = Config.DB_USER
password = Config.DB_PASS
host = Config.DB_HOST
port = Config.DB_PORT
instructions = Config.INSTRUCTIONS
admin_id = Config.ADMIN_ID


async def start_db():
    global db
    db = await asyncpg.connect(database=database, user=db_user, password=password, host=host, port=port)
    await db.execute("CREATE TABLE IF NOT EXISTS profile(user_id BIGINT PRIMARY KEY, is_admin BOOL NOT NULL, is_whitelisted BOOL NOT NULL, instructions TEXT, history JSONB)")


async def create(user_id):
    user = await db.fetch("SELECT 1 FROM profile WHERE user_id = $1", user_id)
    if not user and user_id == admin_id:
        await db.execute("INSERT INTO profile VALUES($1, True, True, $2, NULL)", user_id, instructions)
    elif not user:
        await db.execute("INSERT INTO profile VALUES($1, False, False, $2, NULL)", user_id, instructions)


async def edit_admin(state, user_id):
    await create(user_id)
    data = await state.get_data()
    await db.execute(f"UPDATE profile SET is_admin = $1 WHERE user_id = $2", data['is_admin'], user_id)


async def edit_whitelist(state, user_id):
    await create(user_id)
    data = await state.get_data()
    await db.execute("UPDATE profile SET is_whitelisted = $1 WHERE user_id = $2", data['is_whitelisted'], user_id)


async def edit_instructions(state, user_id):
    data = await state.get_data()
    await db.execute("UPDATE profile SET instructions = $1 WHERE user_id = $2", data['instructions'], user_id)


async def reset_instructions(user_id):
    await db.execute("UPDATE profile SET instructions = $1 WHERE user_id = $2", instructions, user_id)


async def edit_history(history, user_id):
    await db.execute("UPDATE profile SET history = $1 WHERE user_id = $2", history, user_id)


async def clean_history(user_id):
    await db.execute("UPDATE profile SET history = NULL WHERE user_id = $1", user_id)


async def read_admin(user_id):
    result = await db.fetchrow("SELECT is_admin FROM profile WHERE user_id = $1", user_id)
    for res in result:
        return res


async def read_whitelist(user_id):
    result = await db.fetchrow("SELECT is_whitelisted FROM profile WHERE user_id = $1", user_id)
    for res in result:
        return res


async def read_instructions(user_id):
    result = await db.fetchrow("SELECT instructions FROM profile WHERE user_id = $1", user_id)
    for res in result:
        return res


async def read_history(user_id):
    result = await db.fetchrow("SELECT history FROM profile WHERE user_id = $1", user_id)
    for res in result:
        return res


async def get_whitelist():
    result = await db.fetch("SELECT user_id FROM profile WHERE is_whitelisted = True")
    return result
