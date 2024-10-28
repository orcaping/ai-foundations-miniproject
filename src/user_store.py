import json
import logging


class UserPreference:
    def __init__(self, user_id: int, time=None, language=None, level=None, topic=None):
        self.user_id = user_id
        self.time = time
        self.language = language
        self.level = level
        self.topic = topic

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "time": self.time,
            "language": self.language,
            "level": self.level,
            "topic": self.topic,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data["user_id"],
            time=data.get("time"),
            language=data.get("language"),
            level=data.get("level"),
            topic=data.get("topic"),
        )


class UserStore:
    def __init__(self, json_file="user_data.json"):
        logging.debug("Initializing UserStore")
        self.users = {}
        self.json_file = json_file
        self.load_from_json()

    def add_user(self, user_id):
        logging.debug(f"Adding user with ID: {user_id}")
        if user_id in self.users:
            return
        self.users[user_id] = UserPreference(user_id)
        self.save_to_json()

    def check_user_exists(self, user_id: int):
        exists = user_id in self.users
        logging.debug(f"Checking if user exists with ID: {user_id} - Exists: {exists}")
        return exists

    def get_user(self, user_id: int):
        user = self.users.get(user_id)
        logging.debug(f"Getting user with ID: {user_id} - User: {user}")
        return user

    def get_size(self):
        size = len(self.users)
        logging.debug(f"Getting size of user store - Size: {size}")
        return size

    def set_user_preference(self, user_id: int, time, language, level, topic):
        logging.debug(f"Setting preferences for user with ID: {user_id}")
        user = self.get_user(user_id)
        if user is None:
            user = UserPreference(user_id)
            self.users[user_id] = user

        user.time = time
        user.language = language
        user.level = level
        user.topic = topic
        self.save_to_json()

    def save_to_json(self):

        logging.debug("Saving users to JSON")
        with open(self.json_file, "w") as f:
            json.dump(
                {int(user_id): user.to_dict() for user_id, user in self.users.items()},
                f,
            )

    def load_from_json(self):
        logging.debug("Loading users from JSON")
        try:
            with open(self.json_file, "r") as f:
                data = json.load(f)
                self.users = {
                    int(user_id): UserPreference.from_dict(user_data)
                    for user_id, user_data in data.items()
                }
        except FileNotFoundError:
            self.users = {}
            logging.debug("No user data found.")
