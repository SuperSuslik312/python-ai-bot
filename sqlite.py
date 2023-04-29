import sqlite3 as sq

async def start_db():
    global db, cur
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, is_admin BOOLEAN NOT NULL CHECK (is_admin IN (0, 1)), is_whitelisted BOOLEAN NOT NULL CHECK (is_whitelisted IN (0, 1)), history TEXT)")
    db.commit()

async def create(user_id):
    user = cur.execute(f"SELECT 1 FROM profile WHERE user_id == '{user_id}'").fetchone()
    if not user:
        cur.execute(f"INSERT INTO profile VALUES('{user_id}', 0, 0, '')")
        db.commit()

async def edit_admin(state, user_id):
    async with state.proxy() as data:
        cur.execute(f"UPDATE profile SET is_admin = '{data['is_admin']}' WHERE user_id == '{user_id}'")
        db.commit()

async def edit_whitelist(state, user_id):
    async with state.proxy() as data:
        cur.execute(f"UPDATE profile SET is_whitelisted = '{data['is_whitelisted']}' WHERE user_id == '{user_id}'")
        db.commit()