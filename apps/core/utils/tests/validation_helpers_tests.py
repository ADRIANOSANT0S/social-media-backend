import pytest
from rest_framework import serializers

from ..validation_helpers import run_validation


def validate_positive_number(n: int) -> str | int:
    if n < 0:
        raise ValueError("The number must be positive.")
    return n


def test_run_validation_success():
    result = run_validation(validate_positive_number, 7)

    assert result == 7


def test_run_validation_failure():
    with pytest.raises(serializers.ValidationError) as except_info:
        run_validation(validate_positive_number, -1)

    assert except_info.value.detail[0] == "The number must be positive."
