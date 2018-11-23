import unittest
from processing.db_wrapper import DBWrapper


class DbWrapperTest(unittest.TestCase):
    def test_add_users(self):
        w = DBWrapper()
        w.add_label("id1", "l1")
        w.add_label("id1", "l2")
        w.add_label("id2", "l2")
        w.add_label("id3", "l3")
        self.assertEqual(3, len(w.users_list))

    def test_search_users(self):
        w = DBWrapper()
        w.add_label("id1", "l1")
        w.add_label("id1", "l2")
        w.add_label("id1", "l4")
        w.add_label("id1", "l5")
        w.add_label("id2", "l2")
        w.add_label("id2", "l5")
        w.add_label("id3", "l3")
        w.add_label("id3", "l4")
        self.assertEqual([], w.search_by_label("l0"))
        self.assertEqual(["id1"], w.search_by_label("l1"))
        self.assertEqual(["id1", "id2"], w.search_by_label("l2"))
        self.assertEqual(["id3"], w.search_by_label("l3"))
        self.assertEqual(["id1", "id3"], w.search_by_label("l4"))
        self.assertEqual(["id1", "id2"], w.search_by_label("l5"))

    def test_remove_labels(self):
        w = DBWrapper()
        w.add_label("id1", "l1")
        w.add_label("id1", "l2")
        w.add_label("id2", "l2")
        w.add_label("id3", "l2")
        self.assertEqual(["id1"], w.search_by_label("l1"))
        self.assertEqual(["id1", "id2", "id3"], w.search_by_label("l2"))

        w.remove_label("id4", "l3")
        self.assertEqual(["id1"], w.search_by_label("l1"))
        self.assertEqual(["id1", "id2", "id3"], w.search_by_label("l2"))

        w.remove_label("id1", "l2")
        self.assertEqual(["id1"], w.search_by_label("l1"))
        self.assertEqual(["id2", "id3"], w.search_by_label("l2"))

        w.remove_label("id1", "l1")
        self.assertEqual([], w.search_by_label("l1"))
        self.assertEqual(["id2", "id3"], w.search_by_label("l2"))

        w.remove_label("id2", "l2")
        self.assertEqual([], w.search_by_label("l1"))
        self.assertEqual(["id3"], w.search_by_label("l2"))

        w.remove_label("id3", "l2")
        self.assertEqual([], w.search_by_label("l1"))
        self.assertEqual([], w.search_by_label("l2"))
        self.assertEqual(0, len(w.users_list))

    def test_pickle(self):
        w = DBWrapper()
        w.add_label("id1", "l1")
        w.add_label("id1", "l2")
        w.add_label("id1", "l4")
        w.add_label("id1", "l5")
        w.add_label("id2", "l2")
        w.add_label("id2", "l5")
        w.add_label("id3", "l3")
        w.add_label("id3", "l4")
        self.assertEqual([], w.search_by_label("l0"))
        self.assertEqual(["id1"], w.search_by_label("l1"))
        self.assertEqual(["id1", "id2"], w.search_by_label("l2"))
        self.assertEqual(["id3"], w.search_by_label("l3"))
        self.assertEqual(["id1", "id3"], w.search_by_label("l4"))
        self.assertEqual(["id1", "id2"], w.search_by_label("l5"))
        w.save_file("./users.pkl")

        w2 = DBWrapper()
        w2.load_file("./users.pkl")
        self.assertEqual([], w2.search_by_label("l0"))
        self.assertEqual(["id1"], w2.search_by_label("l1"))
        self.assertEqual(["id1", "id2"], w2.search_by_label("l2"))
        self.assertEqual(["id3"], w2.search_by_label("l3"))
        self.assertEqual(["id1", "id3"], w2.search_by_label("l4"))
        self.assertEqual(["id1", "id2"], w2.search_by_label("l5"))


if __name__ == '__main__':
    unittest.main()
