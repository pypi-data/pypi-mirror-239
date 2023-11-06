from __future__ import annotations
from typing import Any, Dict, Optional, Union
from typing_extensions import Literal
from pydantic import BaseModel, Field, Extra, field_validator, model_validator


def deserialize_arguments(value: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    import json
    if isinstance(value, str):
        try:
            return json.loads(value, strict=False)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON String: {value}")
    return value


class MessageFunctionCall(BaseModel):
    name: str
    """The name of the function."""
    arguments: Dict[str, Any] = Field(default_factory=dict)
    """The arguments of the function."""

    @field_validator('arguments', mode='before')
    @classmethod
    def _deserialize_arguments(cls, v):
        return deserialize_arguments(v)


class Message(BaseModel):
    """Base class for all messages."""
    content: Optional[str] = Field(default=None)
    """The string contents of a message."""

    role: Literal["user", "assistant", "function", "system"] = Field(default="user")
    """The role of the message."""

    name: Optional[str] = Field(default=None)
    """The name of the function"""

    function_call: Optional[MessageFunctionCall] = Field(default=None)
    """The function call of the message."""

    class Config:
        extra = Extra.allow

    @model_validator(mode='before')
    @classmethod
    def populate_name(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # Check if function_call is present
        if 'function_call' not in data:
            return data
        # Check if name is present
        if 'name' in data:
            return data
        # Populate name from function_call
        data['name'] = data.get('function_call', {}).get('name', None)
        return data

    def to_message(self) -> Dict[str, Any]:
        """Converts the message to a deserialized LLM message format."""

        if self.content is None and not(self.function_call and self.name):
            raise ValueError("Either content or function_call and name must be provided.")

        include_dict = {
            "content": ...,
            "role": ...,
            "name": ...,
            "function_call": {
                "name": ...,
                "arguments": ...,
            },
        }

        if not self.function_call:
            del include_dict['function_call']

        if not self.name:
            del include_dict['name']

        return self.model_dump(include=include_dict)

