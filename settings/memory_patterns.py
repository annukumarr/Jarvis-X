"""
config/memory_patterns.py

Purpose:
Stores all memory patterns used by JARVIS.
No database code.
No AI code.
Only pattern definitions.
"""

MEMORY_PATTERNS = {

    # ---------- Profile ----------
    "my name is": ("profile", "name"),
    "i am": ("profile", "name"),
    "i study at": ("profile", "college"),
    "my college is": ("profile", "college"),
    "my university is": ("profile", "college"),
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