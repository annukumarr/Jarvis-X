from database.db import get_connection


def save_memory(category, key, value):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO memory(category, memory_key, memory_value)
        VALUES (?, ?, ?)
        """,
        (category, key, value)
    )

    conn.commit()
    conn.close()


def get_memory(category, key):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT memory_value
        FROM memory
        WHERE category=?
        AND memory_key=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (category, key)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None


def get_all_memories():

    """
    Returns latest value of every memory.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT category,
               memory_key,
               memory_value
        FROM memory
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    memories = {}

    for category, key, value in rows:

        if category not in memories:
            memories[category] = {}

        # Keep only latest value
        if key not in memories[category]:
            memories[category][key] = value

    return memories