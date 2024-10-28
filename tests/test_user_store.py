import pytest
from src.user_store import UserStore
import json
import os


@pytest.fixture(scope="module", autouse=True)
def setup_test_data():
    test_data = {
        "1": {
            "user_id": 1,
            "time": 60,
            "language": "English",
            "level": "A1",
            "topic": "Greetings",
        }
    }
    with open("test_user_data.json", "w") as f:
        json.dump(test_data, f)


@pytest.fixture(scope="module", autouse=True)
def cleanup_test_data():
    yield
    if os.path.exists("test_user_data.json"):
        os.remove("test_user_data.json")


def test_user_store():
    store = UserStore("test_user_data.json")
    store.add_user(2)
    assert store.check_user_exists(2) is True
    user = store.get_user(2)
    assert user.user_id == 2
    assert user.time is None
    assert user.language is None
    assert user.level is None
    assert user.topic is None
    store.set_user_preference(2, 60, "English", "A1", "Greetings")
    user = store.get_user(2)
    assert user.time == 60
    assert user.language == "English"
    assert user.level == "A1"
    assert user.topic == "Greetings"
    assert 2 == store.get_size()


def test_get_non_existent_user():
    store = UserStore("test_user_data.json")
    user = store.get_user(3)
    assert user is None
    assert store.check_user_exists(3) is False


def test_no_duplicate():
    store = UserStore("test_user_data.json")
    store.add_user(4)
    store.add_user(4)
    store.add_user(4)
    assert 2 == store.get_size()
