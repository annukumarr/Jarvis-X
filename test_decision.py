"""
test_decision.py

Purpose:
Test JARVIS decision and confirmation requirements.
"""

from brain.decision import (
    get_action,
    requires_confirmation,
)
from brain.confirmation import (
    get_confirmation_result,
)


# ==========================
# DECISION TESTS
# ==========================

def test_shutdown_requires_confirmation():

    assert requires_confirmation("shutdown") is True
    assert get_action("shutdown") == "shutdown"


def test_restart_requires_confirmation():

    assert requires_confirmation("restart") is True
    assert get_action("restart") == "restart"


def test_delete_requires_confirmation():

    assert requires_confirmation("delete file") is True
    assert get_action("delete file") == "delete"


def test_remove_requires_confirmation():

    assert requires_confirmation("remove file") is True
    assert get_action("remove file") == "remove"


def test_safe_command_does_not_require_confirmation():

    assert requires_confirmation("open chrome") is False
    assert get_action("open chrome") is None


def test_ai_question_does_not_require_confirmation():

    assert requires_confirmation(
        "what is artificial intelligence"
    ) is False

    assert get_action(
        "what is artificial intelligence"
    ) is None


# ==========================
# CONFIRMATION TESTS
# ==========================

def test_yes_confirmation():

    assert get_confirmation_result("yes") is True
    assert get_confirmation_result("yeah") is True
    assert get_confirmation_result("confirm") is True


def test_no_confirmation():

    assert get_confirmation_result("no") is False
    assert get_confirmation_result("cancel") is False
    assert get_confirmation_result("stop") is False


def test_unknown_confirmation():

    assert get_confirmation_result("maybe") is None
    assert get_confirmation_result("hello jarvis") is None


# ==========================
# RUN TESTS
# ==========================

if __name__ == "__main__":

    test_shutdown_requires_confirmation()
    test_restart_requires_confirmation()
    test_delete_requires_confirmation()
    test_remove_requires_confirmation()
    test_safe_command_does_not_require_confirmation()
    test_ai_question_does_not_require_confirmation()

    test_yes_confirmation()
    test_no_confirmation()
    test_unknown_confirmation()

    print("All decision and confirmation tests passed.")