import pickle
from processing.user_db import User


class DBWrapper:
    source_file = "./resources/users.pkl"

    def __init__(self):
        self.users_list = []

    def load_file(self, path=source_file):
        with open(path, "rb") as file:
            self.users_list = pickle.load(file)

    def save_file(self, path=source_file):
        with open(path, "wb") as file:
            pickle.dump(self.users_list, file)

    def add_label(self, user_id, label):
        for user in self.users_list:
            if user.aim_id == user_id:
                user.add_label(label)
                return
        user = User(user_id)
        user.add_label(label)
        self.users_list.append(user)

    def remove_label(self, user_id, label):
        for user in self.users_list:
            if user.aim_id == user_id:
                user.remove_label(label)
                if not user.get_labels():
                    self.users_list.remove(user)
                return

    def search_by_label(self, label):
        users = []
        for user in self.users_list:
            if label in user.labels:
                if user.aim_id not in users:
                    users.append(user.aim_id)
        return users

    def search_by_user(self, user_id):
        for user in self.users_list:
            if user.aim_id == user_id:
                return user.get_labels()
        return []
