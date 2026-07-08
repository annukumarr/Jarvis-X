"""
settings/memory_patterns.py

Purpose:
Stores all save and recall patterns used by JARVIS.
No database code.
No AI code.
Only pattern definitions.
"""

# ==========================
# SAVE PATTERNS
# ==========================

SAVE_PATTERNS = {

    # ---------- Profile ----------
    "my name is": ("profile", "name"),
    "i am": ("profile", "name"),

    "i study at": ("profile", "college"),
    "i study in": ("profile", "college"),
    "my college is": ("profile", "college"),
    "my university is": ("profile", "college"),
    "my school is": ("profile", "college"),

    "my birthday is": ("profile", "birthday"),
    "my age is": ("profile", "age"),

    # ---------- Goals ----------
    "my dream company is": ("goal", "dream_company"),
    "i want to become": ("goal", "career"),
    "my goal is": ("goal", "goal"),

    # ---------- Preferences ----------
    "my favorite language is": ("preference", "language"),
    "my favourite language is": ("preference", "language"),

    "my favorite color is": ("preference", "color"),
    "my favourite color is": ("preference", "color"),

    "my favorite food is": ("preference", "food"),
    "my favourite food is": ("preference", "food"),

    # ---------- Schedule ----------
    "i wake up at": ("schedule", "wake_time"),
    "i sleep at": ("schedule", "sleep_time"),
}


# ==========================
# RECALL PATTERNS
# ==========================

RECALL_PATTERNS = {

    # ---------- Profile ----------
    "what is my name": ("profile", "name"),

    "where do i study": ("profile", "college"),
    "where am i studying": ("profile", "college"),
    "what is my college": ("profile", "college"),
    "what is my university": ("profile", "college"),
    "which university do i study at": ("profile", "college"),

    "when is my birthday": ("profile", "birthday"),
    "how old am i": ("profile", "age"),

    # ---------- Goals ----------
    "what is my dream company": ("goal", "dream_company"),
    "what is my goal": ("goal", "goal"),
    "what do i want to become": ("goal", "career"),

    # ---------- Preferences ----------
    "what is my favorite language": ("preference", "language"),
    "what is my favourite language": ("preference", "language"),

    "what is my favorite color": ("preference", "color"),
    "what is my favourite color": ("preference", "color"),

    "what is my favorite food": ("preference", "food"),
    "what is my favourite food": ("preference", "food"),

    # ---------- Schedule ----------
    "when do i wake up": ("schedule", "wake_time"),
    "when do i sleep": ("schedule", "sleep_time"),
}