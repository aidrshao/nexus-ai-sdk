"""Internal HTTP client for API communication."""

import httpx
import json
from typing import Dict, Any, Optional, Iterator
from nexusai.__version__ import __version__
from nexusai.error import (
    APIError,
    AuthenticationError,
    PermissionError,
    NotFoundError,
    RateLimitError,
    APITimeoutError,
    InvalidRequestError,
    ServerError,
    NetworkError,
)
from nexusai.config import config


class InternalClient:
    """
    Internal HTTP client for all API interactions.

    This class handles:
    - HTTP request/response lifecycle
    - Authentication headers
    - Error handling and retries
    - Streaming responses
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ):
        """
        Initialize the internal HTTP client.

        Args:
            api_key: API key for authentication (overrides config)
            base_url: Base URL for API (overrides config)
            timeout: Request timeout in seconds (overrides config)
            max_retries: Maximum number of retries (overrides config)

        Raises:
            AuthenticationError: If API key is not provided
        """
        self.api_key = api_key or config.api_key
        self.base_url = base_url or config.base_url
        self.timeout = timeout if timeout is not None else config.timeout
        self.max_retries = max_retries if max_retries is not None else config.max_retries

        if not self.api_key:
            raise AuthenticationError(
                "API key is required. Set NEXUS_API_KEY environment variable or pass api_key parameter."
            )

        # Create httpx client with retry transport
        transport = httpx.HTTPTransport(retries=self.max_retries)
        self.client = httpx.Client(
            timeout=self.timeout,
            headers=self._default_headers(),
            transport=transport,
        )

    def _default_headers(self) -> Dict[str, str]:
        """Generate default request headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"nexus-ai-python/{__version__}",
        }

    def request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Make a synchronous HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (e.g., "/invoke")
            json_data: JSON request body
            headers: Additional headers to merge with defaults
            params: URL query parameters
            **kwargs: Additional arguments passed to httpx

        Returns:
            Response data as dictionary

        Raises:
            APIError: For various API errors
            APITimeoutError: If request times out
            NetworkError: If network error occurs
        """
        url = f"{self.base_url}{endpoint}"

        # Merge headers
        request_headers = self._default_headers()
        if headers:
            request_headers.update(headers)

        try:
            response = self.client.request(
                method=method,
                url=url,
                json=json_data,
                headers=request_headers,
                params=params,
                **kwargs,
            )
            return self._handle_response(response)

        except httpx.TimeoutException as e:
            raise APITimeoutError(f"Request timed out after {self.timeout}s") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {str(e)}") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {str(e)}") from e

    def stream(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Iterator[Dict[str, Any]]:
        """
        Make a streaming HTTP request (Server-Sent Events).

        Args:
            method: HTTP method
            endpoint: API endpoint path
            json_data: JSON request body
            headers: Additional headers
            **kwargs: Additional arguments passed to httpx

        Yields:
            Parsed JSON chunks from SSE stream

        Raises:
            APIError: For various API errors
        """
        url = f"{self.base_url}{endpoint}"

        # Merge headers
        request_headers = self._default_headers()
        if headers:
            request_headers.update(headers)

        try:
            with self.client.stream(
                method=method,
                url=url,
                json=json_data,
                headers=request_headers,
                **kwargs,
            ) as response:
                # Check response status before streaming
                self._check_response_status(response)

                # Parse SSE stream
                for line in response.iter_lines():
                    line = line.strip()
                    if not line:
                        continue

                    # SSE format: "data: <json>"
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix

                        # Check for stream end marker
                        if data == "[DONE]":
                            break

                        try:
                            yield json.loads(data)
                        except json.JSONDecodeError:
                            # Skip invalid JSON lines
                            continue

        except httpx.TimeoutException as e:
            raise APITimeoutError(f"Stream timed out after {self.timeout}s") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error during streaming: {str(e)}") from e

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """
        Handle HTTP response and parse JSON.

        Args:
            response: HTTP response object

        Returns:
            Parsed JSON response

        Raises:
            APIError: If response indicates an error
        """
        self._check_response_status(response)

        try:
            return response.json()
        except json.JSONDecodeError:
            # If response is not JSON, wrap text in dict
            return {"content": response.text}

    def _check_response_status(self, response: httpx.Response) -> None:
        """
        Check response status code and raise appropriate exceptions.

        Args:
            response: HTTP response object

        Raises:
            AuthenticationError: For 401 status
            PermissionError: For 403 status
            NotFoundError: For 404 status
            RateLimitError: For 429 status
            InvalidRequestError: For 400 status
            ServerError: For 5xx status
            APIError: For other error status codes
        """
        if response.status_code < 400:
            return

        # Try to parse error response
        try:
            error_data = response.json()
            message = error_data.get("detail", response.text)
            error_code = error_data.get("error_code")
        except (json.JSONDecodeError, AttributeError):
            message = response.text or f"HTTP {response.status_code}"
            error_code = None
            error_data = None

        status_code = response.status_code

        # Map status codes to specific exceptions
        if status_code == 401:
            raise AuthenticationError(message, status_code, error_code, error_data)
        elif status_code == 403:
            raise PermissionError(message, status_code, error_code, error_data)
        elif status_code == 404:
            raise NotFoundError(message, status_code, error_code, error_data)
        elif status_code == 429:
            retry_after = response.headers.get("X-RateLimit-Reset")
            raise RateLimitError(
                message,
                retry_after=int(retry_after) if retry_after else None,
                status_code=status_code,
                error_code=error_code,
                response_body=error_data,
            )
        elif status_code == 400:
            raise InvalidRequestError(message, status_code, error_code, error_data)
        elif status_code >= 500:
            raise ServerError(message, status_code, error_code, error_data)
        else:
            raise APIError(message, status_code, error_code, error_data)

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, *args):
        """Context manager exit - close client."""
        self.close()
