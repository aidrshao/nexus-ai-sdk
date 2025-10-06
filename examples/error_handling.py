"""
Comprehensive error handling examples for Nexus AI SDK.

This file demonstrates best practices for handling various errors
that may occur when using the SDK.
"""

from nexusai import NexusAIClient
from nexusai.error import (
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    APITimeoutError,
    NetworkError,
    ServerError,
    NotFoundError,
    StreamError,
)
from nexusai._internal._retry import RetryConfig, RetryableRequest
import time


def example_1_basic_error_handling():
    """Example 1: Basic error handling with try-except."""
    print("\n=== Example 1: Basic Error Handling ===")

    client = NexusAIClient(api_key="nxs_test_key")

    try:
        response = client.text.generate(
            prompt="Hello, world!",
            max_tokens=100,
        )
        print(f"Success: {response.text}")

    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        print("Please check your API key")

    except ValidationError as e:
        print(f"Validation error: {e}")
        if e.validation_errors:
            print("Field errors:")
            for err in e.validation_errors:
                field = ".".join(str(loc) for loc in err.get("loc", []))
                msg = err.get("msg", "")
                print(f"  - {field}: {msg}")

    except APITimeoutError as e:
        print(f"Request timed out: {e}")
        print("Try increasing the timeout or check your network")

    except APIError as e:
        print(f"API error occurred: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Error code: {e.error_code}")


def example_2_validation_error_handling():
    """Example 2: Handling validation errors (HTTP 422)."""
    print("\n=== Example 2: Validation Error Handling ===")

    client = NexusAIClient(api_key="nxs_test_key")

    try:
        # This may fail if system_prompt is required
        session = client.sessions.create(
            name="Test Session",
            agent_config={
                "temperature": 0.7,
                # Missing system_prompt - may cause ValidationError
            },
        )
        print(f"Session created: {session.session_id}")

    except ValidationError as e:
        print(f"Validation error: {e}")

        # Check if it's the system_prompt error
        if e.validation_errors:
            for err in e.validation_errors:
                field_path = err.get("loc", [])
                if "system_prompt" in str(field_path):
                    print("\nFix: Add system_prompt to agent_config")
                    print("Retrying with system_prompt...")

                    # Retry with fix
                    session = client.sessions.create(
                        name="Test Session",
                        agent_config={
                            "temperature": 0.7,
                            "system_prompt": "You are a helpful assistant.",
                        },
                    )
                    print(f"Success! Session created: {session.session_id}")
                    break


def example_3_rate_limit_handling():
    """Example 3: Handling rate limits with exponential backoff."""
    print("\n=== Example 3: Rate Limit Handling ===")

    client = NexusAIClient(api_key="nxs_test_key")

    max_retries = 3
    base_delay = 1.0

    for attempt in range(max_retries + 1):
        try:
            response = client.text.generate(
                prompt="Hello!",
                max_tokens=50,
            )
            print(f"Success: {response.text}")
            break

        except RateLimitError as e:
            if attempt >= max_retries:
                print(f"Rate limit exceeded after {max_retries} retries")
                raise

            # Use retry_after from response if available
            wait_time = e.retry_after if e.retry_after else base_delay * (2**attempt)
            print(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
            time.sleep(wait_time)


def example_4_network_error_retry():
    """Example 4: Retrying network errors."""
    print("\n=== Example 4: Network Error Retry ===")

    client = NexusAIClient(api_key="nxs_test_key")

    max_retries = 3

    for attempt in range(max_retries + 1):
        try:
            response = client.text.generate(
                prompt="Hello!",
                max_tokens=50,
            )
            print(f"Success: {response.text}")
            break

        except NetworkError as e:
            if not e.is_retryable or attempt >= max_retries:
                print(f"Network error (not retryable or max retries exceeded): {e}")
                raise

            delay = 2**attempt  # Exponential backoff: 1s, 2s, 4s
            print(f"Network error. Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)

        except ServerError as e:
            if attempt >= max_retries:
                print(f"Server error after {max_retries} retries: {e}")
                raise

            delay = 2**attempt
            print(f"Server error. Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)


def example_5_streaming_error_handling():
    """Example 5: Handling streaming errors."""
    print("\n=== Example 5: Streaming Error Handling ===")

    client = NexusAIClient(api_key="nxs_test_key")

    try:
        print("Starting stream...")
        for chunk in client.text.generate_stream(
            prompt="Tell me a story",
            max_tokens=200,
        ):
            print(chunk.delta.get("content", ""), end="", flush=True)
        print("\n")

    except StreamError as e:
        print(f"\nStream error: {e}")
        if "No data received" in str(e):
            print("The server may not support SSE streaming.")
            print("Try using non-streaming mode: client.text.generate()")

    except APITimeoutError as e:
        print(f"\nStream timed out: {e}")
        print("Try increasing timeout: NexusAIClient(timeout=120)")

    except NetworkError as e:
        print(f"\nNetwork error during streaming: {e}")


def example_6_context_manager():
    """Example 6: Using context manager for automatic cleanup."""
    print("\n=== Example 6: Context Manager ===")

    try:
        with NexusAIClient(api_key="nxs_test_key") as client:
            response = client.text.generate(
                prompt="Hello!",
                max_tokens=50,
            )
            print(f"Success: {response.text}")

    except APIError as e:
        print(f"Error: {e}")

    # Client is automatically closed when exiting the context


def example_7_retryable_request():
    """Example 7: Using RetryableRequest for advanced retry logic."""
    print("\n=== Example 7: Advanced Retry with RetryableRequest ===")

    client = NexusAIClient(api_key="nxs_test_key")

    # Custom retry configuration
    retry_config = RetryConfig(
        max_retries=5,
        initial_delay=1.0,
        max_delay=30.0,
        exponential_base=2.0,
        jitter=0.1,
    )

    try:
        with RetryableRequest(retry_config=retry_config) as retry:
            response = retry.execute(
                lambda: client.text.generate(
                    prompt="Hello!",
                    max_tokens=50,
                )
            )
            print(f"Success after {retry.attempt} attempts: {response.text}")

    except APIError as e:
        print(f"Failed after all retries: {e}")


def example_8_comprehensive_error_handling():
    """Example 8: Comprehensive error handling for production."""
    print("\n=== Example 8: Production-Ready Error Handling ===")

    def generate_text_with_retry(prompt: str, max_tokens: int = 100):
        """Generate text with comprehensive error handling."""
        client = NexusAIClient(api_key="nxs_test_key")
        max_retries = 3

        for attempt in range(max_retries + 1):
            try:
                response = client.text.generate(
                    prompt=prompt,
                    max_tokens=max_tokens,
                )
                return response.text

            except AuthenticationError as e:
                # Don't retry authentication errors
                print(f"Authentication error: {e}")
                raise

            except ValidationError as e:
                # Don't retry validation errors - fix the input
                print(f"Validation error: {e}")
                if e.validation_errors:
                    print("Please fix the following fields:")
                    for err in e.validation_errors:
                        field = ".".join(str(loc) for loc in err.get("loc", []))
                        msg = err.get("msg", "")
                        print(f"  - {field}: {msg}")
                raise

            except NotFoundError as e:
                # Don't retry 404 errors
                print(f"Resource not found: {e}")
                raise

            except RateLimitError as e:
                if attempt >= max_retries:
                    raise
                wait_time = e.retry_after or (2**attempt)
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)

            except (NetworkError, ServerError, APITimeoutError) as e:
                # Retry transient errors
                if attempt >= max_retries:
                    print(f"Failed after {max_retries} retries: {e}")
                    raise

                delay = 2**attempt
                print(f"Transient error. Retrying in {delay}s... ({attempt + 1}/{max_retries})")
                time.sleep(delay)

            except APIError as e:
                # Catch-all for other API errors
                print(f"API error: {e} (status: {e.status_code})")
                raise

        raise APIError("Max retries exceeded")

    # Usage
    try:
        result = generate_text_with_retry("Hello, world!")
        print(f"Result: {result}")
    except APIError as e:
        print(f"Final error: {e}")


def example_9_error_inspection():
    """Example 9: Inspecting error details."""
    print("\n=== Example 9: Error Inspection ===")

    client = NexusAIClient(api_key="nxs_test_key")

    try:
        response = client.text.generate(
            prompt="Hello!",
            max_tokens=100,
        )

    except APIError as e:
        print("Error details:")
        print(f"  Message: {e.message}")
        print(f"  Status code: {e.status_code}")
        print(f"  Error code: {e.error_code}")
        print(f"  Response body: {e.response_body}")
        print(f"  String representation: {str(e)}")
        print(f"  Repr: {repr(e)}")

        # Check error type
        if isinstance(e, ValidationError):
            print(f"  Validation errors: {e.validation_errors}")
        elif isinstance(e, RateLimitError):
            print(f"  Retry after: {e.retry_after}s")
        elif isinstance(e, NetworkError):
            print(f"  Is retryable: {e.is_retryable}")


if __name__ == "__main__":
    print("Nexus AI SDK - Error Handling Examples")
    print("=" * 50)

    # Note: These examples will fail without a valid API key and running server
    # They are meant to demonstrate error handling patterns

    examples = [
        example_1_basic_error_handling,
        example_2_validation_error_handling,
        example_3_rate_limit_handling,
        example_4_network_error_retry,
        example_5_streaming_error_handling,
        example_6_context_manager,
        example_7_retryable_request,
        example_8_comprehensive_error_handling,
        example_9_error_inspection,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Example failed (expected): {type(e).__name__}")

    print("\n" + "=" * 50)
    print("Examples completed!")
