"""Tests for Pydantic models."""

import pytest
from datetime import datetime
from nexusai.models import (
    Task,
    Image,
    TextResponse,
    Usage,
    Message,
    FileMetadata,
    KnowledgeBase,
)


def test_usage_model():
    """Test Usage model."""
    usage = Usage(
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30
    )
    assert usage.prompt_tokens == 10
    assert usage.completion_tokens == 20
    assert usage.total_tokens == 30


def test_text_response_model():
    """Test TextResponse model."""
    response = TextResponse(
        text="Hello world",
        usage=Usage(prompt_tokens=5, completion_tokens=10, total_tokens=15)
    )
    assert response.text == "Hello world"
    assert response.usage.total_tokens == 15


def test_image_model():
    """Test Image model."""
    image = Image(
        image_url="https://example.com/image.png",
        width=1024,
        height=1024
    )
    assert image.image_url == "https://example.com/image.png"
    assert image.width == 1024
    assert image.height == 1024


def test_task_model():
    """Test Task model."""
    task = Task(
        task_id="task_123",
        status="pending",
        task_type="text_generation"
    )
    assert task.task_id == "task_123"
    assert task.status == "pending"
    assert task.task_type == "text_generation"


def test_message_model():
    """Test Message model."""
    message = Message(
        role="user",
        content="Hello"
    )
    assert message.role == "user"
    assert message.content == "Hello"


def test_file_metadata_model():
    """Test FileMetadata model."""
    file_meta = FileMetadata(
        file_id="file_123",
        filename="test.txt",
        size=1024,
        mime_type="text/plain",
        created_at="2025-01-03T10:00:00Z"
    )
    assert file_meta.file_id == "file_123"
    assert file_meta.filename == "test.txt"
    assert file_meta.size == 1024


def test_knowledge_base_model():
    """Test KnowledgeBase model."""
    kb = KnowledgeBase(
        kb_id="kb_123",
        name="Test KB",
        description="A test knowledge base",
        created_at="2025-01-03T10:00:00Z"
    )
    assert kb.kb_id == "kb_123"
    assert kb.name == "Test KB"
    assert kb.description == "A test knowledge base"
