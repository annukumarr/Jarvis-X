from brain.action_manager import (
    check_command,
    handle_confirmation,
)


def test_confirmation_flow():

    response = check_command("shutdown")

    assert response is not None

    result = handle_confirmation("yes")

    assert result["confirmed"] is True
    assert result["action"] == "shutdown"


def test_cancel_flow():

    response = check_command("restart")

    assert response is not None

    result = handle_confirmation("no")

    assert result["confirmed"] is False
    assert result["action"] == "restart"


def test_safe_command():

    response = check_command("open chrome")

    assert response is None


if __name__ == "__main__":

    test_confirmation_flow()
    test_cancel_flow()
    test_safe_command()

    print("All action manager tests passed.")