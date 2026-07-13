import aiosqlite

DB_PATH = "email_responder.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS professors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                google_id TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                access_token TEXT,
                refresh_token TEXT,
                token_expiry TEXT
            )
        """)
        await db.commit()

async def insert_and_update_professors (
        google_id: str, 
        email: str, 
        name: str, 
        access_token: str,
        refresh_token: str,
        token_expiry: str
    ):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT INTO professors (google_id, email, name, access_token, refresh_token, token_expiry)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(google_id) DO UPDATE SET
                    access_token = excluded.access_token,
                    refresh_token = excluded.refresh_token,
                    token_expiry = excluded.token_expiry
            """, (google_id, email, name, access_token, refresh_token, token_expiry))
            await db.commit()

async def get_professor_by_google_id(google_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute (
            "SELECT * FROM professors WHERE google_id = ?", (google_id,)
        ) as cursor:
            return await cursor.fetchone()
        
async def get_all_professors():
     async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM professors") as cursor:
            return await cursor.fetchall()
        
async def delete_professor(google_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM professors WHERE google_id = ?", (google_id,)
        )
        await db.commit()


        
