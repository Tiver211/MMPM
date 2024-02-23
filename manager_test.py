import unittest
from manager import Path as PathStr, NotFile


class TestPathStr(unittest.TestCase):
    def setUp(self):
        self.path = PathStr("/path/to/file.txt")

    def test_parts(self):
        self.assertEqual(self.path.parts(), ["", "path", "to", "file.txt"])

    def test_expansion(self):
        self.assertEqual(self.path.expansion(), "txt")

    def test_directory(self):
        self.assertEqual(self.path.directory(), "/path/to")

    def test_change_directory(self):
        self.assertEqual(self.path.change_directory("/new/path"), "/new/path/file.txt")

    def test_not_file(self):
        with self.assertRaises(NotFile):
            PathStr("/path/to/file").expansion()


if __name__ == "__main__":
    unittest.main()
