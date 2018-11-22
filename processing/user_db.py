class User:
    def __init__(self, aim_id):
        self.aim_id = aim_id
        self.labels = []

    def add_label(self, label):
        if label not in self.labels:
            self.labels.append(label)

    def remove_label(self, label):
        if label in self.labels:
            self.labels = [l for l in self.labels if l != label]

    def get_labels(self):
        return self.labels
