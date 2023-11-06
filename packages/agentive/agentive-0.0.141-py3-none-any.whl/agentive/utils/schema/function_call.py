from __future__ import annotations
from functools import wraps
from pydantic import BaseModel, Extra, validate_arguments
from typing import Callable, Any, Dict

from agentive.utils.schema.message import Message
from agentive.utils.dict_utils import remove_keys_recursively


def validate_function_call(message: Dict[str, Any], schema: Dict[str, Any], throw_error: bool=True) -> bool:
    if throw_error:
        assert "function_call" in message, "No function call detected"
        assert message["function_call"]["name"] == schema["name"], "Function name does not match"
    return throw_error


class BaseTool(BaseModel):
    class Config:
        extra = Extra.allow


class FunctionCall(BaseTool):
    """
    FunctionCall is a base class that standardizes function calls, particularly within language-learning models or APIs.
    It leverages Pydantic's BaseModel for input validation and schema generation.

    Class Methods:
    - _generate_schema_parameters: Generates parameters for a function call schema.
    - function_call_schema: Generates the full schema of the function call, including the name and required parameters.
    - _validate_function_call: Validates whether the message has a 'function_call' field and if the name matches the schema.
    - from_message: Creates an instance from a Message schema.
    - from_response: Creates an instance from an OpenAI API response.
    - run: Runs the function with the given arguments.

    Example:
    ```python
    class MyFunction(FunctionCall):
        arg1: int
        arg2: str
    ```

    Attributes:
    Inherits attributes from Pydantic's BaseModel.
    """

    @classmethod
    def _generate_schema_parameters(cls):
        schema = cls.model_json_schema()
        parameters = {
            k: v for k, v in schema.items() if k not in ("title", "description")
        }
        parameters["required"] = sorted(
            k for k, v in parameters["properties"].items() if not "default" in v
        )

        if "description" not in schema:
            schema[
                "description"
            ] = f"Correctly extracted `{cls.__name__}` with all the required parameters with correct types"

        parameters = remove_keys_recursively(parameters, "additionalProperties")
        parameters = remove_keys_recursively(parameters, "title")

        return schema, parameters

    @classmethod
    @property
    def function_call_schema(cls):
        schema, parameters = cls._generate_schema_parameters()
        return {
            "name": schema["title"],
            "description": schema["description"],
            "parameters": parameters,
        }

    @classmethod
    def _validate_function_call(cls, message, throw_error=True):
        validate_function_call(message, cls.function_call_schema, throw_error)

    @classmethod
    def from_message(cls, message: Message, throw_error=True):
        if throw_error:
            # Check that the message has a function call associated
            assert message.function_call, "No function call detected"
            # Check if the function name in the message matches the schema
            assert message.name == cls.function_call_schema['name'], "Function name does not match"
        return cls(**message.function_call.arguments)

    @classmethod
    def from_response(cls, completion, throw_error=True):
        import json
        import warnings

        warnings.warn(
            "from_response is deprecated and won't be supported for future versions of Agentive. Please use from_message instead.",
            DeprecationWarning
        )

        message = completion.choices[0].message
        if throw_error:
            # Check if the message has a "function_call" key
            assert "function_call" in message, "No function call detected"
            # Check if the function name in the message matches that in the schema
            assert message["function_call"]["name"] == cls.function_call_schema["name"], "Function name does not match"

        arguments = json.loads(message["function_call"]["arguments"], strict=False)
        return cls(**arguments)

    @classmethod
    def run(cls, arguments):
        return cls(**arguments)


class function_call(BaseTool):
    """
    Decorator to convert a function into a function call for an LLM.

    This decorator will convert a function into a function call for an LLM. The
    function will be validated using pydantic and the schema will be
    generated from the function signature.

    Example:
        ```python
        @function_call
        def sum(a: int, b: int) -> int:
            return a + b
        ```

    Methods:
    - __init__: Initializes the decorator with the function to wrap.
    - _generate_function_call_schema: Generates the schema based on the function signature.
    - __call__: Makes the class instance callable, effectively wrapping the decorated function.
    - _validate_function_call: Validates a message against the function call schema.
    - from_message: Creates an instance from a Message schema.
    - from_response: Creates an instance from an OpenAI API response.
    - run: Runs the function with the given arguments.

    Attributes:
    - func: The function that is being decorated.
    - validate_func: A function that wraps the original function, adding Pydantic validation.
    - function_call_schema: The generated schema for the function call.

        **INSPIRED BY JASON LIU'S EXCELLENT OPENAI_FUNCTION_CALL, NOW INSTRUCTOR, PACKAGE**
    """

    def __init__(self, func: Callable) -> None:
        super().__init__()
        self.func = func
        self.validate_func = validate_arguments(func)
        self.function_call_schema = self._generate_function_call_schema()

    def _generate_function_call_schema(self) -> Dict[str, Any]:
        schema = self.validate_func.model.model_json_schema()
        relevant_properties = {
            k: v for k, v in schema["properties"].items()
            if k not in ("v__duplicate_kwargs", "args", "kwargs")
        }

        schema["properties"] = relevant_properties

        schema["required"] = sorted(
            k for k, v in relevant_properties.items() if "default" not in v
        )

        schema = remove_keys_recursively(schema, "additionalProperties")
        schema = remove_keys_recursively(schema, "title")

        return {
            "name": self.func.__name__,
            "description": self.func.__doc__,
            "parameters": schema,
        }

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        @wraps(self.func)
        def wrapper(*args, **kwargs):
            return self.validate_func(*args, **kwargs)
        return wrapper(*args, **kwargs)

    def _validate_function_call(self, message: Dict[str, Any], throw_error: bool = True) -> None:
        validate_function_call(message, self.function_call_schema, throw_error)

    def from_message(self, message: Message, throw_error: bool = True) -> Any:
        if throw_error:
            assert message.function_call, "No function call detected"
            assert message.name == self.function_call_schema['name'], "Function name does not match"
        return self.validate_func(**message.function_call.arguments)

    def from_response(self, completion: Any, throw_error: bool = True) -> Any:
        import json
        import warnings

        warnings.warn(
            "from_response is deprecated and won't be supported for future versions of Agentive. Please use from_message instead.",
            DeprecationWarning
        )

        message = completion.choices[0].message
        if throw_error:
            assert "function_call" in message, "No function call detected"
            assert message["function_call"]["name"] == self.function_call_schema["name"], "Function name does not match"
        return self.validate_func(**json.loads(message["function_call"]["arguments"], strict=False))

    def run(self, arguments):
        return self.validate_func(**arguments)
