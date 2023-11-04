def check(string: str, *alphabets: str) -> bool:
    """
    Check if a string is present in any of the specified alphabets.

    :param string: The string to be checked.
    :param alphabets: One or more alphabets as variable arguments.
    :return: True if the string is found in any of the alphabets, False otherwise.
    """

    for alphabet in alphabets:
        if string in alphabet:
            return True

    return False


def is_contains_spaces(string: str) -> bool:
    """
    Check if a string contains any space characters.

    :param string: The string to be checked.
    :return: True if the string contains spaces, False otherwise.
    """

    return any(char.isspace() for char in string)


def is_contains_alphabetic(string: str) -> bool:
    """
    Check if a string contains any alphabetic characters.

    :param string: The string to be checked.
    :return: True if the string contains alphabetic characters, False otherwise.
    """

    return any(char.isalpha() for char in string)


def is_contains_digits(string: str) -> bool:
    """
    Check if a string contains any numeric digits.

    :param string: The string to be checked.
    :return: True if the string contains numeric digits, False otherwise.
    """

    return any(char.isdigit() for char in string)


def is_contains_lowercase(string: str) -> bool:
    """
    Check if a string contains any lowercase letters.

    :param string: The string to be checked.
    :return: True if the string contains lowercase letters, False otherwise.
    """

    return any(char.islower() for char in string)


def is_contains_uppercase(string: str) -> bool:
    """
    Check if a string contains any uppercase letters.

    :param string: The string to be checked.
    :return: True if the string contains uppercase letters, False otherwise.
    """

    return any(char.isupper() for char in string)


def is_contains_special(string: str) -> bool:
    """
    Check if a string contains any special characters.

    :param string: The string to be checked.
    :return: True if the string contains special characters, False otherwise.
    """

    return any(not char.isalnum() for char in string)


def is_contains_substring(string: str, substring: str) -> bool:
    """
    Check if a string contains a specific substring.

    :param string: The string to be checked.
    :param substring: The substring to search for.
    :return: True if the string contains the provided substring, False otherwise.
    """

    return substring in string
