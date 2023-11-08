import json
import os


class DirectoryTreeBuilder:
    """
    A class for building a tree structure representing the directory and file hierarchy.

    Args:
        root_path (str): The path to the root directory to build the tree from.

    Attributes:
        root_path (str): The root directory path.

    Methods:
        build_tree: Recursively constructs a tree structure for the specified directory.
        to_json: Serializes the directory tree to JSON format.
    """

    def __init__(self, root_path):
        """
        Initialize the DirectoryTreeBuilder with a root directory path.

        Args:
            root_path (str): The path to the root directory to build the tree from.
        """
        self.root_path = root_path

    def build_tree(self):
        """
        Recursively constructs a tree structure for the specified directory.

        Returns:
            dict: A dictionary representing the directory and file hierarchy.
        """
        if not os.path.exists(self.root_path) or not os.path.isdir(self.root_path):
            raise ValueError("Invalid or non-existent directory path.")

        tree = self._build_tree_recursive(self.root_path)
        return tree

    def _build_tree_recursive(self, directory):
        """
        Recursively builds the directory tree.

        Args:
            directory (str): The current directory to build the tree from.

        Returns:
            dict: A dictionary representing the directory and file hierarchy.
        """
        tree = {"name": os.path.basename(directory), "type": "directory", "children": []}
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                tree["children"].append(self._build_tree_recursive(item_path))
            else:
                tree["children"].append({"name": item, "type": "file"})
        return tree

    def to_json(self):
        """
        Serializes the directory tree to JSON format.

        Returns:
            str: JSON representation of the directory tree.
        """
        tree = self.build_tree()
        return json.dumps(tree, indent=4)
