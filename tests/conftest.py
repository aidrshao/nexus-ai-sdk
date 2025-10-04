"""Pytest configuration and shared fixtures."""

import pytest
from unittest.mock import Mock
from nexusai import NexusAIClient


@pytest.fixture
def mock_client():
    """Create a NexusAIClient with mocked HTTP client."""
    client = NexusAIClient(
        api_key="test_key_123",
        base_url="http://localhost:8000/api/v1"
    )
    return client


@pytest.fixture
def mock_text_response():
    """Mock response for text generation."""
    return {
        "task_id": "task_123",
        "status": "completed",
        "output": {
            "text": "你好！我是 Nexus AI 助手，很高兴为您服务。",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 35,
                "total_tokens": 40
            }
        }
    }


@pytest.fixture
def mock_image_response():
    """Mock response for image generation."""
    return {
        "task_id": "img_task_456",
        "status": "completed",
        "output": {
            "image_url": "https://example.com/generated_image.png",
            "width": 1024,
            "height": 1024
        }
    }


@pytest.fixture
def mock_session_response():
    """Mock response for session creation."""
    return {
        "session_id": "sess_789",
        "name": "Test Session",
        "agent_config": {
            "temperature": 0.7
        },
        "created_at": "2025-01-03T10:00:00Z"
    }


@pytest.fixture
def mock_file_response():
    """Mock response for file upload."""
    return {
        "file_id": "file_abc123",
        "filename": "test.txt",
        "size": 1024,
        "mime_type": "text/plain",
        "created_at": "2025-01-03T10:00:00Z"
    }


@pytest.fixture
def mock_kb_response():
    """Mock response for knowledge base creation."""
    return {
        "kb_id": "kb_xyz789",
        "name": "Test KB",
        "description": "Test knowledge base",
        "created_at": "2025-01-03T10:00:00Z"
    }
