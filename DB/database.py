import aiosqlite


class Database:
    def __init__(self, path="data/database.db"):
        self.path = path

    async def init(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("PRAGMA foreign_keys = ON")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            await db.commit()

    async def add_user(self, user_id: int):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def view_users(self) -> int:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM users")
            result = await cursor.fetchone()
            await cursor.close()
            return result[0] if result else 0

    async def list_user_id(self) -> list[int]:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute("SELECT user_id FROM users")
            rows = await cursor.fetchall()
            await cursor.close()
            return [row[0] for row in rows]

    async def add_message(self, user_id: int, role: str, content: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
                (user_id, role, content)
            )
            await db.commit()

    async def get_history(self, user_id: int) -> list[dict]:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute(
                "SELECT role, content FROM messages WHERE user_id = ? ORDER BY id ASC",
                (user_id,)
            )
            rows = await cursor.fetchall()
            await cursor.close()
            return [{"role": row[0], "content": row[1]} for row in rows]

    async def clear_history(self, user_id: int):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
            await db.commit()


db = Database()
