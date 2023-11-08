from .constants import KEY_REGEX, ESCAPE_PATTERNS
from .errors import Error, SyntaxError

import re


def escape(value: str) -> str:
    res = value

    for pattern in ESCAPE_PATTERNS:
        res = res.replace(pattern["from"], pattern["to"])

    # # Replace unicode escape sequences
    # matches = re.findall("\\\\u[0-9]{4}", res)
    # # Replace all regex matches with the actual unicode character
    # for match in matches:
    #     res = res.replace(match, chr(int(match[2:], 16)))

    return res


def parse(content: str) -> [list[Error], list[dict[str, str]]]:
    errors = []
    pairs = []

    curr_name = ""
    curr_value = ""

    env_pos = 0

    in_quotes = False
    quote_char = ""

    error = None

    in_multiline = False
    quote_level_max = 0
    quote_level = 0

    line_nr_start = 0
    lines = []

    for line_nr, line in enumerate(content.splitlines()):
        if not in_multiline:
            curr_name = ""
            curr_value = ""

            env_pos = 0

            in_quotes = False
            quote_char = ""

            error = None

            quote_level_max = 0
            quote_level = 0

            line_nr_start = line_nr
            lines = []

        lines.append(line)

        for char_nr, char in enumerate(line):
            if not in_quotes and char == "#":
                break

            if (char == '"' or char == "'") and env_pos == 1:
                if in_quotes and (not len(curr_value) == 0 or quote_level_max == 3):
                    if quote_char == char:
                        if char_nr != 0:
                            if line[char_nr - 1] == "\\":
                                curr_value += char
                                continue
                        quote_level -= 1

                        if quote_level > 0 and quote_level != 3 and in_multiline:
                            if char_nr + 1 == len(line):
                                in_multiline = False
                                error = SyntaxError(
                                    f"Missing closing quote (Unexpected EOL)",
                                    line_nr,
                                    char_nr + 1,
                                    line,
                                )
                                break

                            if not line[char_nr + 1] == quote_char:
                                in_multiline = False
                                error = SyntaxError(
                                    f"Missing closing quote (Unexpected character)",
                                    line_nr,
                                    char_nr + 1,
                                    line,
                                )
                                break

                        if quote_level == 0:
                            in_quotes = False

                            if in_multiline:
                                in_multiline = False
                                continue

                        continue

                else:
                    if not len(curr_value) == 0:
                        error = SyntaxError(f"Unexpected quote", line_nr, char_nr, line)
                        break

                    quote_level_max += 1
                    quote_level += 1

                    in_quotes = True
                    quote_char = char

                    if quote_level_max >= 1 and char != quote_char:
                        error = SyntaxError(
                            f"Unexpected quote (Expected {'double' if ord(quote_char) == 34 else 'single'} quote)",
                            line_nr,
                            char_nr,
                            line,
                        )
                        break

                    if quote_level_max == 3:
                        in_multiline = True

                    continue

            if not in_quotes and char == " ":
                continue

            if env_pos == 0:
                if char == "=":
                    env_pos = 1
                    continue

                curr_name += char

                if char_nr == len(line) - 1:
                    error = SyntaxError(
                        f"Missing '=' (Unexpected EOL)", line_nr, char_nr + 1, line
                    )
                    break

            elif env_pos == 1:
                if not in_quotes and char == " ":
                    break

                curr_value += char

                if char_nr == len(line) - 1 and in_quotes:
                    if not in_multiline:
                        error = SyntaxError(
                            f"Missing closing quote (Unexpected EOL)",
                            line_nr,
                            char_nr + 1,
                            line,
                        )
                        break

                    curr_value += "\n"

            if error:
                in_multiline = False

        if curr_name == "":
            continue

        if error:
            errors.append(error)
        else:
            if not in_multiline:
                if not re.match(KEY_REGEX, curr_name):
                    # Get mismatching character
                    mismatch_char = 0
                    for i in range(len(curr_name)):
                        if not re.match(KEY_REGEX, curr_name[: i + 1]):
                            mismatch_char = i

                    errors.append(
                        SyntaxError(
                            f"Invalid name (Pattern mismatch)",
                            line_nr,
                            mismatch_char,
                            line,
                        )
                    )
                    continue

                pairs.append(
                    {
                        "name": curr_name,
                        "value": escape(curr_value),
                        "is_template": quote_char == '"' or quote_level_max == 0,
                        "line_nr_start": line_nr_start,
                        "lines": lines,
                    }
                )

    return [errors, pairs]
