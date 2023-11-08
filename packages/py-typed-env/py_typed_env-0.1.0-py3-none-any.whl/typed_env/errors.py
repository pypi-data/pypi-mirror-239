from rich import print


class Error:
    def __init__(
        self,
        message: str,
        l_i: int | None = None,
        c_i: int | None = None,
        line: str | None = None,
    ) -> None:
        escaped_bracket = "\["
        self.message = (
            f"\[Typed-Env] [#fc03a1 bold]{self.__class__.__name__}[/#fc03a1 bold]: {message: <50}"
            + (f"@ {l_i + 1}:{c_i + 1}" if not c_i == None else "")
            + (
                (
                    f"\n    > {line.replace('[', escaped_bracket)}\n    > "
                    + (" " * c_i)
                    + "^ HERE\n"
                )
                if line
                else ""
            )
        )

    def throw(self) -> None:
        print(self.message)
        exit(1)


class SyntaxError(Error):
    pass


class FileNotFound(Error):
    pass


class VariableNotFound(Error):
    pass


class TypeError(Error):
    pass
