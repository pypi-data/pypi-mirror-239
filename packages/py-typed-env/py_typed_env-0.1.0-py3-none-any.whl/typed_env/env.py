from .parser import parse
from .util import get_file_descending
from .typed_var import TypedVarDefinition
from .errors import Error, FileNotFound, SyntaxError, TypeError
from .constants import TEMPLATE_REGEX, STD_TYPES, KEY_REGEX

import os
import re
import json

from rich import print
from typing import Optional


class Env:
    def __init__(
        self, file_vars: dict[str, str], typed_vars: list[TypedVarDefinition] = []
    ) -> None:
        self.data = file_vars
        self.typed_vars = typed_vars

    def validate_and_parse(self) -> list[Error]:
        errors = []

        for typed_var in self.typed_vars:
            # Check if typed_var.name is a valid key
            if not re.match(KEY_REGEX, typed_var.name):
                errors.append(
                    SyntaxError(
                        f"Variable {typed_var.name} is not a valid key. Keys must match {KEY_REGEX}. (in typed_vars)"
                    )
                )
                continue

            if typed_var.name in self.data:
                value = self.data[typed_var.name]
                if typed_var.validate(value):
                    self.data[typed_var.name] = typed_var.parse(value)
                else:
                    errors.append(
                        TypeError(
                            f"Variable {typed_var.name} is not of type {typed_var.readable_type}."
                        )
                    )

            else:
                if typed_var.required:
                    errors.append(
                        TypeError(
                            f"Variable {typed_var.name} is required but not found."
                        )
                    )

        return errors

    def propagate_environ(self):
        for key, value in self.data.items():
            os.environ[key] = str(value)

    def __getitem__(self, key: str) -> str | None:
        if key in self.data:
            return self.data[key]
        elif key.upper() in self.data:
            return self.data[key.upper()]

        return None

    def get(self, key: str, default: any = None) -> str | None:
        if key in self.data:
            return self.data[key]

        return default

    def __repr__(self) -> str:
        return f"Env({json.dumps({'data': self.data, 'typed_vars': self.typed_vars}, indent=4)})"


def load_env(
    typed_vars: list[dict[str, str]] = [],
    /,
    filename: str = ".env",
    exit_on_error: bool = True,
) -> [Env, Optional[list[Error]]]:
    """Load the environment

    Args:
        typed_vars (list[dict[str, str]], optional): An array of variables whose types you want to define. Defaults to [].
        filename (str, optional): The filename of the .env file. Defaults to ".env".
        exit_on_error (bool, optional): Whether to exit if any error is thrown during parsing and loading. Defaults to True.

    Returns:
        [Env, Optional[list[Error]]]: Returns only the environment if exit_on_error is True, otherwise returns [None, list[Error]] or [Env, []].
    """

    file_path = get_file_descending(filename)
    if file_path is None:
        error = FileNotFound(
            f"The '{filename}'-file with read permissions could not found in any descending directory."
        )
        if exit_on_error:
            error.throw()
        return None, [error]

    with open(file_path, "r", encoding="UTF-8") as f:
        errors, file_vars = parse(f.read())

    if len(errors) > 0:
        if exit_on_error:
            for error in errors:
                print(error.message)
            exit(1)
        else:
            return None, errors

    env_vars = {}

    for var in file_vars:
        if not var["is_template"]:
            env_vars[var["name"]] = var["value"]
            continue

        templates = re.findall(TEMPLATE_REGEX, var["value"])

        for template in templates:
            val = None

            if template in env_vars:
                val = env_vars[template]
            elif (val := os.getenv(template)) != None:
                pass
            else:
                continue

            var["value"] = var["value"].replace(f"${{{template}}}", val)

        env_vars[var["name"]] = var["value"]

    env = Env({**os.environ, **env_vars}, typed_vars)
    errors = env.validate_and_parse()

    if len(errors) > 0:
        if exit_on_error:
            for error in errors:
                print(error.message)
            exit(1)
        else:
            return None, errors

    env.propagate_environ()

    if not exit_on_error:
        return env, []

    return env
