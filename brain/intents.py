"""
brain/intents.py

JARVIS-X Intent Engine

Purpose:
- Detect what the user wants.
- Separate information, navigation, social,
  project and memory-related requests.
- Keep intent detection independent from AI generation.
- Return structured intent information to the caller.

This module does NOT:
- call Gemini
- access the database
- perform navigation
- modify memory
- execute system actions

It only understands the user's intent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re


# ==========================================================
# INTENT NAMES
# ==========================================================

INTENT_GENERAL = "general"

INTENT_ABOUT = "about"
INTENT_PROJECTS = "projects"
INTENT_JOURNEY = "journey"
INTENT_CONTACT = "contact"

INTENT_INSTAGRAM = "instagram"
INTENT_LINKEDIN = "linkedin"
INTENT_GITHUB = "github"
INTENT_EMAIL = "email"

INTENT_NAVIGATE_HOME = "navigate_home"
INTENT_NAVIGATE_PROJECTS = "navigate_projects"
INTENT_NAVIGATE_JOURNEY = "navigate_journey"
INTENT_NAVIGATE_CONTACT = "navigate_contact"

INTENT_MEMORY_SAVE = "memory_save"
INTENT_MEMORY_RECALL = "memory_recall"


# ==========================================================
# RESULT MODEL
# ==========================================================

@dataclass
class IntentResult:
    """
    Structured result returned by the intent engine.
    """

    intent: str
    confidence: float
    entities: dict[str, str] = field(default_factory=dict)
    original_message: str = ""


# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def normalize_text(message: str) -> str:
    """
    Normalize user input before intent detection.
    """

    if not message:
        return ""

    text = message.strip().lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text


# ==========================================================
# KEYWORD MATCHER
# ==========================================================

def _contains_any(
    text: str,
    keywords: tuple[str, ...],
) -> bool:
    """
    Return True when any keyword exists in the text.
    """

    return any(
        keyword in text
        for keyword in keywords
    )


# ==========================================================
# NAVIGATION INTENTS
# ==========================================================

def _detect_navigation(
    text: str,
) -> IntentResult | None:

    # ------------------------------------------------------
    # HOME
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "go home",
            "take me home",
            "show home",
            "open home",
            "back home",
        ),
    ):
        return IntentResult(
            intent=INTENT_NAVIGATE_HOME,
            confidence=0.98,
        )

    # ------------------------------------------------------
    # PROJECTS
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "show me the projects",
            "show my projects",
            "show projects",
            "open projects",
            "go to projects",
            "take me to projects",
            "view projects",
            "see projects",
        ),
    ):
        return IntentResult(
            intent=INTENT_NAVIGATE_PROJECTS,
            confidence=0.98,
        )

    # ------------------------------------------------------
    # JOURNEY
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "show my journey",
            "show journey",
            "open journey",
            "go to journey",
            "take me to journey",
            "view journey",
        ),
    ):
        return IntentResult(
            intent=INTENT_NAVIGATE_JOURNEY,
            confidence=0.98,
        )

    # ------------------------------------------------------
    # CONTACT
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "go to contact",
            "take me to contact",
            "show contact",
            "open contact",
            "contact section",
            "contact me",
        ),
    ):
        return IntentResult(
            intent=INTENT_NAVIGATE_CONTACT,
            confidence=0.98,
        )

    return None


# ==========================================================
# SOCIAL INTENTS
# ==========================================================

def _detect_social(
    text: str,
) -> IntentResult | None:

    # ------------------------------------------------------
    # INSTAGRAM
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "instagram",
            "insta",
            "ig handle",
            "instagram id",
            "instagram username",
        ),
    ):
        return IntentResult(
            intent=INTENT_INSTAGRAM,
            confidence=0.99,
            entities={
                "platform": "instagram",
            },
        )

    # ------------------------------------------------------
    # LINKEDIN
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "linkedin",
            "linkedin profile",
            "linkedin id",
            "linkedin url",
        ),
    ):
        return IntentResult(
            intent=INTENT_LINKEDIN,
            confidence=0.99,
            entities={
                "platform": "linkedin",
            },
        )

    # ------------------------------------------------------
    # GITHUB
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "github",
            "github profile",
            "github username",
            "github id",
        ),
    ):
        return IntentResult(
            intent=INTENT_GITHUB,
            confidence=0.99,
            entities={
                "platform": "github",
            },
        )

    # ------------------------------------------------------
    # EMAIL
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "email",
            "email id",
            "email address",
            "mail id",
            "contact email",
        ),
    ):
        return IntentResult(
            intent=INTENT_EMAIL,
            confidence=0.99,
            entities={
                "platform": "email",
            },
        )

    return None


# ==========================================================
# PUBLIC INFORMATION INTENTS
# ==========================================================

def _detect_information(
    text: str,
) -> IntentResult | None:

    # ------------------------------------------------------
    # ABOUT ANNU
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "who is annu",
            "who's annu",
            "tell me about annu",
            "about annu",
            "who is anu",
            "tell me about anu",
        ),
    ):
        return IntentResult(
            intent=INTENT_ABOUT,
            confidence=0.99,
        )

    # ------------------------------------------------------
    # PROJECTS
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "what are his projects",
            "what are annu's projects",
            "what projects has he built",
            "tell me about his projects",
            "tell me his projects",
            "list his projects",
        ),
    ):
        return IntentResult(
            intent=INTENT_PROJECTS,
            confidence=0.97,
        )

    # ------------------------------------------------------
    # JOURNEY
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "what is his journey",
            "tell me about his journey",
            "annu's journey",
            "career journey",
            "learning journey",
        ),
    ):
        return IntentResult(
            intent=INTENT_JOURNEY,
            confidence=0.97,
        )

    # ------------------------------------------------------
    # CONTACT
    # ------------------------------------------------------

    if _contains_any(
        text,
        (
            "how can i contact annu",
            "how to contact annu",
            "contact annu",
            "how can i reach annu",
        ),
    ):
        return IntentResult(
            intent=INTENT_CONTACT,
            confidence=0.97,
        )

    return None


# ==========================================================
# MEMORY INTENTS
# ==========================================================

def _detect_memory(
    text: str,
) -> IntentResult | None:

    # ======================================================
    # RECALL MEMORY
    # ======================================================

    if _contains_any(
        text,
        (
            # Generic recall
            "what did i tell you",
            "what do you remember",
            "what do you remember about",
            "do you remember",
            "do you remember about",
            "recall my memory",
            "recall my",
            "what have i told you",

            # Personal memory questions
            "what is my",
            "what's my",
            "where do i study",
            "where am i studying",
            "when is my birthday",
            "how old am i",
            "what do i want to become",
            "where do i want to work",
        ),
    ):
        return IntentResult(
            intent=INTENT_MEMORY_RECALL,
            confidence=0.98,
        )

    # ======================================================
    # SAVE MEMORY
    # ======================================================

    if _contains_any(
        text,
        (
            "remember that",
            "remember this",
            "save this",
            "save that",
            "please remember",
            "please save",
        ),
    ):
        return IntentResult(
            intent=INTENT_MEMORY_SAVE,
            confidence=0.98,
        )

    return None


# ==========================================================
# MAIN INTENT DETECTOR
# ==========================================================

def detect_intent(
    message: str,
) -> IntentResult:
    """
    Detect the primary intent of a user message.

    Priority:

    1. Navigation
    2. Social
    3. Memory
    4. Public information
    5. General conversation
    """

    original_message = message or ""

    text = normalize_text(
        original_message
    )

    if not text:
        return IntentResult(
            intent=INTENT_GENERAL,
            confidence=0.0,
            original_message=original_message,
        )

    # ------------------------------------------------------
    # NAVIGATION
    # ------------------------------------------------------

    result = _detect_navigation(text)

    if result:
        result.original_message = original_message
        return result

    # ------------------------------------------------------
    # SOCIAL
    # ------------------------------------------------------

    result = _detect_social(text)

    if result:
        result.original_message = original_message
        return result

    # ------------------------------------------------------
    # MEMORY
    # ------------------------------------------------------

    result = _detect_memory(text)

    if result:
        result.original_message = original_message
        return result

    # ------------------------------------------------------
    # INFORMATION
    # ------------------------------------------------------

    result = _detect_information(text)

    if result:
        result.original_message = original_message
        return result

    # ------------------------------------------------------
    # GENERAL
    # ------------------------------------------------------

    return IntentResult(
        intent=INTENT_GENERAL,
        confidence=0.50,
        original_message=original_message,
    )


# ==========================================================
# SIMPLE STRING HELPER
# ==========================================================

def get_intent(
    message: str,
) -> str:
    """
    Return only the intent name.
    """

    return detect_intent(
        message
    ).intent


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    test_messages = [

        "hello jarvis",

        "who is annu",

        "what are his projects",

        "show me the projects",

        "take me to projects",

        "show my journey",

        "go to contact",

        "what is Annu's Instagram?",

        "what is Annu's LinkedIn?",

        "show me his GitHub",

        "what is his email?",

        "remember that my next target is Microsoft",

        "what is my target company",

        "what do you remember about Microsoft?",

        "what did I tell you about my target?",

        "do you remember my Microsoft goal?",

        "what is my goal",

        "what is my name",

        "what is my college",
    ]


    print()

    print("=" * 60)

    print(
        "JARVIS-X INTENT ENGINE TEST"
    )

    print("=" * 60)


    for message in test_messages:

        result = detect_intent(
            message
        )

        print()

        print(
            f"User:       {message}"
        )

        print(
            f"Intent:     {result.intent}"
        )

        print(
            f"Confidence: {result.confidence}"
        )

        print(
            f"Entities:   {result.entities}"
        )


    print()

    print("=" * 60)

    print(
        "INTENT ENGINE TEST COMPLETE"
    )

    print("=" * 60)