from processing.user_db import User
import unittest


class UserTest(unittest.TestCase):

    def test_create(self):
        u = User("id1")
        self.assertEqual("id1", u.aim_id)
        self.assertEqual([], u.get_labels())

    def test_add_label(self):
        u = User("id2")
        u.add_label("l1")

        self.assertEqual("id2", u.aim_id)
        self.assertEqual(["l1"], u.get_labels())

    def test_add_many_labels(self):
        u = User("id3")
        self.assertEqual([], u.get_labels())
        u.add_label("l1")
        self.assertEqual(["l1"], u.get_labels())
        u.add_label("l2")
        self.assertEqual(["l1", "l2"], u.get_labels())
        u.add_label("l2")
        self.assertEqual(["l1", "l2"], u.get_labels())
        u.add_label("l4")
        self.assertEqual(["l1", "l2", "l4"], u.get_labels())
        u.add_label("l3")
        self.assertEqual(["l1", "l2", "l4", "l3"], u.get_labels())
        u.add_label("l4")
        self.assertEqual(["l1", "l2", "l4", "l3"], u.get_labels())
        u.add_label("l1")
        self.assertEqual(["l1", "l2", "l4", "l3"], u.get_labels())
        self.assertEqual("id3", u.aim_id)

    def test_remove_label(self):
        u = User("id4")
        u.add_label("l1")
        u.add_label("l2")
        u.add_label("l3")
        self.assertEqual("id4", u.aim_id)
        self.assertEqual(["l1", "l2", "l3"], u.get_labels())
        u.remove_label("l2")
        self.assertEqual("id4", u.aim_id)
        self.assertEqual(["l1", "l3"], u.get_labels())
        u.remove_label("l5")
        self.assertEqual("id4", u.aim_id)
        self.assertEqual(["l1", "l3"], u.get_labels())
        u.remove_label("l1")
        self.assertEqual("id4", u.aim_id)
        self.assertEqual(["l3"], u.get_labels())
        u.remove_label("l3")
        self.assertEqual("id4", u.aim_id)
        self.assertEqual([], u.get_labels())


if __name__ == '__main__':
    unittest.main()
