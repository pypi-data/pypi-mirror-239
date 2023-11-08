import json


class ModelSerializer:
    def __init__(self, model=None):
        """
        Initialize the ModelSerializer with a model object.

        :param model: The model object to serialize.
        """
        self.model = model

    def to_json(self, model=None):
        """
        Serialize the model object to JSON.

        :return: JSON representation of the model.
        """
        model_dict = self.serialize_model(self.model if model is None else model)
        json_str = json.dumps(model_dict, indent=4)
        return json_str

    def serialize_model(self, obj):
        """
        Recursively serialize a Python object into a JSON-serializable format.

        :param obj: The object to be serialized.
        :return: JSON-serializable data.
        """
        if obj is None:
            raise ValueError("Cannot serialize None object.")

        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        elif isinstance(obj, list):
            return [self.serialize_model(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.serialize_model(value) for key, value in obj.items()}
        elif hasattr(obj, '__dict__'):
            model_dict = {key: self.serialize_model(value) for key, value in obj.__dict__.items()}
            model_dict['__class__'] = obj.__class__.__name__
            return model_dict
        else:
            raise ValueError(f"Unsupported data type: {type(obj).__name__}")

    @staticmethod
    def from_json(json_str):
        """
        Deserialize a JSON string into a Python object.

        :param json_str: The JSON string to deserialize.
        :return: Deserialized Python object.
        """
        try:
            data = json.loads(json_str)
            if '__class__' in data:
                class_name = data.pop('__class__')
                cls = globals().get(class_name)
                if cls:
                    return cls(**data)
                else:
                    raise ValueError(f"Unknown class: {class_name}")
            else:
                return data
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decoding error: {e}")
