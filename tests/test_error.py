"""Tests for error handling and exception types."""

import pytest
from nexusai.error import (
    APIError,
    AuthenticationError,
    PermissionError,
    NotFoundError,
    RateLimitError,
    InvalidRequestError,
    ServerError,
    APITimeoutError,
    NetworkError,
)


def test_api_error_basic():
    """Test basic APIError."""
    error = APIError("Test error", status_code=500)
    assert str(error) == "Test error"
    assert error.status_code == 500


def test_authentication_error():
    """Test AuthenticationError."""
    error = AuthenticationError("Invalid API key")
    assert "Invalid API key" in str(error)
    assert isinstance(error, APIError)


def test_rate_limit_error():
    """Test RateLimitError with retry_after."""
    error = RateLimitError("Rate limited", retry_after=60)
    assert error.retry_after == 60
    assert isinstance(error, APIError)


def test_not_found_error():
    """Test NotFoundError."""
    error = NotFoundError("Resource not found")
    assert "not found" in str(error).lower()
    assert isinstance(error, APIError)


def test_timeout_error():
    """Test APITimeoutError."""
    error = APITimeoutError("Request timed out")
    assert "timed out" in str(error).lower()
    assert isinstance(error, APIError)


def test_network_error():
    """Test NetworkError."""
    error = NetworkError("Connection failed")
    assert "Connection failed" in str(error)
    assert isinstance(error, APIError)


def test_server_error():
    """Test ServerError."""
    error = ServerError("Internal server error", status_code=500)
    assert error.status_code == 500
    assert isinstance(error, APIError)


def test_invalid_request_error():
    """Test InvalidRequestError."""
    error = InvalidRequestError("Invalid parameter")
    assert "Invalid parameter" in str(error)
    assert isinstance(error, APIError)


def test_permission_error():
    """Test PermissionError."""
    error = PermissionError("Access denied")
    assert "Access denied" in str(error)
    assert isinstance(error, APIError)
