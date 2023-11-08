# Model Serializer and Directory Tree Builder

This is a Python package that includes: ModelSerializer and DirectoryTreeBuilder. The package is designed to provide serialization and deserialization capabilities for Python objects, as well as the ability to create a tree structure representing the directory and file hierarchy of a specified directory.

## ModelSerializer

The ModelSerializer class is used to serialize Python objects into JSON format and deserialize JSON strings back into Python objects. It provides the following methods:

```python
__init__(self, model=None)
```
where `model`: The model object to serialize.

**[1.A]** Initialize the ModelSerializer with a model object.

```python
to_json(self, model=None)
```

**[1.B]** Serialize the model object to JSON.

where `model`: (optional) If provided, **[2.A]** serialize the specified model object, otherwise, **[2.B]** use the object provided during initialization.

```python
serialize_model(self, obj)
```
where `obj`: The object to be serialized.

**[3]** Recursively serialize a Python object into a JSON-serializable format.

```python
from_json(json_str)
```
where `json_str`: The JSON string to deserialize.

**[4]** Deserialize a JSON string into a Python object.

## DirectoryTreeBuilder

The DirectoryTreeBuilder class is used to create a tree structure that represents the directory and file hierarchy of a specified directory. It provides the following methods:

```python
__init__(self, root_path)
```
where `root_path`: The path to the root directory to build the tree from.

**[1]** Initialize the DirectoryTreeBuilder with a root directory path.

```python
build_tree(self)
```
_Returns:_ A dictionary representing the directory and file hierarchy.

**[2]** Recursively construct a tree structure for the specified directory.

```python
to_json(self)
```
_Returns:_ JSON representation of the directory tree.

**[3]** Serialize the directory tree to JSON format.

## Example Usage

Here's an example of how to use these classes:

```python
from model_serializer import ModelSerializer
from directory_tree_builder import DirectoryTreeBuilder

# Example for ModelSerializer
data = {"name": "John", "age": 30, "city": "New York"}
serializer = ModelSerializer(data)
json_data = serializer.to_json()

# Example for DirectoryTreeBuilder
root_directory = '/path/to/root/directory'
tree_builder = DirectoryTreeBuilder(root_directory)
directory_tree_json = tree_builder.to_json()
```

To install this package from PyPI, you can use pip:

```python
pip install model-serializer
```


# License

This package is distributed under the MIT License. Feel free to use it in your projects and contribute to its development on GitHub.

# Author

Made with ❤️ by Olger Chotza in Thessaloniki, Greece.

If you encounter any issues, have questions, or want to contribute to the development of this package, please visit the GitHub repository and create an issue or pull request.

Thank you for using the Model Serializer and Directory Tree Builder package!