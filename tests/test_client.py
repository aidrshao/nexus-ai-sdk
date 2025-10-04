"""Tests for NexusAIClient initialization and configuration."""

import pytest
from nexusai import NexusAIClient
from nexusai.error import AuthenticationError


def test_client_initialization():
    """Test client can be initialized with parameters."""
    client = NexusAIClient(
        api_key="test_key",
        base_url="http://localhost:8000/api/v1"
    )
    assert client is not None
    assert client._internal_client.api_key == "test_key"
    assert client._internal_client.base_url == "http://localhost:8000/api/v1"


def test_client_default_base_url():
    """Test client uses localhost by default."""
    client = NexusAIClient(api_key="test_key")
    assert "localhost:8000" in client._internal_client.base_url


def test_client_lazy_loading():
    """Test resources are lazy-loaded."""
    client = NexusAIClient(api_key="test_key")

    # Resources should be None initially
    assert client._images_resource is None
    assert client._text_resource is None
    assert client._sessions_resource is None

    # Accessing should trigger loading
    _ = client.images
    assert client._images_resource is not None


def test_client_context_manager():
    """Test client works as context manager."""
    with NexusAIClient(api_key="test_key") as client:
        assert client is not None
    # Client should be closed after exiting context


def test_client_close():
    """Test client can be closed."""
    client = NexusAIClient(api_key="test_key")
    client.close()
    # Should not raise any errors
