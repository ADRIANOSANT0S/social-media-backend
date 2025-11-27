import re

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email as django_validate_email

from apps.core.contracts.lang import LANGUAGES

from ..models import User

ALLOWED_CHARS_REGEX = r"A-Za-zÀ-ÿ\s.'-"


def validate_name(name: str) -> str:
    """
    Validate the first name.
    1. Check if the first name start with a letter.
    2. Check if the first name contains only allowed characters (letters, apostrophes, spaces, and hyphens).
    3. Check if the first name length is between 2 and 50 characters.
    Raise a ValidationError if the first name is invalid.
    """

    if not re.match(rf"^[A-Za-zÀ-ÿ][{ALLOWED_CHARS_REGEX}]{{1,99}}$", name):
        raise ValueError(
            "Name must be 2-100 chars, letters, apostrophes, spaces, periods, hyphen."
        )
    return name


def validate_age(age: int | str) -> int:
    """
    Validate the age.
    1. Check if the age is a digit and convert it to an integer.
    2. Check if the age is between 18 and 100 years.
    Raise a ValidationError if the age is invalid.
    """

    if isinstance(age, str):
        if not age.isdigit():
            raise ValueError("Age must be contain ony digits.")
        age = int(age)

    if age < 18 or age > 100:
        raise ValueError("Age must be between 18 and 100 years.")
    return age


def validate_email(email: str) -> str:
    """
    Validate the email.
    1. Check if the email format is valid using Django's built-in validator.
    2. Check if the email already exists in the database.
    Raise a ValidationError if the email is invalid or already exists.
    """

    try:
        django_validate_email(email)
    except DjangoValidationError:
        raise ValueError("Invalid email format.")
    if User.objects.filter(email=email).exists():
        raise ValueError("Email already exists.")
    return email


def validate_password(password):
    """
    Validate the password.
    1. Check the password is between 12 and 100 characters long.
    2. Check the password contains at least one uppercase letter, one lowercase letter, one number, and one special character.
    Raise a ValidationError if the password is invalid.
    """

    PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{12,100}$"
    if not re.match(PASSWORD_REGEX, password):
        raise ValueError(
            "Password must contain at least 12 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character."
        )
    return password


def validate_avatar(avatar: str | None) -> str | None:
    """
    Validate the avatar.
    1. Check if the avatar is a valid url.
    2. Check if the avatar is not a object.
    Raise a ValidationError if the avatar is invalid.
    """

    if not avatar:
        return None

    if avatar is not None and not isinstance(avatar, str):
        raise ValueError("Avatar must be a valid URL string or None.")

    if avatar and not avatar.startswith(("http://", "https://")):
        raise ValueError(
            "Avatar must be a valid URL starting with http:// or https://."
        )

    return avatar


def validate_username(username: str) -> str:
    """
    Validate the username.
    1. Check if the username is between 3 and 15 characters long.
    2. check if the username contains only allowed characters (letters, numbers, underscores).
    3. Check if the username starts with a letter.
    4. Check if the username is not already exists in the database.
    Raise a ValidationError if the username is invalid.
    """

    USERNAME_REGEX = r"^[A-Za-z][A-Za-z0-9_]{2,14}$"
    if not re.match(USERNAME_REGEX, username):
        raise ValueError("User must be 3-15 chars, letters numbers, underscores.")
    if User.objects.filter(username=username).exists():
        raise ValueError("Username already exists.")
    return username


def validate_banner(banner: str | None) -> str | None:
    """
    Validate the banner.
    1. Check banner is None
    2. Check banner has a valid URL
    Raise a ValidationError if the banner is invalid.
    """

    if not banner:
        return None

    if banner is not None and not isinstance(banner, str):
        raise ValueError("banner must be a valid URL string or None.")

    if banner and not banner.startswith(("http://", "https://")):
        raise ValueError(
            "banner must be a valid URL starting with http:// or https://."
        )

    return banner


def validate_bio(bio: str | None) -> str | None:
    """
    Validate the bio.
    1. Check the bio is none
    2. Check the bio must be most 150.
    Raise a ValidationError if the bio is invalid.
    """

    if not bio:
        return None

    if len(bio) > 150:
        raise ValueError("Bio must be at most 150 characters.")
    return bio


def validate_lang(lang: str) -> str:
    """
    Validate the language.
    1. Return default  'en' if language is none or empty.
    2. Set the default language to 'en' if the language is invalid.
    Raise a ValidationError if the language is invalid.
    """

    if not lang:
        return "en"

    if lang not in LANGUAGES:
        raise ValueError(f"Language must be one of the following: {LANGUAGES}.")
    return lang


def validate_recover_email_code(code: str) -> str:
    """
    Validate the recover email code.
    1. Check if the code is provided.
    2. Check if the code length is 12.
    3. Check if the code is alphanumeric.
    Raise a ValidationError if the code is invalid.
    """

    if not code:
        raise ValueError("The recover_email_code is required.")
    if len(code) != 12:
        raise ValueError("The code is invalid.")
    if not code.isalnum():
        raise ValueError(
            "The code format is invalid. The code must be include lowercase, uppercase letters and numbers."
        )
    return code
