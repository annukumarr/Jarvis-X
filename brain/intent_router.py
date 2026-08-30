"""
brain/intent_router.py

Purpose:
Route JARVIS-X intents to the correct subsystem.

This module does NOT:
- execute system actions
- access the database
- call the AI
- perform frontend navigation

It only decides where an intent should go.

Architecture:

User Message
      ↓
Intent Engine
      ↓
Intent Router
      ├── navigation
      ├── social
      ├── information
      ├── memory
      ├── system_action
      └── general
"""

from __future__ import annotations

from brain.intents import (
    detect_intent,

    INTENT_GENERAL,
    INTENT_ABOUT,
    INTENT_PROJECTS,
    INTENT_JOURNEY,
    INTENT_CONTACT,

    INTENT_INSTAGRAM,
    INTENT_LINKEDIN,
    INTENT_GITHUB,
    INTENT_EMAIL,

    INTENT_NAVIGATE_HOME,
    INTENT_NAVIGATE_PROJECTS,
    INTENT_NAVIGATE_JOURNEY,
    INTENT_NAVIGATE_CONTACT,

    INTENT_MEMORY_SAVE,
    INTENT_MEMORY_RECALL,
)

from brain.decision import (
    get_action,
)


# ==========================================================
# ROUTE NAMES
# ==========================================================

ROUTE_GENERAL = "general"

ROUTE_INFORMATION = "information"

ROUTE_SOCIAL = "social"

ROUTE_NAVIGATION = "navigation"

ROUTE_MEMORY = "memory"

ROUTE_SYSTEM_ACTION = "system_action"


# ==========================================================
# ROUTE RESULT
# ==========================================================

def route_intent(
    message: str,
) -> dict:
    """
    Detect and route a JARVIS-X message.

    Returns a dictionary containing:

    intent
    route
    confidence
    entities
    action
    message
    """

    # ======================================================
    # DETECT INTENT
    # ======================================================

    result = detect_intent(
        message
    )

    intent = result.intent


    # ======================================================
    # SYSTEM ACTION CHECK
    # ======================================================

    system_action = get_action(
        message
    )

    if system_action is not None:

        return {
            "intent": "system_action",
            "route": ROUTE_SYSTEM_ACTION,
            "confidence": 1.0,
            "entities": {},
            "action": system_action,
            "message": message,
        }


    # ======================================================
    # NAVIGATION
    # ======================================================

    navigation_intents = {
        INTENT_NAVIGATE_HOME,
        INTENT_NAVIGATE_PROJECTS,
        INTENT_NAVIGATE_JOURNEY,
        INTENT_NAVIGATE_CONTACT,
    }

    if intent in navigation_intents:

        return {
            "intent": intent,
            "route": ROUTE_NAVIGATION,
            "confidence": result.confidence,
            "entities": result.entities,
            "action": None,
            "message": message,
        }


    # ======================================================
    # SOCIAL
    # ======================================================

    social_intents = {
        INTENT_INSTAGRAM,
        INTENT_LINKEDIN,
        INTENT_GITHUB,
        INTENT_EMAIL,
    }

    if intent in social_intents:

        return {
            "intent": intent,
            "route": ROUTE_SOCIAL,
            "confidence": result.confidence,
            "entities": result.entities,
            "action": None,
            "message": message,
        }


    # ======================================================
    # MEMORY
    # ======================================================

    memory_intents = {
        INTENT_MEMORY_SAVE,
        INTENT_MEMORY_RECALL,
    }

    if intent in memory_intents:

        return {
            "intent": intent,
            "route": ROUTE_MEMORY,
            "confidence": result.confidence,
            "entities": result.entities,
            "action": None,
            "message": message,
        }


    # ======================================================
    # PUBLIC INFORMATION
    # ======================================================

    information_intents = {
        INTENT_ABOUT,
        INTENT_PROJECTS,
        INTENT_JOURNEY,
        INTENT_CONTACT,
    }

    if intent in information_intents:

        return {
            "intent": intent,
            "route": ROUTE_INFORMATION,
            "confidence": result.confidence,
            "entities": result.entities,
            "action": None,
            "message": message,
        }


    # ======================================================
    # GENERAL
    # ======================================================

    return {
        "intent": INTENT_GENERAL,
        "route": ROUTE_GENERAL,
        "confidence": result.confidence,
        "entities": result.entities,
        "action": None,
        "message": message,
    }


# ==========================================================
# SIMPLE ROUTE HELPER
# ==========================================================

def get_route(
    message: str,
) -> str:
    """
    Return only the route name.
    """

    return route_intent(
        message
    )["route"]


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

        "what do you remember about Microsoft?",

        "shutdown pc",

        "restart computer",

        "delete test.txt",
    ]


    print()

    print("=" * 70)
    print("JARVIS-X INTENT ROUTER TEST")
    print("=" * 70)


    for message in test_messages:

        result = route_intent(
            message
        )

        print()

        print(
            f"User:       {message}"
        )

        print(
            f"Intent:     {result['intent']}"
        )

        print(
            f"Route:      {result['route']}"
        )

        print(
            f"Confidence: {result['confidence']}"
        )

        print(
            f"Action:     {result['action']}"
        )


    print()

    print("=" * 70)
    print("INTENT ROUTER TEST COMPLETE")
    print("=" * 70)