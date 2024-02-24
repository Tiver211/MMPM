import unittest
from manager import Path


class TestPath(unittest.TestCase):
    def test_parts(self):
        path = Path("test\\path\\file.txt")
        self.assertEqual(path.parts(), ["test", "path", "file.txt"])

    def test_expansion(self):
        path = Path("test\\path\\file.txt")
        self.assertEqual(path.expansion(), "txt")

    def test_directory(self):
        path = Path("test\\path\\file.txt")
        self.assertEqual(path.directory(), "test/path")

    def test_change_directory(self):
        path = Path("test\\path\\file.txt")
        self.assertEqual(path.change_directory("new"), "new/file.txt")


if __name__ == "__main__":
    unittest.main()
