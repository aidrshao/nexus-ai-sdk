"""Tests for image generation resource."""

import pytest
from unittest.mock import patch
from nexusai import NexusAIClient
from nexusai.models import Image, Task


def test_images_generate_simple(mock_client, mock_image_response):
    """Test simple image generation."""
    with patch.object(mock_client._internal_client, 'request', return_value=mock_image_response):
        with patch.object(mock_client.images._poller, 'poll', return_value=mock_image_response):
            image = mock_client.images.generate(prompt="A sunset")

            assert isinstance(image, Image)
            assert image.image_url is not None
            assert image.width == 1024
            assert image.height == 1024


def test_images_generate_with_params(mock_client, mock_image_response):
    """Test image generation with parameters."""
    with patch.object(mock_client._internal_client, 'request', return_value=mock_image_response) as mock_request:
        with patch.object(mock_client.images._poller, 'poll', return_value=mock_image_response):
            image = mock_client.images.generate(
                prompt="Digital art",
                provider="dmxapi",
                model="gemini-2.5-flash-image",
                size="1920x1080",
                quality="hd"
            )

            assert isinstance(image, Image)
            # Verify request parameters
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            request_body = call_args[1]['json_data']
            assert request_body['provider'] == "dmxapi"
            assert request_body['model'] == "gemini-2.5-flash-image"


def test_images_generate_task_polling(mock_client):
    """Test that image generation uses task polling."""
    task_response = {
        "task_id": "img_task_123",
        "status": "pending",
    }
    completed_response = {
        "task_id": "img_task_123",
        "status": "completed",
        "output": {
            "image_url": "https://example.com/image.png",
            "width": 512,
            "height": 512
        }
    }

    with patch.object(mock_client._internal_client, 'request', return_value=task_response):
        with patch.object(mock_client.images._poller, 'poll', return_value=completed_response):
            image = mock_client.images.generate(prompt="Test")

            assert isinstance(image, Image)
            # Verify poller was called
            mock_client.images._poller.poll.assert_called_once()
