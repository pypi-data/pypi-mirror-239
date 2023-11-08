from .constants import OPTIONAL, STD_TYPES

from typing import Callable
import re


class RegexType:
    def __init__(self, regex: str) -> None:
        self.pattern = regex
        self.regex = re.compile(regex)


def regex(regex: str):
    """Define a regex to match the variable against.

    Args:
        regex (str): The regex pattern to match the variable against.
    """
    return RegexType(regex)


class TypedVarDefinition:
    def __init__(self, name: str, _type: Callable | RegexType, required: bool) -> None:
        self.type = _type
        self.name = name
        self.required = required
        self.readable_type = _type.__name__ if callable(_type) else "regex"

    def __repr__(self) -> str:
        return f"TypedVarDefinition(name={self.name}, type={self.type}, required={self.required})"

    def __str__(self) -> str:
        return self.__repr__()

    def validate(self, value: str) -> bool:
        if isinstance(self.type, RegexType):
            return self.type.regex.match(value) is not None
        else:
            t = STD_TYPES[self.type]
            if re.match(t["regex"], value):
                return True
            else:
                return False

    def parse(self, value: str) -> any:
        if not self.validate(value):
            return None

        if isinstance(self.type, RegexType):
            return value
        else:
            t = STD_TYPES[self.type]
            return t["parser"](value)


def v(name: str, type: Callable | RegexType, /, *args):
    """Define a typed variable.
    Pass the OPTIONAL constant as an argument to make the variable optional.

    Args:
        name (str): The name of the variable. Should be a valid environment variable name.
        type (Callable | RegexType): The type of the callable. For supported types, see the documentation.

    """
    return TypedVarDefinition(name, type, not OPTIONAL in args)
