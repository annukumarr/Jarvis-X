"""
database/memory_db.py

Purpose:
Database operations for JARVIS-X memory.

This module:
- Saves memories
- Retrieves a specific memory
- Retrieves all memories
- Searches memories by text

No AI logic.
No command logic.
"""


from database.db import get_connection


# ==========================================================
# SAVE MEMORY
# ==========================================================

def save_memory(
    category,
    key,
    value,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO memory(
            category,
            memory_key,
            memory_value
        )
        VALUES (?, ?, ?)
        """,
        (
            category,
            key,
            value,
        )
    )

    conn.commit()
    conn.close()


# ==========================================================
# GET SPECIFIC MEMORY
# ==========================================================

def get_memory(
    category,
    key,
):

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
        (
            category,
            key,
        )
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None


# ==========================================================
# GET ALL MEMORIES
# ==========================================================

def get_all_memories():

    """
    Returns the latest valid memory for each key.

    Prevents duplicate keys from appearing
    multiple times.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            category,
            memory_key,
            memory_value
        FROM memory
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    memories = {}

    seen_keys = set()

    for category, key, value in rows:

        if key in seen_keys:
            continue

        seen_keys.add(key)

        if category not in memories:
            memories[category] = {}

        memories[category][key] = value

    return memories


# ==========================================================
# SEARCH MEMORIES
# ==========================================================

def search_memories(
    query: str,
):
    """
    Search stored memories using a text query.

    Searches across:
    - category
    - memory key
    - memory value

    Returns latest matching memories first.
    """

    if not query:
        return []

    query = query.strip()

    if not query:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    search_pattern = f"%{query}%"

    cursor.execute(
        """
        SELECT
            category,
            memory_key,
            memory_value
        FROM memory
        WHERE
            category LIKE ?
            OR memory_key LIKE ?
            OR memory_value LIKE ?
        ORDER BY id DESC
        """,
        (
            search_pattern,
            search_pattern,
            search_pattern,
        )
    )

    rows = cursor.fetchall()

    conn.close()

    results = []

    seen_keys = set()

    for category, key, value in rows:

        if key in seen_keys:
            continue

        seen_keys.add(key)

        results.append(
            {
                "category": category,
                "key": key,
                "value": value,
            }
        )

    return results