"""Tests for configuration management."""

import os
import pytest
from nexusai.config import config


def test_config_singleton():
    """Test config is a singleton."""
    from nexusai.config import config as config2
    assert config is config2


def test_config_default_values():
    """Test config has expected default values."""
    # Base URL should default to localhost
    assert "localhost:8000" in config.base_url
    assert config.timeout == 30.0
    assert config.max_retries == 3
    assert config.poll_interval == 2.0
    assert config.poll_timeout == 300.0


def test_config_get_api_key():
    """Test getting API key."""
    # Set test key
    original = config._api_key
    config._api_key = "test_key_123"

    assert config.get_api_key() == "test_key_123"

    # Restore
    config._api_key = original


def test_config_get_api_key_missing():
    """Test error when API key is missing."""
    original = config._api_key
    config._api_key = None

    with pytest.raises(ValueError, match="API key is required"):
        config.get_api_key()

    # Restore
    config._api_key = original
