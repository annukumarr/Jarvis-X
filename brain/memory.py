import sqlite3

conn = sqlite3.connect("database/jarvis_memory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory(
    key TEXT PRIMARY KEY,
    value TEXT
)
""")

conn.commit()


def save_memory(key, value):
    cursor.execute(
        "INSERT OR REPLACE INTO memory VALUES (?, ?)",
        (key, value)
    )
    conn.commit()


def get_memory(key):
    cursor.execute(
        "SELECT value FROM memory WHERE key=?",
        (key,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    return None