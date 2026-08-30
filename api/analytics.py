"""
api/analytics.py

Visitor analytics for Legacy / JARVIS-X.

This module stores anonymous visitor sessions
and interaction events.

No owner memory is stored here.
"""

import json
import uuid

from database.db import get_connection


# ==========================================================
# SESSION
# ==========================================================

def create_visitor_session(
    visitor_id: str | None = None,
    page: str | None = None,
    referrer: str | None = None,
):
    """
    Create a new anonymous visitor session.

    If visitor_id is not provided, a new visitor ID
    is generated.
    """

    if not visitor_id:
        visitor_id = str(uuid.uuid4())

    session_id = str(uuid.uuid4())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO visitor_sessions (
            visitor_id,
            session_id,
            page,
            referrer
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            visitor_id,
            session_id,
            page,
            referrer,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "visitor_id": visitor_id,
        "session_id": session_id,
    }


# ==========================================================
# UPDATE SESSION
# ==========================================================

def update_session(
    visitor_id: str,
    session_id: str,
    page: str | None = None,
):
    """
    Update the last activity timestamp
    of an existing visitor session.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE visitor_sessions

        SET
            last_seen = CURRENT_TIMESTAMP,
            page = COALESCE(?, page)

        WHERE
            visitor_id = ?
            AND session_id = ?
        """,
        (
            page,
            visitor_id,
            session_id,
        ),
    )

    conn.commit()
    conn.close()


# ==========================================================
# SAVE EVENT
# ==========================================================

def save_visitor_event(
    visitor_id: str,
    session_id: str,
    event_type: str,
    event_data: dict | None = None,
):
    """
    Save an anonymous visitor event.
    """

    event_json = None

    if event_data:
        event_json = json.dumps(
            event_data,
            ensure_ascii=False,
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO visitor_events (
            visitor_id,
            session_id,
            event_type,
            event_data
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            visitor_id,
            session_id,
            event_type,
            event_json,
        ),
    )

    cursor.execute(
        """
        UPDATE visitor_sessions
        SET last_seen = CURRENT_TIMESTAMP
        WHERE
            visitor_id = ?
            AND session_id = ?
        """,
        (
            visitor_id,
            session_id,
        ),
    )

    conn.commit()
    conn.close()


# ==========================================================
# ANALYTICS SUMMARY
# ==========================================================

def get_analytics_summary():
    """
    Return basic visitor analytics.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Total unique visitors
    cursor.execute(
        """
        SELECT COUNT(DISTINCT visitor_id)
        FROM visitor_sessions
        """
    )

    total_visitors = cursor.fetchone()[0]

    # Total sessions
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM visitor_sessions
        """
    )

    total_sessions = cursor.fetchone()[0]

    # Total events
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM visitor_events
        """
    )

    total_events = cursor.fetchone()[0]

    # Event breakdown
    cursor.execute(
        """
        SELECT
            event_type,
            COUNT(*) AS count
        FROM visitor_events
        GROUP BY event_type
        ORDER BY count DESC
        """
    )

    event_rows = cursor.fetchall()

    event_breakdown = {}

    for event_type, count in event_rows:
        event_breakdown[event_type] = count

    # Recent sessions
    cursor.execute(
        """
        SELECT
            visitor_id,
            session_id,
            first_seen,
            last_seen,
            page,
            referrer

        FROM visitor_sessions

        ORDER BY id DESC

        LIMIT 20
        """
    )

    session_rows = cursor.fetchall()

    recent_sessions = []

    for row in session_rows:

        (
            visitor_id,
            session_id,
            first_seen,
            last_seen,
            page,
            referrer,
        ) = row

        recent_sessions.append(
            {
                "visitor_id": visitor_id,
                "session_id": session_id,
                "first_seen": first_seen,
                "last_seen": last_seen,
                "page": page,
                "referrer": referrer,
            }
        )

    conn.close()

    return {
        "total_visitors": total_visitors,
        "total_sessions": total_sessions,
        "total_events": total_events,
        "event_breakdown": event_breakdown,
        "recent_sessions": recent_sessions,
    }