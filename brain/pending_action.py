"""
brain/pending_action.py

Purpose:
Store and manage the action waiting for user confirmation.

Pending confirmation is persisted in SQLite so that
separate HTTP requests can safely access the same state.

This module does not execute actions.
It only manages pending confirmation state.
"""

import json

from database.db import (
    get_connection,
    initialize_database,
)


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def _ensure_table():
    """
    Make sure the pending_action table exists.
    """

    initialize_database()


# ==========================================================
# SET PENDING ACTION
# ==========================================================

def set_pending_action(action, data=None):
    """
    Store an action that requires confirmation.

    Any previous pending action is replaced.

    Parameters:
        action:
            Action identifier.

        data:
            Optional action-specific data.
    """

    _ensure_table()

    serialized_data = None

    if data is not None:

        try:
            serialized_data = json.dumps(
                data,
                ensure_ascii=False
            )

        except (TypeError, ValueError):

            serialized_data = json.dumps(
                str(data),
                ensure_ascii=False
            )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO pending_action (
            id,
            action,
            data
        )
        VALUES (
            1,
            ?,
            ?
        )
        ON CONFLICT(id)
        DO UPDATE SET
            action = excluded.action,
            data = excluded.data,
            created_at = CURRENT_TIMESTAMP
        """,
        (
            action,
            serialized_data,
        )
    )

    conn.commit()
    conn.close()


# ==========================================================
# GET PENDING ACTION
# ==========================================================

def get_pending_action():
    """
    Return the current pending action.

    Returns:
        dict
            {
                "action": "...",
                "data": ...
            }

        None
            No action is waiting.
    """

    _ensure_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT action, data
        FROM pending_action
        WHERE id = 1
        LIMIT 1
        """
    )

    result = cursor.fetchone()

    conn.close()

    if not result:
        return None

    action, serialized_data = result

    data = None

    if serialized_data:

        try:
            data = json.loads(
                serialized_data
            )

        except json.JSONDecodeError:

            data = serialized_data

    return {
        "action": action,
        "data": data,
    }


# ==========================================================
# CLEAR PENDING ACTION
# ==========================================================

def clear_pending_action():
    """
    Clear the current pending action.
    """

    _ensure_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM pending_action
        WHERE id = 1
        """
    )

    conn.commit()
    conn.close()


# ==========================================================
# HAS PENDING ACTION
# ==========================================================

def has_pending_action():
    """
    Check whether an action is waiting for confirmation.

    Returns:
        True
            Pending action exists.

        False
            No pending action exists.
    """

    return get_pending_action() is not None