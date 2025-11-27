import secrets
import string


def generate_code(digits: int = 12) -> str:
    """
    Generate a random alphanumeric code

    :param digits: Length of the code. Default is 12.
    :type digits: int
    :return: A random code containing lowercase, uppercase letters and digits.

    Example:
    >>> generate_code()
    'zP9y6E8a0noh'
    >>> generate_code(5)
    'T7puZ'
    """
    characters = string.ascii_letters + string.digits

    return "".join(secrets.choice(characters) for _ in range(digits))
