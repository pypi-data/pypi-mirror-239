import unittest

from app import ModelSerializer


class TestModelSerializer(unittest.TestCase):
    def test_serialize_deserialize(self):
        # Create an object to serialize
        data = {
            'name': 'John',
            'age': 30,
            'is_student': False
        }

        serializer = ModelSerializer(data)
        json_data = serializer.to_json()

        # Deserialize and check if the result matches the original data
        deserialized_data = ModelSerializer.from_json(json_data)
        self.assertEqual(data, deserialized_data)

    def test_serialize_unsupported_type(self):
        # Attempt to serialize an unsupported data type
        unsupported_data = complex(3, 4)
        serializer = ModelSerializer(unsupported_data)

        # Verify that a ValueError is raised
        with self.assertRaises(ValueError):
            serializer.to_json()

    def test_deserialize_invalid_json(self):
        # Attempt to deserialize invalid JSON
        invalid_json = '{"name": "Alice, "age": 25}'

        # Verify that a ValueError is raised due to JSON decoding error
        with self.assertRaises(ValueError):
            ModelSerializer.from_json(invalid_json)

    def test_deserialize_unknown_class(self):
        # Attempt to deserialize JSON with an unknown class
        json_data = '{"__class__": "NonExistentClass", "value": 42}'

        # Verify that a ValueError is raised due to an unknown class
        with self.assertRaises(ValueError):
            ModelSerializer.from_json(json_data)

    def test_serialize_dict_with_nested_dict(self):
        # Serialize a dictionary with nested dictionaries
        data = {
            'name': 'John',
            'address': {
                'street': '123 Main St',
                'city': 'Exampleville'
            }
        }

        serializer = ModelSerializer(data)
        json_data = serializer.to_json()

        # Deserialize and check if the result matches the original data
        deserialized_data = ModelSerializer.from_json(json_data)
        self.assertEqual(data, deserialized_data)

    def test_serialize_empty_data(self):
        # Serialize an empty dictionary
        data = {}
        serializer = ModelSerializer(data)
        json_data = serializer.to_json()

        # Deserialize and check if the result matches the original data
        deserialized_data = ModelSerializer.from_json(json_data)
        self.assertEqual(data, deserialized_data)


if __name__ == '__main__':
    unittest.main()
