"""Tests for session management resource."""

import pytest
from unittest.mock import patch
from nexusai import NexusAIClient
from nexusai.models import SessionResponse, Message
from nexusai.resources.sessions import Session


def test_sessions_create(mock_client, mock_session_response):
    """Test session creation."""
    with patch.object(mock_client._internal_client, 'request', return_value=mock_session_response):
        session = mock_client.sessions.create(
            name="Test Session",
            agent_config={"temperature": 0.7}
        )

        assert isinstance(session, Session)
        assert session.id == "sess_789"
        assert session.name == "Test Session"


def test_session_invoke(mock_client, mock_session_response):
    """Test invoking a session."""
    invoke_response = {
        "response": {
            "role": "assistant",
            "content": "Hello! How can I help?",
        },
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }

    with patch.object(mock_client._internal_client, 'request', side_effect=[mock_session_response, invoke_response]):
        session = mock_client.sessions.create(name="Test")
        response = session.invoke("Hi")

        assert isinstance(response, SessionResponse)
        assert isinstance(response.response, Message)
        assert response.response.role == "assistant"
        assert "help" in response.response.content.lower()


def test_session_history(mock_client, mock_session_response):
    """Test getting session history."""
    history_response = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]

    with patch.object(mock_client._internal_client, 'request', side_effect=[mock_session_response, history_response]):
        session = mock_client.sessions.create(name="Test")
        history = session.history()

        assert isinstance(history, list)
        assert len(history) == 2
        assert all(isinstance(msg, Message) for msg in history)


def test_session_stream(mock_client, mock_session_response):
    """Test streaming session responses."""
    mock_chunks = [
        {"delta": {"content": "Hello"}},
        {"delta": {"content": " there"}},
    ]

    with patch.object(mock_client._internal_client, 'request', return_value=mock_session_response):
        with patch.object(mock_client._internal_client, 'stream', return_value=iter(mock_chunks)):
            session = mock_client.sessions.create(name="Test")
            chunks = list(session.stream("Hi"))

            assert len(chunks) == 2


def test_session_delete(mock_client, mock_session_response):
    """Test deleting a session."""
    with patch.object(mock_client._internal_client, 'request', return_value=mock_session_response):
        with patch.object(mock_client._internal_client, 'request', return_value={"success": True}) as mock_delete:
            session = mock_client.sessions.create(name="Test")
            session.delete()

            # Verify delete was called with correct endpoint
            delete_call = [call for call in mock_delete.call_args_list if "/sessions/" in str(call)]
            assert len(delete_call) > 0
