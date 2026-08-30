from brain.action_executor import (
    SAFETY_DELAY,
    schedule_shutdown,
    schedule_restart,
    cancel_system_action,
)


def test_safety_delay():

    assert SAFETY_DELAY == 5


def test_functions_exist():

    assert callable(schedule_shutdown)
    assert callable(schedule_restart)
    assert callable(cancel_system_action)


if __name__ == "__main__":

    test_safety_delay()
    test_functions_exist()

    print("Action executor safety tests passed.")