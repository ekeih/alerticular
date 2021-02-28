from unittest.mock import Mock


def get_test_json(name: str) -> dict or None:
    """
    Reads a JSON file from the tests directory
    :param name:
    :return: the parsed json file content
    """
    import json

    with open(f"tests/{name}.json", "r") as f:
        return json.loads(f.read())


def get_mock_coro(return_value) -> Mock:
    """
    Get a coroutine Mock which returns the given value
    :param return_value:
    :return: mocked coroutine
    """

    async def mock_coro(*args, **kwargs):
        return return_value

    return Mock(wraps=mock_coro)
