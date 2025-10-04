"""
Nexus AI Python SDK

A Python client library for the Nexus AI platform.
"""

from nexusai.__version__ import __version__
from nexusai.client import NexusAIClient
from nexusai.config import config
from nexusai import error

__all__ = [
    "__version__",
    "NexusAIClient",
    "config",
    "error",
]
