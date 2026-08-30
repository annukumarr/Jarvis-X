from brain.safety import (
    is_dangerous_action,
    get_safety_message,
)


def test_shutdown_is_dangerous():

    assert is_dangerous_action("shutdown") is True


def test_restart_is_dangerous():

    assert is_dangerous_action("restart") is True


def test_unknown_action_is_safe():

    assert is_dangerous_action("open_chrome") is False


def test_shutdown_message():

    message = get_safety_message("shutdown")

    assert message is not None


def test_restart_message():

    message = get_safety_message("restart")

    assert message is not None


if __name__ == "__main__":

    test_shutdown_is_dangerous()
    test_restart_is_dangerous()
    test_unknown_action_is_safe()

    test_shutdown_message()
    test_restart_message()

    print("All safety tests passed.")