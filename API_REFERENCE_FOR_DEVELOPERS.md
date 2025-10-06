# Nexus AI SDK - Complete API Reference for Application Developers

**Package**: `keystone-ai` (import as `nexusai`)
**Version**: 0.2.1a1 (Alpha)
**Last Updated**: 2025-10-06

---

## 📦 Installation

```bash
# Install alpha version (required --pre flag)
pip install keystone-ai --pre

# Or use specific version
pip install keystone-ai==0.2.1a1 --pre

# Verify installation
python -c "import nexusai; print(nexusai.__version__)"
```

**国内镜像加速**：
```bash
# 清华镜像
pip install keystone-ai --pre -i https://pypi.tuna.tsinghua.edu.cn/simple

# 阿里云镜像
pip install keystone-ai --pre -i https://mirrors.aliyun.com/pypi/simple/
```

---

## 🚀 Quick Start

```python
from nexusai import NexusAIClient

# Initialize client (uses production API automatically)
client = NexusAIClient(api_key="your_api_key_here")

# Generate text
response = client.text.generate("Hello, AI!")
print(response.text)
```

---

## 🎯 Supported Models

### Text Generation Models

**三档模型体系**：

#### 🥇 高端模型 (Premium Tier)
| Model | Speed | Cost | Best For | Temperature Range |
|-------|-------|------|----------|-------------------|
| `gpt-5` | ⚡⚡⚡ **最快** | 💰 最贵 | 复杂推理 + 速度要求 | 0.0 - 2.0 |
| `gemini-2.5-pro` | ⚡⚡ 较慢 | 💰 最贵 | 复杂推理、深度分析 | 0.0 - 2.0 |

#### 🥈 中端模型 (Standard Tier)
| Model | Speed | Cost | Best For | Temperature Range |
|-------|-------|------|----------|-------------------|
| `gpt-5-mini` | ⚡⚡⚡ 快 | 💰💰 中等 | **推荐** - 通用任务、对话 | 0.0 - 2.0 |
| `gpt-4o-mini` | ⚡⚡⚡ 快 | 💰💰 中等 | 通用任务、对话 | 0.0 - 2.0 |

#### 🥉 经济模型 (Budget Tier)
| Model | Speed | Cost | Best For | Temperature Range |
|-------|-------|------|----------|-------------------|
| `deepseek-v3.2-exp` | ⚡⚡ 中等 | 💰💰💰 **最便宜** | 成本敏感型应用 | 0.0 - 2.0 |

**Default Model**: `gpt-5-mini` (if not specified)

**模型选择建议**：
- **gpt-5**: 需要顶级推理能力 + 最快响应（如实时客服、复杂分析）
- **gemini-2.5-pro**: 需要顶级推理能力，对速度不敏感（如深度研究、长文分析）
- **gpt-5-mini**: 日常通用任务的最佳选择（推荐）
- **gpt-4o-mini**: 备选通用模型
- **deepseek-v3.2-exp**: 大批量、成本敏感场景（如批量翻译、简单分类）

**Usage Example**:
```python
# 高端模型 - 快速 + 复杂推理
response = client.text.generate(
    prompt="分析这份复杂的法律合同，找出潜在风险",
    model="gpt-5",  # 最快的高端模型
    temperature=0.3
)

# 高端模型 - 深度分析
response = client.text.generate(
    prompt="对这篇学术论文进行深度批判性分析",
    model="gemini-2.5-pro",  # 最强推理能力
    temperature=0.3
)

# 中端模型 - 推荐用于大多数场景
response = client.text.generate(
    prompt="总结这篇文章的要点",
    model="gpt-5-mini",  # 默认推荐
    temperature=0.7
)

# 经济模型 - 成本优先
response = client.text.generate(
    prompt="将以下文本翻译成英文",
    model="deepseek-v3.2-exp",  # 最便宜
    temperature=0.5
)
```

---

### Image Generation Models

| Model | Quality | Speed | Best For |
|-------|---------|-------|----------|
| `doubao-seedream-4-0-250828` | 🌟🌟🌟 高质量 | ⚡⚡⚡ 快 | **默认推荐** - 通用图片生成 |
| `gemini-2.5-flash-image` | 🌟🌟🌟 高质量 | ⚡⚡ 中等 | 备选方案 |

**Default Model**: `doubao-seedream-4-0-250828` (if not specified)

**模型选择建议**：
- **doubao-seedream-4-0-250828**: 字节豆包即梦模型，速度快、质量高（推荐）
- **gemini-2.5-flash-image**: Google Gemini图片模型，备选方案

**Supported Aspect Ratios**:
```python
"1:1"    # Square (1024x1024)
"16:9"   # Landscape widescreen (1792x1024)
"9:16"   # Portrait widescreen (1024x1792)
"4:3"    # Standard landscape (1365x1024)
"3:4"    # Standard portrait (1024x1365)
"21:9"   # Ultra-wide (2389x1024)
```

**❌ Not Supported**: Custom pixel dimensions (e.g., `1920x1080`)

**Usage Example**:
```python
# Single image (uses default model)
image = client.image.generate(
    prompt="A professional business headshot, white background",
    aspect_ratio="1:1",
    num_images=1
)
print(f"Image URL: {image.url}")

# With explicit model selection
image = client.image.generate(
    prompt="A professional business headshot, white background",
    model="doubao-seedream-4-0-250828",  # 默认推荐模型
    aspect_ratio="1:1",
    num_images=1
)

# Batch generation (e.g., for employee matrix)
images = client.image.generate(
    prompt="Professional headshot, neutral background, diverse person",
    model="doubao-seedream-4-0-250828",
    aspect_ratio="1:1",
    num_images=8  # Generate 8 images at once
)
for img in images:
    print(f"Image {img.index + 1}: {img.url}")
```

---

## 📚 Core API Reference

### 1. Text Generation

#### `client.text.generate()`

**Basic Usage**:
```python
response = client.text.generate(
    prompt="Write a poem about spring",
    model="gpt-5-mini",         # Optional, defaults to gpt-5-mini
    temperature=0.7,            # Optional, 0.0-2.0, default 0.7
    max_tokens=500,             # Optional, default None (unlimited)
    top_p=0.9,                  # Optional, 0.0-1.0, default None
    stream=False                # Optional, set True for streaming
)

print(response.text)
print(f"Tokens: {response.usage.total_tokens}")
```

**Response Object**:
```python
{
    "text": str,              # Generated text
    "usage": {
        "prompt_tokens": int,
        "completion_tokens": int,
        "total_tokens": int
    },
    "model": str,             # Model used
    "finish_reason": str      # "stop", "length", etc.
}
```

---

#### `client.text.generate_stream()`

**Streaming Usage**:
```python
for chunk in client.text.generate_stream(
    prompt="Tell me a long story",
    model="gpt-5-mini",
    temperature=0.8
):
    print(chunk.text, end="", flush=True)
print()  # New line after streaming
```

---

### 2. Image Generation

#### `client.image.generate()`

**Parameters**:
```python
image = client.image.generate(
    prompt=str,                              # Required: image description
    model="doubao-seedream-4-0-250828",      # Optional, default model
    aspect_ratio="16:9",                     # Required: one of the supported ratios
    num_images=1                             # Optional, 1-8, default 1
)
```

**Response Object** (single image):
```python
{
    "url": str,           # Image URL (valid for 24 hours)
    "width": int,         # Image width in pixels
    "height": int,        # Image height in pixels
    "index": int          # 0 for single image
}
```

**Response Object** (multiple images):
```python
[
    {"url": str, "width": int, "height": int, "index": 0},
    {"url": str, "width": int, "height": int, "index": 1},
    ...
]
```

**⚠️ Important Notes**:
1. **Style prompts**: Include style in main prompt (no separate `style` parameter)
   ```python
   # ✅ Correct
   prompt = "Cyberpunk style futuristic city, neon lights, rain"

   # ❌ Wrong (no style parameter supported)
   prompt = "Futuristic city", style = "cyberpunk"
   ```

2. **Aspect ratio only**: No custom pixel dimensions
   ```python
   # ✅ Correct
   aspect_ratio = "16:9"

   # ❌ Wrong
   size = "1920x1080"  # Not supported
   ```

---

### 3. Session Management (Conversations)

#### `client.sessions.create()`

**Create a Session**:
```python
session = client.sessions.create(
    name="Customer Support Chat",
    agent_config={
        "model": "gpt-5-mini",  # 推荐使用中端模型
        "temperature": 0.7,
        "system_prompt": "You are a helpful customer support agent."
    }
)

print(f"Session ID: {session.session_id}")
```

---

#### `session.invoke()`

**Send Messages**:
```python
# First message
response = session.invoke("My name is Alice")
print(response.response.content)

# Follow-up (remembers context)
response = session.invoke("What's my name?")
print(response.response.content)  # Output: "Your name is Alice"
```

**Temporary Config Override**:
```python
# Override temperature for this message only
response = session.invoke(
    "Be creative and write a poem",
    config={"temperature": 1.5}  # Higher creativity for this message
)
# Session's base temperature remains 0.7
```

---

#### `session.history()`

**Get Conversation History**:
```python
history = session.history()

for message in history.messages:
    print(f"{message.role}: {message.content}")
    print(f"Timestamp: {message.created_at}")
```

---

### 4. Knowledge Base & RAG

#### `client.knowledge_bases.create()`

```python
kb = client.knowledge_bases.create(
    name="Company Documentation",
    description="Internal policies and procedures"
)
print(f"Knowledge Base ID: {kb.kb_id}")
```

---

#### `client.knowledge_bases.upload_document()`

**Upload and Process Document**:
```python
# Single-step upload
task = client.knowledge_bases.upload_document(
    kb_id=kb.kb_id,
    file="employee_handbook.pdf"
)

# Wait for processing
import time
while True:
    status = client.tasks.get(task.task_id)
    if status.status == "completed":
        print("Document processed!")
        break
    elif status.status == "failed":
        print(f"Failed: {status.error}")
        break
    time.sleep(2)
```

**Reuse Files Across Knowledge Bases**:
```python
# Upload once
file_meta = client.files.upload("shared_policy.pdf")

# Add to multiple knowledge bases
client.knowledge_bases.add_document("kb_sales", file_meta.file_id)
client.knowledge_bases.add_document("kb_support", file_meta.file_id)
client.knowledge_bases.add_document("kb_hr", file_meta.file_id)
```

---

#### `client.knowledge_bases.search()`

```python
results = client.knowledge_bases.search(
    query="What is the vacation policy?",
    knowledge_base_ids=[kb.kb_id],
    top_k=3  # Return top 3 most relevant chunks
)

for result in results.results:
    print(f"Score: {result.score}")
    print(f"Content: {result.content}")
    print(f"Source: {result.metadata.get('filename')}")
```

---

### 5. File Operations

#### `client.files.upload()`

```python
file_meta = client.files.upload("document.pdf")

print(f"File ID: {file_meta.file_id}")
print(f"Filename: {file_meta.filename}")
print(f"Size: {file_meta.file_size} bytes")
```

**Supported File Types**:
- Documents: `.pdf`, `.txt`, `.md`, `.docx`
- Audio: `.mp3`, `.wav`, `.m4a`, `.flac`
- Images: `.png`, `.jpg`, `.jpeg`, `.webp`
- ⚠️ Not supported: `.json`, `.csv`, `.xlsx` (coming in v0.3.0)

---

#### `client.files.list()`

```python
response = client.files.list(page=1, per_page=20)

print(f"Total files: {response.total}")
for file in response.files:
    print(f"{file.filename} ({file.file_size} bytes)")
```

---

### 6. Audio Processing

#### `client.audio.transcribe()` (ASR)

```python
# Upload audio file
file_meta = client.files.upload("meeting.mp3")

# Transcribe
transcription = client.audio.transcribe(
    file_id=file_meta.file_id,
    language="zh"  # "zh" for Chinese, "en" for English
)

print(transcription.text)
```

#### `client.audio.text_to_speech()` (TTS)

⚠️ **Not Yet Implemented** - Coming in v0.3.0

---

## 🔐 Configuration

### Environment Variables

Create a `.env` file:
```bash
# Required
NEXUS_API_KEY=your_api_key_here

# Optional (defaults shown)
NEXUS_BASE_URL=https://nexus-ai.juncai-ai.com/api/v1
NEXUS_TIMEOUT=30
NEXUS_MAX_RETRIES=3
```

### Code Configuration

```python
from nexusai import NexusAIClient

# Production (default)
client = NexusAIClient(api_key="your_key")

# Custom configuration
client = NexusAIClient(
    api_key="your_key",
    base_url="https://custom-api.example.com/api/v1",
    timeout=60,
    max_retries=5
)
```

---

## ⚠️ Error Handling

```python
from nexusai import NexusAIClient
from nexusai.error import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    APITimeoutError,
    NetworkError
)

client = NexusAIClient()

try:
    response = client.text.generate("Hello")
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Invalid parameters: {e.validation_errors}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except APITimeoutError:
    print("Request timed out")
except NetworkError as e:
    if e.is_retryable:
        print("Network error, will retry")
except APIError as e:
    print(f"API error: {e}")
```

---

## 💡 Best Practices

### 1. Model Selection

**文本模型选择决策树**：

```python
# 需要最强推理 + 最快速度？ → gpt-5
model = "gpt-5"

# 需要最强推理，速度不重要？ → gemini-2.5-pro
model = "gemini-2.5-pro"

# 日常通用任务（推荐）？ → gpt-5-mini
model = "gpt-5-mini"

# 大批量、成本敏感？ → deepseek-v3.2-exp
model = "deepseek-v3.2-exp"
```

**图片模型选择**：

```python
# 默认推荐（快速、高质量）
model = "doubao-seedream-4-0-250828"

# 备选方案
model = "gemini-2.5-flash-image"
```

### 2. Temperature Guidelines

```python
# Factual/deterministic tasks (summaries, translations)
temperature = 0.0 - 0.3

# Balanced creativity (general conversation)
temperature = 0.7

# Creative tasks (stories, brainstorming)
temperature = 0.9 - 1.5
```

### 3. Session Management

```python
# Reuse sessions for multi-turn conversations
session = client.sessions.create(name="User Chat", agent_config={...})

# Don't create new session for each message!
# ❌ Bad
for message in messages:
    session = client.sessions.create(...)  # Wasteful!
    session.invoke(message)

# ✅ Good
session = client.sessions.create(...)
for message in messages:
    session.invoke(message)
```

### 4. File Management

```python
# Upload once, reuse across knowledge bases
file_meta = client.files.upload("large_document.pdf")
client.knowledge_bases.add_document("kb_1", file_meta.file_id)
client.knowledge_bases.add_document("kb_2", file_meta.file_id)
```

---

## 📊 Usage Quotas & Cost Control

### Recommended Quota Structure

**Free Tier**:
- Text: 50 generations/month (gpt-5-mini/gpt-4o-mini/deepseek only)
- Images: 20 images/month (doubao model only)
- Sessions: 5 active sessions
- Knowledge Bases: 1 KB, max 10 documents

**Pro Tier**:
- Text: 500 generations/month (all models including gpt-5/gemini-2.5-pro)
- Images: 200 images/month (all models)
- Sessions: Unlimited
- Knowledge Bases: 10 KBs, unlimited documents

### Cost Estimation Example

```python
def estimate_cost(num_employees, images_per_employee, model="doubao-seedream-4-0-250828"):
    """
    Estimate image generation cost

    Args:
        num_employees: Number of employees
        images_per_employee: Images per employee (1-3)
        model: Image model to use

    Returns:
        dict with cost breakdown
    """
    # Pricing (example - replace with actual)
    IMAGE_COST = {
        "doubao-seedream-4-0-250828": 1.5,  # ¥1.5 per image
        "gemini-2.5-flash-image": 2.0       # ¥2.0 per image
    }

    total_images = num_employees * images_per_employee
    cost_per_image = IMAGE_COST.get(model, 2.0)
    total_cost = total_images * cost_per_image

    return {
        "total_images": total_images,
        "cost_per_image": cost_per_image,
        "total_cost": total_cost,
        "currency": "CNY"
    }

# Example: 8 employees, 2 images each
estimate = estimate_cost(8, 2)
print(f"Total: ¥{estimate['total_cost']} for {estimate['total_images']} images")
# Output: Total: ¥32.0 for 16 images
```

---

## 🚧 Alpha Version Limitations

1. **Shared API Key**: All users use same key (individual keys in v0.3.0)
2. **No TTS**: Text-to-speech not implemented yet
3. **Limited File Types**: No JSON/CSV/XLSX support yet
4. **No Usage Tracking**: You need to implement quota tracking

---

## 📞 Support

- **Documentation**: https://nexus-ai.juncai-ai.com/docs
- **GitHub Issues**: https://github.com/aidrshao/nexus-ai-sdk/issues
- **Email**: support@nexus-ai.com

---

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Version**: 0.2.1a1
**Last Updated**: 2025-10-06
