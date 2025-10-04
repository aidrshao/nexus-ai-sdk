#!/usr/bin/env python3
"""
Test SDK with mock data.

This script tests all SDK functionality using mock responses,
demonstrating that the SDK logic is correct and ready for real API.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from unittest.mock import Mock, patch, MagicMock
from nexusai import NexusAIClient
from nexusai.models import Image, TextResponse, Usage, SessionResponse, Message
import json

print("=" * 70)
print("NEXUS AI SDK - Mock Test (All Features)")
print("=" * 70)
print("\nThis test uses mock data to verify SDK functionality")
print("while the real API is being finalized.\n")

# Test results tracking
results = {
    'passed': [],
    'failed': []
}

def test_client_initialization():
    """Test 1: Client initialization."""
    print("\n" + "=" * 70)
    print("[TEST 1] Client Initialization")
    print("=" * 70)

    try:
        # Set API key
        os.environ['NEXUS_API_KEY'] = 'nxs_test_key_for_mock'

        client = NexusAIClient()
        print(f"[OK] Client initialized")
        print(f"     Base URL: {client._internal_client.base_url}")

        # Check all resource properties
        resources = ['images', 'text', 'sessions', 'files', 'audio', 'knowledge_bases']
        for resource in resources:
            assert hasattr(client, resource), f"Missing resource: {resource}"
            print(f"     [OK] client.{resource} available")

        results['passed'].append('Client Initialization')
        return client

    except Exception as e:
        print(f"[FAIL] {e}")
        results['failed'].append(f'Client Initialization: {str(e)}')
        return None

def test_text_generation_sync(client):
    """Test 2: Synchronous text generation."""
    print("\n" + "=" * 70)
    print("[TEST 2] Text Generation (Sync)")
    print("=" * 70)

    try:
        # Mock the HTTP client request
        mock_response = {
            "output": {
                "text": "你好！我是 Nexus AI 助手。我可以帮助你进行文本生成、图像创作、语音识别等多种AI任务。",
                "usage": {
                    "prompt_tokens": 5,
                    "completion_tokens": 35,
                    "total_tokens": 40
                },
                "model": "gpt-4o-mini",
                "finish_reason": "stop"
            }
        }

        with patch.object(client._internal_client, 'request', return_value=mock_response):
            response = client.text.generate(
                prompt="你好，请介绍一下自己",
                temperature=0.7,
                max_tokens=100
            )

        print(f"[OK] Text generation successful")
        print(f"     Prompt: '你好，请介绍一下自己'")
        print(f"     Response: {response.text}")
        print(f"     Model: {response.model}")
        print(f"     Tokens: {response.usage.total_tokens}")

        # Verify response structure
        assert isinstance(response.text, str)
        assert response.usage.total_tokens > 0

        results['passed'].append('Text Generation (Sync)')

    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        results['failed'].append(f'Text Generation (Sync): {str(e)}')

def test_text_streaming(client):
    """Test 3: Streaming text generation."""
    print("\n" + "=" * 70)
    print("[TEST 3] Text Generation (Stream)")
    print("=" * 70)

    try:
        # Mock streaming response
        mock_chunks = [
            {"delta": {"content": "机器"}},
            {"delta": {"content": "学习"}},
            {"delta": {"content": "是"}},
            {"delta": {"content": "人工智能"}},
            {"delta": {"content": "的"}},
            {"delta": {"content": "一个"}},
            {"delta": {"content": "分支"}},
        ]

        def mock_stream(*args, **kwargs):
            for chunk in mock_chunks:
                yield chunk

        with patch.object(client._internal_client, 'stream', side_effect=mock_stream):
            print(f"[INFO] Streaming: ", end="", flush=True)
            full_text = ""
            chunk_count = 0

            for chunk in client.text.stream(
                prompt="什么是机器学习？",
                max_tokens=50
            ):
                if "delta" in chunk and "content" in chunk["delta"]:
                    content = chunk["delta"]["content"]
                    print(content, end="", flush=True)
                    full_text += content
                    chunk_count += 1

            print()  # New line

        print(f"[OK] Streaming successful")
        print(f"     Received {chunk_count} chunks")
        print(f"     Full text: {full_text}")

        assert chunk_count == len(mock_chunks)

        results['passed'].append('Text Generation (Stream)')

    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        results['failed'].append(f'Text Generation (Stream): {str(e)}')

def test_session_management(client):
    """Test 4: Session management."""
    print("\n" + "=" * 70)
    print("[TEST 4] Session Management")
    print("=" * 70)

    try:
        # Mock session creation
        mock_session_data = {
            "session_id": "sess_mock_abc123",
            "agent_type": "assistant",
            "agent_config": {
                "model": "gpt-4",
                "temperature": 0.7
            },
            "is_active": True,
            "created_at": "2025-01-03T20:00:00Z"
        }

        with patch.object(client._internal_client, 'request', return_value=mock_session_data):
            session = client.sessions.create(
                name="Mock Test Session",
                agent_config={"model": "gpt-4", "temperature": 0.7}
            )

        print(f"[OK] Session created")
        print(f"     Session ID: {session.id}")
        print(f"     Agent type: {session.agent_type}")

        # Mock session invoke
        mock_invoke_response = {
            "session_id": "sess_mock_abc123",
            "response": {
                "role": "assistant",
                "content": "你好，Alice！很高兴认识你。我会记住你的名字。",
                "timestamp": "2025-01-03T20:01:00Z"
            },
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }

        with patch.object(client._internal_client, 'request', return_value=mock_invoke_response):
            response = session.invoke("我叫 Alice")

        print(f"[OK] Session invoke successful")
        print(f"     User: '我叫 Alice'")
        print(f"     Assistant: {response.response.content}")

        # Mock session history
        mock_history = {
            "messages": [
                {
                    "role": "user",
                    "content": "我叫 Alice",
                    "timestamp": "2025-01-03T20:00:00Z"
                },
                {
                    "role": "assistant",
                    "content": "你好，Alice！很高兴认识你。",
                    "timestamp": "2025-01-03T20:00:02Z"
                }
            ]
        }

        with patch.object(client._internal_client, 'request', return_value=mock_history):
            history = session.history(limit=10)

        print(f"[OK] Session history retrieved")
        print(f"     Message count: {len(history)}")

        # Mock session deletion
        with patch.object(client._internal_client, 'request', return_value={}):
            session.delete()

        print(f"[OK] Session deleted")

        assert session.id == "sess_mock_abc123"
        assert len(history) == 2

        results['passed'].append('Session Management')

    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        results['failed'].append(f'Session Management: {str(e)}')

def test_image_generation(client):
    """Test 5: Image generation with async polling."""
    print("\n" + "=" * 70)
    print("[TEST 5] Image Generation (Async + Polling)")
    print("=" * 70)

    try:
        # Mock task creation
        mock_task_response = {
            "task_id": "task_img_123",
            "status": "queued",
            "task_type": "image_generation"
        }

        # Mock task completion
        mock_task_complete = {
            "task_id": "task_img_123",
            "status": "completed",
            "output": {
                "image_url": "http://localhost:8000/storage/images/sunset-12345.png",
                "width": 1024,
                "height": 1024,
                "revised_prompt": "A beautiful sunset over mountains, digital art style"
            }
        }

        print(f"[INFO] Submitting image generation task...")

        with patch.object(client._internal_client, 'request') as mock_request:
            # First call: create task
            # Second call: poll task (completed)
            mock_request.side_effect = [mock_task_response, mock_task_complete]

            image = client.images.generate(
                prompt="A beautiful sunset over mountains",
                size="1024x1024"
            )

        print(f"[OK] Image generated")
        print(f"     Image URL: {image.image_url}")
        print(f"     Dimensions: {image.width}x{image.height}")

        assert image.width == 1024
        assert image.height == 1024

        results['passed'].append('Image Generation')

    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        results['failed'].append(f'Image Generation: {str(e)}')

def test_file_operations(client):
    """Test 6: File upload and management."""
    print("\n" + "=" * 70)
    print("[TEST 6] File Operations")
    print("=" * 70)

    try:
        # Create temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test file content for Nexus AI SDK")
            temp_file = f.name

        # Mock file upload
        mock_file_response = {
            "file_id": "file_mock_xyz789",
            "filename": "test.txt",
            "content_type": "text/plain",
            "size": 35,
            "created_at": "2025-01-03T20:00:00Z"
        }

        print(f"[INFO] Uploading file: {temp_file}")

        # Mock the httpx client post method
        mock_response = Mock()
        mock_response.json.return_value = mock_file_response
        mock_response.status_code = 200

        with patch.object(client._internal_client.client, 'post', return_value=mock_response):
            file_meta = client.files.upload(temp_file)

        print(f"[OK] File uploaded")
        print(f"     File ID: {file_meta.file_id}")
        print(f"     Filename: {file_meta.filename}")
        print(f"     Size: {file_meta.size} bytes")

        # Mock file get
        with patch.object(client._internal_client, 'request', return_value=mock_file_response):
            retrieved = client.files.get(file_meta.file_id)

        print(f"[OK] File metadata retrieved")

        # Mock file delete
        mock_delete = {"message": "File deleted successfully"}
        with patch.object(client._internal_client, 'request', return_value=mock_delete):
            result = client.files.delete(file_meta.file_id)

        print(f"[OK] File deleted")

        # Clean up
        os.unlink(temp_file)

        assert file_meta.file_id == "file_mock_xyz789"

        results['passed'].append('File Operations')

    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        results['failed'].append(f'File Operations: {str(e)}')

        # Clean up
        if 'temp_file' in locals() and os.path.exists(temp_file):
            os.unlink(temp_file)

def test_audio_transcription(client):
    """Test 7: Audio transcription (ASR)."""
    print("\n" + "=" * 70)
    print("[TEST 7] Audio Transcription (ASR)")
    print("=" * 70)

    try:
        # Mock task creation and completion
        mock_task_response = {
            "task_id": "task_asr_456",
            "status": "queued"
        }

        mock_task_complete = {
            "task_id": "task_asr_456",
            "status": "completed",
            "output": {
                "text": "这是一段测试音频的转录文本。我们正在测试 Nexus AI 的语音识别功能。",
                "language": "zh",
                "duration": 5.2
            }
        }

        print(f"[INFO] Transcribing audio file...")

        with patch.object(client._internal_client, 'request') as mock_request:
            mock_request.side_effect = [mock_task_response, mock_task_complete]

            transcription = client.audio.transcribe(
                file_id="file_audio_123",
                language="zh"
            )

        print(f"[OK] Transcription successful")
        print(f"     Text: {transcription.text}")
        print(f"     Language: {transcription.language}")
        print(f"     Duration: {transcription.duration}s")

        assert transcription.language == "zh"

        results['passed'].append('Audio Transcription')

    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        results['failed'].append(f'Audio Transcription: {str(e)}')

def test_knowledge_base(client):
    """Test 8: Knowledge base operations."""
    print("\n" + "=" * 70)
    print("[TEST 8] Knowledge Base Operations")
    print("=" * 70)

    try:
        # Mock KB creation
        mock_kb = {
            "kb_id": "kb_mock_123",
            "name": "Test KB",
            "description": "Mock knowledge base for testing",
            "embedding_model": "BAAI/bge-base-zh-v1.5",
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "document_count": 0,
            "created_at": "2025-01-03T20:00:00Z"
        }

        print(f"[INFO] Creating knowledge base...")

        with patch.object(client._internal_client, 'request', return_value=mock_kb):
            kb = client.knowledge_bases.create(
                name="Test KB",
                description="Mock knowledge base for testing"
            )

        print(f"[OK] Knowledge base created")
        print(f"     KB ID: {kb.kb_id}")
        print(f"     Name: {kb.name}")

        # Test document upload (new two-step architecture)
        print(f"[INFO] Testing document upload (two-step process)...")

        # Mock file upload response
        mock_file_response = {
            "file_id": "file_doc_456",
            "filename": "test_document.pdf",
            "size": 1024000,
            "content_type": "application/pdf",
            "created_at": "2025-01-03T20:01:00Z"
        }

        # Mock add document task response
        mock_add_doc_task = {
            "task_id": "task_doc_789",
            "status": "queued",
            "task_type": "document_processing"
        }

        # Create a temporary mock file
        from io import BytesIO
        mock_file_obj = BytesIO(b"Mock PDF content")

        with patch.object(client._internal_client.client, 'post') as mock_post:
            # Mock file upload
            mock_upload_response = MagicMock()
            mock_upload_response.status_code = 200
            mock_upload_response.json.return_value = mock_file_response
            mock_post.return_value = mock_upload_response

            with patch.object(client._internal_client, 'request', return_value=mock_add_doc_task):
                task = client.knowledge_bases.upload_document(
                    kb_id=kb.kb_id,
                    file=mock_file_obj,
                    filename="test_document.pdf"
                )

        print(f"[OK] Document uploaded via two-step process")
        print(f"     Task ID: {task.task_id}")
        print(f"     Status: {task.status}")

        # Mock search
        mock_search_result = {
            "query": "什么是AI？",
            "results": [
                {
                    "chunk_id": "chunk_001",
                    "doc_id": "doc_001",
                    "kb_id": "kb_mock_123",
                    "content": "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
                    "similarity_score": 0.92,
                    "metadata": {"page": 1}
                },
                {
                    "chunk_id": "chunk_002",
                    "doc_id": "doc_001",
                    "kb_id": "kb_mock_123",
                    "content": "AI技术包括机器学习、深度学习、自然语言处理等多个领域。",
                    "similarity_score": 0.85,
                    "metadata": {"page": 2}
                }
            ],
            "total_results": 2
        }

        print(f"[INFO] Searching knowledge base...")

        with patch.object(client._internal_client, 'request', return_value=mock_search_result):
            search_results = client.knowledge_bases.search(
                query="什么是AI？",
                knowledge_base_ids=[kb.kb_id],
                top_k=3
            )

        print(f"[OK] Search successful")
        print(f"     Query: {search_results.query}")
        print(f"     Results: {len(search_results.results)}")
        for i, result in enumerate(search_results.results, 1):
            print(f"       [{i}] Score: {result.similarity_score:.2f}")
            print(f"           {result.content[:60]}...")

        assert len(search_results.results) == 2
        assert search_results.results[0].similarity_score > 0.9

        results['passed'].append('Knowledge Base Operations')

    except Exception as e:
        print(f"[FAIL] {e}")
        import traceback
        traceback.print_exc()
        results['failed'].append(f'Knowledge Base Operations: {str(e)}')

# Run all tests
print("\n" + "=" * 70)
print("Starting Mock Tests...")
print("=" * 70)

client = test_client_initialization()

if client:
    test_text_generation_sync(client)
    test_text_streaming(client)
    test_session_management(client)
    test_image_generation(client)
    test_file_operations(client)
    test_audio_transcription(client)
    test_knowledge_base(client)

# Print summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

print(f"\n[PASSED] {len(results['passed'])} tests:")
for test in results['passed']:
    print(f"  - {test}")

if results['failed']:
    print(f"\n[FAILED] {len(results['failed'])} tests:")
    for test in results['failed']:
        print(f"  - {test}")

print("\n" + "=" * 70)

if not results['failed']:
    print("[SUCCESS] All mock tests passed!")
    print("\nSDK is fully functional and ready for real API integration.")
    print("When the API is ready, run: python test_with_api.py")
else:
    print("[WARN] Some tests failed")

print("=" * 70)

sys.exit(0 if not results['failed'] else 1)
