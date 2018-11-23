class User:
    def __init__(self, aim_id):
        self.aim_id = aim_id
        self.labels = []

    def add_label(self, label):
        if label not in self.labels:
            self.labels.append(label)
            return 1
        return 0

    def remove_label(self, label):
        l1 = len(self.labels)
        if label in self.labels:
            self.labels = [lbl for lbl in self.labels if lbl != label]
        l2 = len(self.labels)
        return l1 - l2

    def get_labels(self):
        return self.labels
