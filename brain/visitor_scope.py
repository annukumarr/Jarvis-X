"""
brain/visitor_scope.py

Purpose:
Enforce the public Legacy-only scope for visitor JARVIS-X.

Visitor JARVIS-X must not answer unrelated general questions.
"""

from __future__ import annotations


# ==========================================================
# VISITOR SCOPE RESPONSE
# ==========================================================

VISITOR_SCOPE_RESPONSE = (
    "I'm JARVIS-X, the assistant for Legacy. "
    "I can help you explore Legacy, its projects, "
    "technologies, features, work, and related information."
)


# ==========================================================
# LEGACY SCOPE KEYWORDS
# ==========================================================

LEGACY_SCOPE_KEYWORDS = (
    "legacy",
    "portfolio",
    "website",
    "site",
    "project",
    "projects",
    "work",
    "experience",
    "skill",
    "skills",
    "technology",
    "technologies",
    "tech stack",
    "stack",
    "feature",
    "features",
    "jarvis",
    "annu",
    "about",
    "journey",
    "contact",
    "github",
    "linkedin",
    "instagram",
    "email",
    "resume",
    "cv",
)


# ==========================================================
# CONTEXTUAL WORDS
# ==========================================================

CONTEXTUAL_KEYWORDS = (
    "this",
    "this website",
    "this project",
    "this portfolio",
    "here",
    "your portfolio",
    "your project",
    "your work",
    "your website",
)


# ==========================================================
# CHECK LEGACY RELEVANCE
# ==========================================================

def is_legacy_related(message: str) -> bool:
    """
    Return True when a visitor question is reasonably
    related to Legacy.

    This is intentionally deterministic.
    """

    if not message:
        return False

    text = " ".join(
        message.strip().lower().split()
    )

    if not text:
        return False

    # ------------------------------------------------------
    # Direct Legacy-related keywords
    # ------------------------------------------------------

    if any(
        keyword in text
        for keyword in LEGACY_SCOPE_KEYWORDS
    ):
        return True

    # ------------------------------------------------------
    # Contextual website questions
    # ------------------------------------------------------

    if any(
        phrase in text
        for phrase in CONTEXTUAL_KEYWORDS
    ):
        return True

    return False


# ==========================================================
# GET VISITOR RESPONSE
# ==========================================================

def get_visitor_scope_response() -> str:
    """
    Return the fixed response used when a visitor
    asks something outside Legacy scope.
    """

    return VISITOR_SCOPE_RESPONSE