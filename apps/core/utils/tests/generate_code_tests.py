import pytest

from ..generate_code import generate_code


class TestGenerateCode:
    """Tests for generate_code"""

    def test_default_length(self):
        """Check that generate_code returns a code with default length (12)."""
        code = generate_code()
        assert len(code) == 12
        assert code.isalnum()

    def test_length_10(self):
        """Check that generate_code returns a code with the specified length."""
        code = generate_code(10)
        assert len(code) == 10

    def test_code_is_alphanumeric(self):
        """Check that the generated code contains only alphanumeric characters."""
        code = generate_code()
        assert code.isalnum()

    def test_invalid_param(self):
        """Check that generate_code raises TypeError with invalid parameter."""
        with pytest.raises(TypeError):
            generate_code("invalid_param")  # type: ignore[arg-type]
