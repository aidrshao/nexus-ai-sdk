"""Tests for text generation resource."""

import pytest
from unittest.mock import patch, MagicMock
from nexusai import NexusAIClient
from nexusai.models import TextResponse


def test_text_generate_simple(mock_client, mock_text_response):
    """Test simple text generation."""
    with patch.object(mock_client._internal_client, 'request', return_value=mock_text_response):
        response = mock_client.text.generate(prompt="Hello")

        assert isinstance(response, TextResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0
        assert response.usage is not None
        assert response.usage.total_tokens > 0


def test_text_generate_with_params(mock_client, mock_text_response):
    """Test text generation with parameters."""
    with patch.object(mock_client._internal_client, 'request', return_value=mock_text_response) as mock_request:
        response = mock_client.text.generate(
            prompt="Tell me a story",
            provider="openai",
            model="gpt-4",
            temperature=0.7,
            max_tokens=500
        )

        assert isinstance(response, TextResponse)
        # Verify request was made with correct parameters
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        request_body = call_args[1]['json_data']
        assert request_body['input']['prompt'] == "Tell me a story"
        assert request_body['provider'] == "openai"
        assert request_body['model'] == "gpt-4"


def test_text_stream(mock_client):
    """Test streaming text generation."""
    mock_chunks = [
        {"delta": {"content": "Hello"}},
        {"delta": {"content": " world"}},
        {"delta": {"content": "!"}},
    ]

    with patch.object(mock_client._internal_client, 'stream', return_value=iter(mock_chunks)):
        chunks = list(mock_client.text.stream(prompt="Hi"))

        assert len(chunks) == 3
        assert chunks[0]["delta"]["content"] == "Hello"
        assert chunks[1]["delta"]["content"] == " world"
        assert chunks[2]["delta"]["content"] == "!"


def test_text_generate_async(mock_client):
    """Test async text generation (returns task)."""
    mock_task_response = {
        "task_id": "task_async_123",
        "status": "pending",
    }

    with patch.object(mock_client._internal_client, 'request', return_value=mock_task_response):
        from nexusai.models import Task
        task = mock_client.text.generate_async(prompt="Long task")

        assert isinstance(task, Task)
        assert task.task_id == "task_async_123"
        assert task.status == "pending"
