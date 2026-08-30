import sqlite3
import os


DATABASE_NAME = "database/jarvis_memory.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """

    # Make sure database directory exists
    os.makedirs(
        os.path.dirname(DATABASE_NAME),
        exist_ok=True
    )

    conn = sqlite3.connect(
        DATABASE_NAME,
        timeout=10
    )

    return conn


def initialize_database():
    """
    Initialize all JARVIS-X database tables.

    Existing owner memory is preserved.
    Visitor analytics uses separate tables.
    Pending confirmation actions are persisted.
    """

    # ======================================================
    # MAKE DATABASE DIRECTORY
    # ======================================================

    os.makedirs(
        os.path.dirname(DATABASE_NAME),
        exist_ok=True
    )

    conn = get_connection()
    cursor = conn.cursor()

    # ======================================================
    # JARVIS OWNER MEMORY
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            memory_key TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ======================================================
    # VISITOR SESSIONS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitor_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            visitor_id TEXT NOT NULL,
            session_id TEXT NOT NULL UNIQUE,

            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            page TEXT,
            referrer TEXT
        )
    """)

    # ======================================================
    # VISITOR EVENTS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitor_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            visitor_id TEXT NOT NULL,
            session_id TEXT NOT NULL,

            event_type TEXT NOT NULL,
            event_data TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ======================================================
    # PENDING ACTION
    # ======================================================
    #
    # Stores the action waiting for confirmation.
    #
    # This replaces the old in-memory global state:
    #
    #     _pending_action = None
    #
    # Now the confirmation survives between
    # separate HTTP requests.
    #
    # Only one pending action is allowed at a time.
    #

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pending_action (
            id INTEGER PRIMARY KEY CHECK (id = 1),

            action TEXT NOT NULL,

            data TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ======================================================
    # INDEXES
    # ======================================================

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_visitor_sessions_visitor_id
        ON visitor_sessions(visitor_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_visitor_events_visitor_id
        ON visitor_events(visitor_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_visitor_events_session_id
        ON visitor_events(session_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_visitor_events_event_type
        ON visitor_events(event_type)
    """)

    conn.commit()
    conn.close()