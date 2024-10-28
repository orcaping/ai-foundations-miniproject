import json


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
        self.users = {}
        self.json_file = json_file
        self.load_from_json()

    def add_user(self, user_id):
        self.users[user_id] = UserPreference(user_id)
        self.save_to_json()

    def check_user_exists(self, user_id: int):
        return user_id in self.users

    def get_user(self, user_id: int):
        return self.users.get(user_id)

    def get_size(self):
        return len(self.users)

    def set_user_preference(self, user_id: int, time, language, level, topic):
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
        with open(self.json_file, "w") as f:
            json.dump(
                {user_id: user.to_dict() for user_id, user in self.users.items()}, f
            )

    def load_from_json(self):
        try:
            with open(self.json_file, "r") as f:
                data = json.load(f)
                self.users = {
                    user_id: UserPreference.from_dict(user_data)
                    for user_id, user_data in data.items()
                }
        except FileNotFoundError:
            self.users = {}
            print("No user data found.")
