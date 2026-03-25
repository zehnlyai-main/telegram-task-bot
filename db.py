import os
import aiosqlite

DB_PATH = os.getenv("DATABASE_PATH", "data/bot.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id    INTEGER PRIMARY KEY,
    language   TEXT DEFAULT 'en',
    api_key    TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    text         TEXT NOT NULL,
    status       TEXT DEFAULT 'active',
    remind_at    TEXT,
    snooze_count INTEGER DEFAULT 0,
    created_at   TEXT DEFAULT (datetime('now')),
    completed_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
"""


async def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.executescript(SCHEMA)
        # Add columns if upgrading from older schema
        for col, typ in [("api_key", "TEXT"), ("completed_at", "TEXT")]:
            try:
                await conn.execute(f"ALTER TABLE users ADD COLUMN {col} {typ}")
            except Exception:
                pass
        try:
            await conn.execute("ALTER TABLE tasks ADD COLUMN completed_at TEXT")
        except Exception:
            pass
        await conn.commit()


async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def upsert_user(user_id: int, **fields) -> None:
    existing = await get_user(user_id)
    async with aiosqlite.connect(DB_PATH) as conn:
        if existing:
            sets = ", ".join(f"{k} = ?" for k in fields)
            vals = list(fields.values()) + [user_id]
            await conn.execute(f"UPDATE users SET {sets} WHERE user_id = ?", vals)
        else:
            fields["user_id"] = user_id
            cols = ", ".join(fields.keys())
            placeholders = ", ".join("?" for _ in fields)
            await conn.execute(
                f"INSERT INTO users ({cols}) VALUES ({placeholders})",
                list(fields.values()),
            )
        await conn.commit()


async def create_task(user_id: int, text: str, status: str = "active") -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "INSERT INTO tasks (user_id, text, status) VALUES (?, ?, ?)",
            (user_id, text, status),
        )
        await conn.commit()
        return cursor.lastrowid


async def get_task(task_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def update_task(task_id: int, **fields) -> None:
    sets = ", ".join(f"{k} = ?" for k in fields)
    vals = list(fields.values()) + [task_id]
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(f"UPDATE tasks SET {sets} WHERE id = ?", vals)
        await conn.commit()


async def delete_task(task_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        await conn.commit()


async def get_user_tasks(user_id: int) -> list[dict]:
    """Get all non-done, non-backlog tasks."""
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND status NOT IN ('done', 'backlog') "
            "ORDER BY created_at DESC",
            (user_id,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_backlog_tasks(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND status = 'backlog' "
            "ORDER BY created_at DESC",
            (user_id,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_done_tasks(user_id: int, limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND status = 'done' "
            "ORDER BY completed_at DESC LIMIT ?",
            (user_id, limit),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_pending_tasks() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT * FROM tasks WHERE status = 'pending' AND remind_at IS NOT NULL"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_all_users() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
