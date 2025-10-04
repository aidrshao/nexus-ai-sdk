# Changelog

All notable changes to the Nexus AI Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-03 (Updated 2025-10-03)

### 🔥 BREAKING CHANGE - Knowledge Base Document Upload Architecture (2025-10-03)

**Backend API Migration**: The knowledge base document upload endpoint has been upgraded to use the unified file architecture.

#### What Changed

The backend API endpoint `POST /knowledge-bases/{kb_id}/documents` has changed:
- **OLD**: Accepted `multipart/form-data` with file upload
- **NEW**: Accepts `application/json` with `{"file_id": "..."}`

This requires a two-step process:
1. Upload file to `/files` → get `file_id`
2. Add `file_id` to knowledge base → get processing task

#### SDK Changes (Backward Compatible)

✅ **Good news**: Your existing code continues to work!

The SDK has been updated to handle the new two-step process automatically:

```python
# Your existing code still works (internally upgraded)
task = client.knowledge_bases.upload_document(
    kb_id="kb_123",
    file="document.pdf"
)
```

**New capability added**: File reuse across knowledge bases

```python
# New method: add_document(kb_id, file_id)
file_meta = client.files.upload("shared_doc.pdf")
client.knowledge_bases.add_document("kb_sales", file_meta.file_id)
client.knowledge_bases.add_document("kb_support", file_meta.file_id)
```

#### Implementation Details

- Updated `KnowledgeBasesResource.upload_document()` to internally call `files.upload()` first
- Added new method `KnowledgeBasesResource.add_document(kb_id, file_id)`
- All 8 mock tests pass with new architecture
- Backward compatibility maintained - no user code changes required

#### Benefits

- ✅ File reuse across multiple knowledge bases
- ✅ Automatic deduplication of identical files
- ✅ Large file support (up to 5GB via cloud storage)
- ✅ Unified file management via `client.files` API

### Added
- Initial alpha release of Nexus AI Python SDK
- Core client implementation with configuration management
- Text generation support (synchronous, asynchronous, streaming)
- Image generation with automatic task polling
- Session management for stateful conversations
- File upload and management system
- Audio processing (ASR/TTS) capabilities
- Knowledge base creation and search functionality
- Comprehensive error handling with 9 exception types
- Full type hints using Pydantic models
- Development mode defaulting to localhost:8000
- Easy production switch via environment variables
- Context manager support for client
- Lazy-loading resource architecture
- HTTP/2 support via httpx
- Automatic retry logic for failed requests
- Comprehensive unit test suite (41 tests)
- Code formatting with Black
- Complete documentation and examples

### Known Limitations
- API integration testing pending (waiting for production API)
- Some edge case tests may fail (to be refined in v0.2.0)
- Limited error message localization

### API Endpoints
- `/invoke` - Text and image generation
- `/tasks/{task_id}` - Task status polling
- `/sessions` - Session CRUD operations
- `/sessions/{session_id}/invoke` - Session interactions
- `/files` - File upload and management
- `/audio/transcribe` - Audio transcription
- `/audio/tts` - Text-to-speech
- `/knowledge-bases` - Knowledge base operations

### Configuration
Default configuration:
- `base_url`: http://localhost:8000/api/v1
- `timeout`: 30 seconds
- `max_retries`: 3
- `poll_interval`: 2 seconds
- `poll_timeout`: 300 seconds

### Dependencies
- Python 3.8+
- httpx >= 0.25.0
- pydantic >= 2.5.0
- python-dotenv >= 1.0.0
- typing-extensions >= 4.8.0

---

## [Unreleased]

### Planned for v0.2.0
- Real API integration testing
- Enhanced error messages
- Additional examples
- Performance optimizations
- CI/CD pipeline
- Multi-language documentation

---

[0.1.0]: https://github.com/nexus-ai/python-sdk/releases/tag/v0.1.0
