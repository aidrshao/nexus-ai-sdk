"""Text generation resource module."""

from typing import Optional, Iterator, Dict, Any
from nexusai.models import TextResponse, Task, Usage
from nexusai._internal._poller import TaskPoller
from nexusai.constants import TASK_TYPE_TEXT_GENERATION


class TextResource:
    """
    Text generation resource.

    Provides methods for generating text using language models.
    Supports synchronous, asynchronous, and streaming modes.
    """

    def __init__(self, client):
        """
        Initialize text resource.

        Args:
            client: InternalClient instance
        """
        self._client = client
        self._poller = TaskPoller(client)

    def generate(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> TextResponse:
        """
        Generate text synchronously.

        Args:
            prompt: Input prompt for text generation
            provider: AI service provider (e.g., "openai", "dmxapi", "anthropic").
                     If not specified, uses default provider.
            model: Model name (e.g., "gpt-4", "gpt-4o-mini").
                  If not specified, uses default model.
            temperature: Sampling temperature (0.0 to 2.0). Higher values make
                        output more random. Default: 0.7
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional model configuration parameters

        Returns:
            TextResponse object containing generated text and metadata

        Raises:
            InvalidRequestError: If request parameters are invalid
            APIError: If generation fails

        Example:
            ```python
            from nexusai import NexusAIClient

            client = NexusAIClient()

            # Simple mode (省心模式)
            response = client.text.generate("写一首关于春天的诗")
            print(response.text)

            # Expert mode (专家模式)
            response = client.text.generate(
                prompt="Explain quantum computing in simple terms",
                provider="openai",
                model="gpt-4",
                temperature=0.5,
                max_tokens=500
            )
            print(response.text)
            print(f"Tokens used: {response.usage.total_tokens}")
            ```
        """
        # Build request body
        request_body = {
            "task_type": TASK_TYPE_TEXT_GENERATION,
            "input": {"prompt": prompt},
        }

        # Add optional provider and model
        if provider:
            request_body["provider"] = provider
        if model:
            request_body["model"] = model

        # Build configuration
        config_params = {"temperature": temperature, **kwargs}
        if max_tokens:
            config_params["max_tokens"] = max_tokens
        request_body["config"] = config_params

        # Make synchronous request (no stream, no async)
        response = self._client.request("POST", "/invoke", json_data=request_body)

        # Parse response
        output = response.get("output", {})
        usage_data = output.get("usage")

        return TextResponse(
            text=output.get("text", ""),
            usage=Usage(**usage_data) if usage_data else None,
            model=output.get("model"),
            finish_reason=output.get("finish_reason"),
        )

    def generate_async(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> TextResponse:
        """
        Generate text asynchronously (with task polling).

        Similar to generate() but uses async task pattern with polling.
        Useful for long-running text generation tasks.

        Args:
            prompt: Input prompt for text generation
            provider: AI service provider
            model: Model name
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional model configuration parameters

        Returns:
            TextResponse object containing generated text and metadata

        Raises:
            InvalidRequestError: If request parameters are invalid
            APITimeoutError: If generation times out
            APIError: If generation fails

        Example:
            ```python
            response = client.text.generate_async(
                prompt="Write a long article about AI",
                max_tokens=2000
            )
            print(response.text)
            ```
        """
        # Build request body (same as generate)
        request_body = {
            "task_type": TASK_TYPE_TEXT_GENERATION,
            "input": {"prompt": prompt},
        }

        if provider:
            request_body["provider"] = provider
        if model:
            request_body["model"] = model

        config_params = {"temperature": temperature, **kwargs}
        if max_tokens:
            config_params["max_tokens"] = max_tokens
        request_body["config"] = config_params

        # Submit async task
        response = self._client.request(
            "POST",
            "/invoke",
            json_data=request_body,
            headers={"Prefer": "respond-async"},
        )

        # Parse task and poll
        task = Task(**response)
        result = self._poller.poll(task.task_id)

        # Parse final result
        output = result.get("output", {})
        usage_data = output.get("usage")

        return TextResponse(
            text=output.get("text", ""),
            usage=Usage(**usage_data) if usage_data else None,
            model=output.get("model"),
            finish_reason=output.get("finish_reason"),
        )

    def stream(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Iterator[Dict[str, Any]]:
        """
        Generate text with streaming response (Server-Sent Events).

        Yields chunks of text as they are generated, allowing for real-time
        display of generation progress.

        Args:
            prompt: Input prompt for text generation
            provider: AI service provider
            model: Model name
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional model configuration parameters

        Yields:
            Dictionary chunks with generation data. Each chunk typically contains:
            - delta: {"content": "text chunk"}
            - usage: token usage information (final chunk only)

        Raises:
            InvalidRequestError: If request parameters are invalid
            APIError: If generation fails

        Example:
            ```python
            from nexusai import NexusAIClient

            client = NexusAIClient()

            # Stream text generation
            for chunk in client.text.stream("Tell me a story"):
                if "delta" in chunk:
                    print(chunk["delta"].get("content", ""), end="", flush=True)
            print()  # New line after streaming completes
            ```
        """
        # Build request body
        request_body = {
            "task_type": TASK_TYPE_TEXT_GENERATION,
            "input": {"prompt": prompt},
            "stream": True,  # Enable streaming
        }

        if provider:
            request_body["provider"] = provider
        if model:
            request_body["model"] = model

        config_params = {"temperature": temperature, **kwargs}
        if max_tokens:
            config_params["max_tokens"] = max_tokens
        request_body["config"] = config_params

        # Stream response
        for chunk in self._client.stream("POST", "/invoke", json_data=request_body):
            yield chunk
