STD_TYPES = {
    bool: {
        "regex": r"^((t|T)rue|(f|F)alse|TRUE|FALSE)$",
        "parser": lambda x: x.lower() == "true",
    },
    int: {
        "regex": r"^-?\d+$",
        "parser": int,
    },
    float: {
        "regex": r"^-?\d+(\.\d+)?$",
        "parser": float,
    },
    str: {
        "regex": r".*",
        "parser": lambda x: x,
    },
}

ESCAPE_PATTERNS = [
    {
        "from": r"\n",
        "to": "\n",
    },
    {
        "from": r"\r",
        "to": "\r",
    },
    {
        "from": r"\t",
        "to": "\t",
    },
    {
        "from": r"\f",
        "to": "\f",
    },
    {
        "from": r"\b",
        "to": "\b",
    },
    {
        "from": r"\"",
        "to": '"',
    },
    {
        "from": r"\\'",
        "to": "'",
    },
    {
        "from": r"\\",
        "to": "\\",
    },
]

KEY_REGEX = r"^[a-zA-Z_]+[a-zA-Z0-9_]*$"
TEMPLATE_REGEX = r"\$\{([a-zA-Z_]+[a-zA-Z0-9_]*)\}"

OPTIONAL = "optional"
