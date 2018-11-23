import pickle
from processing.user_db import User
import os.path


class DBWrapper:
    source_file = "./resources/users.pkl"

    def __init__(self):
        self.users_list = []

    def load_file(self, path=source_file):
        if os.path.exists(path):
            with open(path, "rb") as file:
                self.users_list = pickle.load(file)

    def save_file(self, path=source_file):
        with open(path, "wb") as file:
            pickle.dump(self.users_list, file)

    def add_label(self, user_id, label):
        for user in self.users_list:
            if user.aim_id == user_id:
                return user.add_label(label)
        user = User(user_id)
        user.add_label(label)
        self.users_list.append(user)
        return 2

    def remove_label(self, user_id, label):
        for user in self.users_list:
            if user.aim_id == user_id:
                removed = user.remove_label(label)
                if not user.get_labels():
                    self.users_list.remove(user)
                    return -1
                return removed
        return 0

    def search_by_raw_label(self, raw_label):
        users = []
        label_parts = raw_label.split(".")
        labels = [raw_label]
        for i in range(1, len(label_parts)):
            labels.append('.'.join(label_parts[0:i]))
        for label in labels:
            for user_id in self.search_by_label(label):
                if user_id not in users:
                    users.append(user_id)
        return users

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
