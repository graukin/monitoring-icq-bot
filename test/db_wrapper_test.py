import unittest
from processing.db_wrapper import DBWrapper
import os


class DbWrapperTest(unittest.TestCase):
    pkl_file = "./users.pkl"

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

    def test_search_raw_labels(self):
        w = DBWrapper()
        w.add_label("id1", "a")
        w.add_label("id1", "b")
        w.add_label("id2", "a.b")
        w.add_label("id2", "c")
        w.add_label("id3", "a.b.c")
        w.add_label("id3", "d")
        w.add_label("id4", "a.b.c.d")
        w.add_label("id5", "b.c.d")
        w.add_label("id6", "a.b")

        self.assertEqual(["id1"], w.search_by_raw_label("a"), msg="check 'a'")
        self.assertEqual(["id1"], w.search_by_raw_label("b"), msg="check 'b'")
        self.assertEqual(["id2"], w.search_by_raw_label("c"), msg="check 'c'")
        self.assertEqual(["id3"], w.search_by_raw_label("d"), msg="check 'd'")
        self.assertEqual(["id2", "id6", "id1"], w.search_by_raw_label("a.b"), msg="check 'a.b'")
        self.assertEqual(["id3", "id1", "id2", "id6"], w.search_by_raw_label("a.b.c"), msg="check 'a.b.c'")
        self.assertEqual(["id4", "id1", "id2", "id6", "id3"], w.search_by_raw_label("a.b.c.d"), msg="check 'a.b.c.d'")
        self.assertEqual([], w.search_by_raw_label("e"), msg="check 'e'")

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
        w.save_file(self.pkl_file)

        w2 = DBWrapper()
        w2.load_file(self.pkl_file)
        self.assertEqual([], w2.search_by_label("l0"))
        self.assertEqual(["id1"], w2.search_by_label("l1"))
        self.assertEqual(["id1", "id2"], w2.search_by_label("l2"))
        self.assertEqual(["id3"], w2.search_by_label("l3"))
        self.assertEqual(["id1", "id3"], w2.search_by_label("l4"))
        self.assertEqual(["id1", "id2"], w2.search_by_label("l5"))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.pkl_file):
            os.remove(cls.pkl_file)


if __name__ == '__main__':
    unittest.main()
