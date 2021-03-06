from typing import NamedTuple, Dict, List

from skadoo import utils


class Flag(NamedTuple):
    """
    Flag argument object.

    Attributes:
        name (str): Name of argument.
        flag (str): Long string format of flag (--name)
        description (string): Description of argument.
        called (bool): Boolean of if the argument is called. Defaults to False.
        short (str): Short-hand version of flag name. Defaults to "-[initials]".
        value (str): Value passed with flag argument. Defaults to "False".
        empty (bool): True if no value should be expected. Defaults to True.
    """

    name: str
    flag: str
    description: str
    called: bool
    short: str
    value: str
    empty: bool

    def validate(self):
        """Validate Flag composition."""

        if self.empty and self.value != "":
            raise ValueError(
                f"Cannot set value ({self.value}) for empty flag ({self.flag})"
            )

    def __str__(self) -> str:
        """
        Create string of Flag contents.

        Returns:
            str
        """
        return "\n ".join(
            [
                f"Flag ({self.flag})",
                f"Short ({self.short})",
                f"Name: {self.name}",
                f"Empty Arg: {self.empty}",
                f"Description: {self.description}",
            ]
        )

    def describe(self):
        """Print Flag content descriptions"""
        print(self.__str__())


def parse_flag(flag: str, short: str, empty: bool = False) -> str:
    """
    Parse flag argumnet for value. Defaults to True if exists but no falue passed.

    Args:
        flag (str): Flag passed via command line.
        short (str): Short version of flag argument.
        empty (bool): True if no value should be expected. Defaults to True.

    Returns:
        str
    """
    index = None
    parts = utils.get_command_parts()

    if flag not in parts and short not in parts:
        return "False"

    if empty:
        return "True"

    if flag in parts:
        index = parts.index(flag)

    if short in parts:
        index = parts.index(short)

    return parts[index + 1]


def create_flag(
    name: str,
    flag: str = "",
    description: str = "",
    short: str = "",
    value: str = "",
    empty: bool = False,
) -> Flag:
    """
    Create Flag argument.

    Args:
        name (str): Name of argument.
        flag (str, optional): Long version of flag string. Defaults to "--[name]".
        description (str, optional): Description of argument. Defaults to "".
        short (str, optional): Short-hand version of flag string. Defaults to "-[initials]".
        value (str, optional): Value passed with flag argument. Defaults to "False".
        empty (str, optional): True if no value should be expected. Defaults to True.

    Returns:
        Flag
    """
    flag_parts = utils.get_name_parts(name)

    if flag == "":
        flag = "--" + "-".join(flag_parts)

    if short == "":
        short = "-" + "".join([_[:1] for _ in flag_parts])

    called = utils.is_called(full=flag, abbreviation=short)

    if called:
        value = parse_flag(flag, short, empty)

    result = Flag(name, flag, description, called, short, value, empty)
    result.validate()

    return result
