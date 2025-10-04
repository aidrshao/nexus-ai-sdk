"""Exception classes for Nexus AI SDK."""

from typing import Optional, Dict, Any


class APIError(Exception):
    """
    Base exception for all SDK errors.

    All Nexus AI SDK exceptions inherit from this class.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        response_body: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize an API error.

        Args:
            message: Human-readable error message
            status_code: HTTP status code (if applicable)
            error_code: Error code from API response
            response_body: Full response body from the API
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.response_body = response_body

    def __str__(self) -> str:
        """Return a string representation of the error."""
        parts = [self.message]
        if self.status_code:
            parts.append(f"(HTTP {self.status_code})")
        if self.error_code:
            parts.append(f"[{self.error_code}]")
        return " ".join(parts)

    def __repr__(self) -> str:
        """Return a detailed string representation of the error."""
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"status_code={self.status_code}, "
            f"error_code={self.error_code!r})"
        )


class AuthenticationError(APIError):
    """
    Authentication failed (HTTP 401).

    Raised when the API key is missing, invalid, or expired.
    """

    pass


class PermissionError(APIError):
    """
    Permission denied (HTTP 403).

    Raised when the API key doesn't have permission to perform the requested action.
    """

    pass


class NotFoundError(APIError):
    """
    Resource not found (HTTP 404).

    Raised when the requested resource doesn't exist.
    """

    pass


class RateLimitError(APIError):
    """
    Rate limit exceeded (HTTP 429).

    Raised when too many requests have been made in a given time period.
    """

    def __init__(
        self,
        message: str,
        retry_after: Optional[int] = None,
        **kwargs,
    ):
        """
        Initialize a rate limit error.

        Args:
            message: Human-readable error message
            retry_after: Number of seconds to wait before retrying
            **kwargs: Additional arguments passed to APIError
        """
        super().__init__(message, **kwargs)
        self.retry_after = retry_after

    def __str__(self) -> str:
        """Return a string representation of the error."""
        base = super().__str__()
        if self.retry_after:
            return f"{base} (retry after {self.retry_after}s)"
        return base


class APITimeoutError(APIError):
    """
    Request or polling timed out.

    Raised when a request takes longer than the configured timeout,
    or when task polling exceeds the maximum wait time.
    """

    pass


class InvalidRequestError(APIError):
    """
    Invalid request parameters (HTTP 400).

    Raised when the request is malformed or contains invalid parameters.
    """

    pass


class ServerError(APIError):
    """
    Server-side error (HTTP 5xx).

    Raised when the server encounters an internal error.
    """

    pass


class ValidationError(APIError):
    """
    Data validation error.

    Raised when response data fails validation against expected schema.
    """

    pass


class NetworkError(APIError):
    """
    Network communication error.

    Raised when a network error occurs during the request.
    """

    pass
