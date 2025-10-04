"""Tests for file operations resource."""

import pytest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from nexusai import NexusAIClient
from nexusai.models import FileMetadata


def test_files_upload_from_path(mock_client, mock_file_response):
    """Test uploading a file from path."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_file_response

    with patch("builtins.open", mock_open(read_data=b"test content")):
        with patch.object(mock_client._internal_client.client, 'post', return_value=mock_response):
            file_meta = mock_client.files.upload("test.txt")

            assert isinstance(file_meta, FileMetadata)
            assert file_meta.file_id == "file_abc123"
            assert file_meta.filename == "test.txt"


def test_files_get(mock_client, mock_file_response):
    """Test getting file metadata."""
    with patch.object(mock_client._internal_client, 'request', return_value=mock_file_response):
        file_meta = mock_client.files.get("file_abc123")

        assert isinstance(file_meta, FileMetadata)
        assert file_meta.file_id == "file_abc123"


def test_files_delete(mock_client):
    """Test deleting a file."""
    with patch.object(mock_client._internal_client, 'request', return_value={"success": True}):
        result = mock_client.files.delete("file_abc123")

        assert result["success"] is True


def test_files_list(mock_client, mock_file_response):
    """Test listing files."""
    list_response = [mock_file_response, mock_file_response]

    with patch.object(mock_client._internal_client, 'request', return_value=list_response):
        files = mock_client.files.list()

        assert isinstance(files, list)
        assert len(files) == 2
        assert all(isinstance(f, FileMetadata) for f in files)
