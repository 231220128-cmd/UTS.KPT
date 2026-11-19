
import aiosqlite

DATABASE_NAME = "bookstore.db"

CREATE_BOOK_TABLE = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);
"""

CREATE_TRANSACTION_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id)
);
"""

async def get_db():
    db = await aiosqlite.connect(DATABASE_NAME)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA foreign_keys = ON")
    return db

async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute(CREATE_BOOK_TABLE)
        await db.execute(CREATE_TRANSACTION_TABLE)
        await db.commit()

async def fetch_one(query: str, params: tuple = ()):
    db = await get_db()
    try:
        cursor = await db.execute(query, params)
        row = await cursor.fetchone()
        await cursor.close()
        return dict(row) if row else None
    finally:
        await db.close()

async def fetch_all(query: str, params: tuple = ()):
    db = await get_db()
    try:
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        await cursor.close()
        return [dict(row) for row in rows]
    finally:
        await db.close()

async def execute(query: str, params: tuple = ()):
    db = await get_db()
    try:
        cursor = await db.execute(query, params)
        await db.commit()
        last_id = cursor.lastrowid
        await cursor.close()
        return last_id
    finally:
        await db.close()
