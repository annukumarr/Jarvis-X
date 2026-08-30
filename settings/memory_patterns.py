"""
settings/memory_patterns.py

Purpose:
Stores all save and recall patterns used by JARVIS.

No database code.
No AI code.
Only pattern definitions.
"""


# ==========================================================
# SAVE PATTERNS
# ==========================================================

SAVE_PATTERNS = {

    # ======================================================
    # PROFILE
    # ======================================================

    "my name is": (
        "profile",
        "name",
    ),

    "i am": (
        "profile",
        "name",
    ),

    "i study at": (
        "profile",
        "college",
    ),

    "i study in": (
        "profile",
        "college",
    ),

    "my college is": (
        "profile",
        "college",
    ),

    "my university is": (
        "profile",
        "college",
    ),

    "my school is": (
        "profile",
        "college",
    ),

    "my birthday is": (
        "profile",
        "birthday",
    ),

    "my age is": (
        "profile",
        "age",
    ),


    # ======================================================
    # GOALS
    # ======================================================

    "my dream company is": (
        "goal",
        "dream_company",
    ),

    "my target company is": (
        "goal",
        "target_company",
    ),

    "my target is": (
        "goal",
        "target",
    ),

    "my goal is": (
        "goal",
        "goal",
    ),

    "i want to become": (
        "goal",
        "career",
    ),

    "i want to work": (
        "goal",
        "career",
    ),


    # ======================================================
    # PREFERENCES
    # ======================================================

    "my favorite language is": (
        "preference",
        "language",
    ),

    "my favourite language is": (
        "preference",
        "language",
    ),

    "my favorite color is": (
        "preference",
        "color",
    ),

    "my favourite color is": (
        "preference",
        "color",
    ),

    "my favorite food is": (
        "preference",
        "food",
    ),

    "my favourite food is": (
        "preference",
        "food",
    ),


    # ======================================================
    # SCHEDULE
    # ======================================================

    "i wake up at": (
        "schedule",
        "wake_time",
    ),

    "i sleep at": (
        "schedule",
        "sleep_time",
    ),
}


# ==========================================================
# RECALL PATTERNS
# ==========================================================

RECALL_PATTERNS = {

    # ======================================================
    # PROFILE
    # ======================================================

    "what is my name": (
        "profile",
        "name",
    ),

    "what's my name": (
        "profile",
        "name",
    ),

    "where do i study": (
        "profile",
        "college",
    ),

    "where am i studying": (
        "profile",
        "college",
    ),

    "what is my college": (
        "profile",
        "college",
    ),

    "what's my college": (
        "profile",
        "college",
    ),

    "what is my university": (
        "profile",
        "college",
    ),

    "what's my university": (
        "profile",
        "college",
    ),

    "which university do i study at": (
        "profile",
        "college",
    ),

    "when is my birthday": (
        "profile",
        "birthday",
    ),

    "how old am i": (
        "profile",
        "age",
    ),


    # ======================================================
    # GOALS
    # ======================================================

    "what is my dream company": (
        "goal",
        "dream_company",
    ),

    "what's my dream company": (
        "goal",
        "dream_company",
    ),

    "what is my target company": (
        "goal",
        "target_company",
    ),

    "what's my target company": (
        "goal",
        "target_company",
    ),

    "what is my target": (
        "goal",
        "target",
    ),

    "what's my target": (
        "goal",
        "target",
    ),

    "what is my goal": (
        "goal",
        "goal",
    ),

    "what's my goal": (
        "goal",
        "goal",
    ),

    "what do i want to become": (
        "goal",
        "career",
    ),

    "where do i want to work": (
        "goal",
        "career",
    ),


    # ======================================================
    # PREFERENCES
    # ======================================================

    "what is my favorite language": (
        "preference",
        "language",
    ),

    "what's my favorite language": (
        "preference",
        "language",
    ),

    "what is my favourite language": (
        "preference",
        "language",
    ),

    "what's my favourite language": (
        "preference",
        "language",
    ),

    "what is my favorite color": (
        "preference",
        "color",
    ),

    "what's my favorite color": (
        "preference",
        "color",
    ),

    "what is my favourite color": (
        "preference",
        "color",
    ),

    "what's my favourite color": (
        "preference",
        "color",
    ),

    "what is my favorite food": (
        "preference",
        "food",
    ),

    "what's my favorite food": (
        "preference",
        "food",
    ),

    "what is my favourite food": (
        "preference",
        "food",
    ),

    "what's my favourite food": (
        "preference",
        "food",
    ),


    # ======================================================
    # SCHEDULE
    # ======================================================

    "when do i wake up": (
        "schedule",
        "wake_time",
    ),

    "when do i sleep": (
        "schedule",
        "sleep_time",
    ),
}