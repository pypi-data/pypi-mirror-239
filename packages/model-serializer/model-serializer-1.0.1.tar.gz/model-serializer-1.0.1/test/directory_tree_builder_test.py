import json
import os
import unittest

from app import DirectoryTreeBuilder


class TestDirectoryTreeBuilder(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with a predefined structure for testing
        self.test_dir = "test_directory"
        os.mkdir(self.test_dir)
        os.mkdir(os.path.join(self.test_dir, "dir1"))
        os.mkdir(os.path.join(self.test_dir, "dir2"))
        with open(os.path.join(self.test_dir, "file1.txt"), "w") as file:
            file.write("File 1 content")
        with open(os.path.join(self.test_dir, "dir1", "file2.txt"), "w") as file:
            file.write("File 2 content")

    def tearDown(self):
        # Remove the temporary test directory and its contents
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(self.test_dir)

    def test_build_tree(self):
        builder = DirectoryTreeBuilder(self.test_dir)
        tree = builder.build_tree()
        # Check if the root directory exists in the tree
        self.assertEqual(tree["name"], "test_directory")
        # Check if subdirectories and files exist in the tree
        self.assertTrue(any(item["name"] == "dir1" for item in tree["children"]))
        self.assertTrue(any(item["name"] == "dir2" for item in tree["children"]))
        self.assertTrue(any(item["name"] == "file1.txt" for item in tree["children"]))
        # Check the content of a nested file
        dir1 = next(item for item in tree["children"] if item["name"] == "dir1")
        file2 = next(item for item in dir1["children"] if item["name"] == "file2.txt")
        self.assertEqual(file2["name"], "file2.txt")
        self.assertEqual(file2["type"], "file")

    def test_build_tree_invalid_path(self):
        invalid_path = "non_existent_directory"
        builder = DirectoryTreeBuilder(invalid_path)
        # Check if an error is raised when providing an invalid path
        with self.assertRaises(ValueError):
            builder.build_tree()

    def test_to_json(self):
        builder = DirectoryTreeBuilder(self.test_dir)
        tree_json = builder.to_json()
        # Parse the JSON and check if it's a valid representation
        tree = json.loads(tree_json)
        self.assertEqual(tree["name"], "test_directory")
        self.assertTrue(any(item["name"] == "dir1" for item in tree["children"]))
        self.assertTrue(any(item["name"] == "dir2" for item in tree["children"]))
        self.assertTrue(any(item["name"] == "file1.txt" for item in tree["children"]))
        # Check if the JSON serialization is consistent with the tree structure
        self.assertEqual(json.dumps(tree, indent=4), tree_json)


if __name__ == "__main__":
    unittest.main()
