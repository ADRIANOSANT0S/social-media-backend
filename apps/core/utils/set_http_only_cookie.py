def set_http_only_cookie(response, key, value, expires, **kwargs) -> None:
    """
    Sets an HTTP-only cookie on the given HttpResponse.

    Args:
        response (HttpResponse): The Django HttpResponse object.
        key (str): The name of the cookie.
        value (Any): The value to store in the cookie.
        expires (datetime): The expiration datetime of the cookie.
        **kwargs: Optional cookie parameters such as `path`, `domain`, `max_age`, `secure`, `samesite`.
                  Note: Do not use `expires` and `max_age` together.

    Returns:
        None

    Example:
        expires = datetime.now(timezone.utc) + timedelta(minutes=5)

        set_http_only_cookie(response, "cookie_name", value_of_cookie, expires)
    """
    response.set_cookie(
        key=key,
        value=str(value),
        httponly=True,
        secure=kwargs.pop("secure", True),
        samesite=kwargs.pop("samesite", "Lax"),
        expires=expires,
        **kwargs,
    )
