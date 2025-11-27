# test_cookies.py
from datetime import datetime, timedelta, timezone

import pytest
from django.http import HttpResponse

from ..set_http_only_cookie import set_http_only_cookie


@pytest.fixture
def response():
    return HttpResponse()


@pytest.fixture
def cookie_data():
    return {
        "key": "access_token",
        "value": "test123",
        "expires": datetime.now(timezone.utc) + timedelta(hours=1),
    }


def test_basic_cookie(response, cookie_data):
    set_http_only_cookie(response, **cookie_data)
    key = cookie_data["key"]

    assert key in response.cookies
    assert response.cookies[key]["httponly"] is True
    assert response.cookies[key]["samesite"].lower() == "lax"
    # Por padrão secure=True
    assert response.cookies[key]["secure"] is True


def test_cookie_with_secure_false(response, cookie_data):
    set_http_only_cookie(response, **cookie_data, secure=False)
    key = cookie_data["key"]
    assert response.cookies[key]["secure"] == ""


def test_cookie_with_samesite(response, cookie_data):
    set_http_only_cookie(response, **cookie_data, samesite="None")
    key = cookie_data["key"]
    assert response.cookies[key]["samesite"] == "None"


def test_cookie_with_domain(response, cookie_data):
    set_http_only_cookie(response, **cookie_data, domain=".localhost")
    key = cookie_data["key"]
    assert response.cookies[key]["domain"] == ".localhost"


def test_cookie_with_additional_params(response, cookie_data):
    set_http_only_cookie(
        response,
        **cookie_data,
        path="/api",
    )
    key = cookie_data["key"]
    assert response.cookies[key]["path"] == "/api"


def test_cookie_expires_set(response, cookie_data):
    set_http_only_cookie(response, **cookie_data)
    key = cookie_data["key"]
    # Comparação aproximada da expiração
    cookie_expires = response.cookies[key]["expires"]
    expected_expires = cookie_data["expires"].strftime("%a, %d %b %Y %H:%M:%S GMT")
    assert cookie_expires == expected_expires
