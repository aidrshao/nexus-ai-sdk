# Nexus AI Python SDK

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Official Python SDK for [Nexus AI](https://nexus-ai.juncai-ai.com) - A unified AI capabilities platform.

## Features

- 🚀 **Simple & Intuitive** - Clean API design with sensible defaults
- 🔄 **Async Support** - Built-in task polling for long-running operations
- 📡 **Streaming** - Real-time streaming for text generation
- 💬 **Session Management** - Stateful conversations with automatic context handling
- 🧠 **Knowledge Bases** - RAG capabilities with semantic search
- 🎨 **Multi-Modal** - Text, images, audio (ASR/TTS), and document processing
- 🔐 **Type-Safe** - Full type hints with Pydantic models
- 🌐 **Development Friendly** - Defaults to localhost for easy development

## Installation

```bash
pip install nexus-ai-sdk
```

Or install from source:

```bash
git clone https://github.com/nexus-ai/python-sdk.git
cd python-sdk
poetry install
```

## Quick Start

### 1. Set up your API key

Create a `.env` file in your project root:

```bash
NEXUS_API_KEY=nxs_your_api_key_here
# Optional: Set base URL (defaults to http://localhost:8000/api/v1)
# NEXUS_BASE_URL=https://nexus-ai.juncai-ai.com/api/v1
```

### 2. Initialize the client

```python
from nexusai import NexusAIClient

# Reads configuration from environment variables
client = NexusAIClient()

# Or configure explicitly
client = NexusAIClient(
    api_key="nxs_your_api_key",
    base_url="http://localhost:8000/api/v1"
)
```

### 3. Generate text

```python
# Simple mode (省心模式) - uses default provider and model
response = client.text.generate("写一首关于春天的诗")
print(response.text)

# Expert mode (专家模式) - specify provider and model
response = client.text.generate(
    prompt="Explain quantum computing",
    provider="openai",
    model="gpt-4",
    temperature=0.7,
    max_tokens=500
)
print(response.text)
print(f"Tokens used: {response.usage.total_tokens}")
```

### 4. Stream text generation

```python
for chunk in client.text.stream("Tell me a story"):
    if "delta" in chunk:
        print(chunk["delta"].get("content", ""), end="", flush=True)
print()
```

### 5. Work with sessions (conversations)

```python
# Create a session
session = client.sessions.create(
    name="My Chat",
    agent_config={
        "model": "gpt-4",
        "temperature": 0.7
    }
)

# Have a conversation
response = session.invoke("My name is Alice")
print(response.response.content)

response = session.invoke("What's my name?")
print(response.response.content)  # Remembers "Alice"

# Get conversation history
history = session.history()
for message in history:
    print(f"{message.role}: {message.content}")
```

### 6. Generate images

```python
# Simple mode
image = client.images.generate("A futuristic city")
print(image.image_url)

# With options
image = client.images.generate(
    prompt="A sunset over mountains, digital art",
    provider="dmxapi",
    model="gemini-2.5-flash-image",
    size="1920x1080",
    quality="hd"
)
print(f"Image: {image.image_url} ({image.width}x{image.height})")
```

### 7. Speech-to-Text (ASR)

```python
# Upload audio file
file_meta = client.files.upload("meeting.mp3")

# Transcribe
transcription = client.audio.transcribe(
    file_id=file_meta.file_id,
    language="zh"
)
print(transcription.text)
```

### 8. Knowledge Base & RAG

```python
# Create knowledge base
kb = client.knowledge_bases.create(
    name="Company Docs",
    description="Internal documentation"
)

# Upload documents (uses unified file architecture internally)
task = client.knowledge_bases.upload_document(
    kb_id=kb.kb_id,
    file="policy.pdf"
)

# Or use two-step process for file reuse
file_meta = client.files.upload("policy.pdf")
task = client.knowledge_bases.add_document(kb.kb_id, file_meta.file_id)
# Same file can be added to multiple knowledge bases!

# Search
results = client.knowledge_bases.search(
    query="What is the vacation policy?",
    knowledge_base_ids=[kb.kb_id],
    top_k=3
)

# Use results for RAG
context = "\n\n".join([r.content for r in results.results])
answer = client.text.generate(
    prompt=f"Based on this context:\n{context}\n\nQuestion: What is the vacation policy?"
)
print(answer.text)
```

## Configuration

The SDK can be configured via environment variables or constructor parameters:

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `NEXUS_API_KEY` | (required) | Your API key |
| `NEXUS_BASE_URL` | `http://localhost:8000/api/v1` | API base URL |
| `NEXUS_TIMEOUT` | `30` | Request timeout (seconds) |
| `NEXUS_MAX_RETRIES` | `3` | Maximum retry attempts |
| `NEXUS_POLL_INTERVAL` | `2` | Task polling interval (seconds) |
| `NEXUS_POLL_TIMEOUT` | `300` | Task polling timeout (seconds) |

## Development Mode vs Production

**Development Mode (Default)**:
```python
# Uses localhost by default
client = NexusAIClient()  # Points to http://localhost:8000/api/v1
```

**Production Mode**:
```bash
# Set environment variable
export NEXUS_BASE_URL=https://nexus-ai.juncai-ai.com/api/v1
```

Or in code:
```python
client = NexusAIClient(
    base_url="https://nexus-ai.juncai-ai.com/api/v1"
)
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from nexusai import NexusAIClient
from nexusai.error import (
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APITimeoutError,
)

client = NexusAIClient()

try:
    response = client.text.generate("Hello")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except NotFoundError:
    print("Resource not found")
except APITimeoutError:
    print("Request timed out")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Context Manager

The client supports context manager for automatic cleanup:

```python
with NexusAIClient() as client:
    response = client.text.generate("Hello")
    print(response.text)
# Client automatically closed
```

## API Reference

For detailed API documentation, see [docs/api_reference.md](docs/api_reference.md).

## Examples

Check out the [examples/](examples/) directory for more usage examples:

- `basic_usage.py` - Core features demonstration
- `streaming_example.py` - Streaming text generation
- `session_chat.py` - Multi-turn conversations
- `knowledge_base_rag.py` - RAG with knowledge bases

## Requirements

- Python 3.8+
- httpx >= 0.25.0
- pydantic >= 2.5.0
- python-dotenv >= 1.0.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: https://nexus-ai.juncai-ai.com/docs
- Issues: https://github.com/nexus-ai/python-sdk/issues
- Email: support@nexus-ai.com

## Changelog

### v0.1.0 (2025-01-03)

- Initial release
- Text generation (sync, async, streaming)
- Image generation
- Session management
- Audio processing (ASR/TTS)
- Knowledge base management
- File upload system
- Full type hints with Pydantic
