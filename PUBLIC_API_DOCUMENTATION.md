# Nexus AI 开发者API文档

> **版本**: v1.0
> **基础URL**: `https://nexus-ai.juncai-ai.com`
> **认证方式**: Bearer Token (API Key)
> **最后更新**: 2025-01-02

---

## 快速开始

Nexus AI 是一个企业级统一AI能力平台，为开发者提供简单、强大的AI集成能力。

### 认证

所有API请求都需要在请求头中包含您的API密钥：

```bash
Authorization: Bearer YOUR_API_KEY
```

#### 如何获取 API Key

请联系系统管理员获取您的 API Key。API Key 格式示例：`nxs_xxxxxxxxxxxxxx`

#### 认证错误处理

| 错误信息 | HTTP状态码 | 原因 | 解决方法 |
|---------|-----------|------|---------|
| `Missing Authorization header` | 401 | 请求头中缺少认证信息 | 确保在请求头中添加 `Authorization: Bearer YOUR_API_KEY` |
| `Invalid API key` | 401 | API Key 不存在或格式错误 | 检查 API Key 是否正确，应以 `nxs_` 开头 |
| `API key is disabled` | 401 | API Key 已被禁用 | 联系管理员重新激活或获取新的 Key |
| `Rate limit exceeded` | 429 | 超过速率限制 | 降低请求频率或联系管理员提升限额 |

#### 安全最佳实践

- ✅ 使用环境变量存储 API Key，不要硬编码在代码中
- ✅ 不要将 API Key 提交到代码仓库
- ✅ 定期轮换 API Key
- ✅ 使用 HTTPS 进行通信
- ✅ 遵守速率限制，避免被限流

### 基础请求示例

> **提示**: 以下所有示例中的 `$BASE_URL` 代表基础URL：`https://nexus-ai.juncai-ai.com`

```bash
# 设置基础URL环境变量（方便复制使用）
export BASE_URL="$BASE_URL"

# 发起请求（省心模式 - 推荐）
curl -X POST "$BASE_URL/api/v1/invoke" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "text_generation",
    "input": {
      "prompt": "你好，请介绍一下人工智能"
    }
  }'
```

---

## API概览

Nexus AI 提供以下核心功能：

| 功能模块 | API数量 | 描述 |
|---------|---------|------|
| [文件管理](#1-文件管理) | 3个 | 统一文件上传和管理（核心基础设施） |
| [AI调用](#2-ai调用) | 2个 | 统一的AI能力调用接口 |
| [会话管理](#3-会话管理) | 6个 | 构建具有上下文记忆的多轮对话 |
| [知识库](#4-知识库) | 7个 | 私有知识库的创建和管理 |

---

## 1. 文件管理

**核心架构原则**：Nexus AI 实现了统一文件上传架构，将"文件上传"和"文件处理"完全解耦。

### 工作流程

```
Step 1: 上传文件 → 获得 file_id（文件的平台身份证）
Step 2: 使用 file_id → 进行任何AI操作（ASR、RAG等）
```

### 1.1 上传文件

`POST /api/v1/files`

上传文件到平台，获得唯一的 `file_id` 用于后续所有操作。

#### 请求格式

`multipart/form-data`

| 字段 | 类型 | 描述 |
|------|------|------|
| file | file | 文件（支持音频、图片、视频、文档） |

#### 支持的文件类型

- **音频**: mp3, wav, m4a, flac, aac, ogg, wma
- **图片**: jpg, jpeg, png, gif, webp, bmp
- **视频**: mp4, avi, mov, mkv, flv, wmv
- **文档**: pdf, txt, md, docx, doc

#### 示例

```bash
curl -X POST "$BASE_URL/api/v1/files" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@meeting_audio.mp3"
```

#### 响应

```json
{
  "file_id": "file_abc123def456",
  "filename": "meeting_audio.mp3",
  "content_type": "audio/mpeg",
  "size": 2048576,
  "created_at": "2025-10-03T05:30:00Z",
  "message": "File 'meeting_audio.mp3' uploaded successfully. Use 'file_id' for all subsequent operations."
}
```

> **重要**：响应中**只包含 file_id**，不包含文件URL。这是平台的核心安全设计，确保所有文件访问都经过认证和授权。

---

### 1.2 获取文件元数据

`GET /api/v1/files/{file_id}`

获取已上传文件的元数据信息。

#### 示例

```bash
curl -X GET "$BASE_URL/api/v1/files/file_abc123def456" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
{
  "file_id": "file_abc123def456",
  "filename": "meeting_audio.mp3",
  "content_type": "audio/mpeg",
  "size": 2048576,
  "created_at": "2025-10-03T05:30:00Z"
}
```

---

### 1.3 删除文件

`DELETE /api/v1/files/{file_id}`

删除已上传的文件。

#### 示例

```bash
curl -X DELETE "$BASE_URL/api/v1/files/file_abc123def456" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
{
  "message": "File 'file_abc123def456' deleted successfully",
  "deleted_count": 1
}
```

---

## 2. AI调用

### 2.1 发起AI调用

`POST /api/v1/invoke`

**核心AI服务调用接口**，支持文本生成、图片生成、语音转文字等多种AI任务。

#### 调用模式

- **同步模式**: 等待任务完成后返回结果
- **异步模式**: 立即返回任务ID，通过轮询查询结果
- **流式模式**: 实时流式返回生成内容（适用于文本生成）

#### 请求参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| task_type | string | 是 | 任务类型：`text_generation`（文本生成）、`image_generation`（图片生成）、`speech_to_text`（语音转文字）、`document_processing`（文档处理） |
| provider | string | **否** | AI服务提供商（如：`openai`、`dmxapi`、`anthropic`）。**省心模式：不指定时自动使用默认服务商**。专家模式：可明确指定服务商 |
| model | string | **否** | 模型名称（如：`gpt-4`、`gpt-4o-mini`、`gemini-2.5-flash-image`）。**省心模式：不指定时自动使用默认模型**。专家模式：可明确指定模型 |
| input | object | 是 | 输入数据，根据任务类型不同而不同 |
| config | object | 否 | 模型配置参数。**文本生成**：`temperature`、`max_tokens`等；**图片生成**：`size`（如`512x512`、`1024x1024`）；**语音识别**：`language`等 |
| stream | boolean | 否 | 是否启用流式响应，默认false（仅文本生成支持） |

> **💡 省心模式 vs 专家模式**
> - **省心模式**（推荐）：不指定 `provider` 和 `model` 参数，系统根据任务类型自动选择最合适的服务商和模型
> - **专家模式**：明确指定 `provider` 和/或 `model` 参数，适合对特定服务商或模型有要求的高级用户
>
> **默认配置**（可通过服务器.env文件调整）：
> - `text_generation` → `dmxapi` + `gpt-4o-mini`
> - `image_generation` → `dmxapi` + `gemini-2.5-flash-image`
> - `speech_to_text` → `dmxapi` + `whisper-1`（注：腾讯云ASR使用自己的引擎模型`16k_zh`）

#### 请求头

```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Prefer: respond-async  # 可选，启用异步模式
```

#### 示例1：文本生成（省心模式 - 推荐）

```bash
curl -X POST "$BASE_URL/api/v1/invoke" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "text_generation",
    "input": {
      "prompt": "写一首关于春天的诗"
    },
    "config": {
      "temperature": 0.7,
      "max_tokens": 500
    }
  }'
```

> **省心模式**：未指定 `provider` 和 `model`，系统自动使用默认的 `dmxapi` 服务商和 `gpt-4o-mini` 模型

**响应**:
```json
{
  "task_id": "task_abc123def456",
  "status": "completed",
  "output": {
    "text": "春风拂面暖阳天，\n嫩芽初绽展新颜...",
    "usage": {
      "prompt_tokens": 12,
      "completion_tokens": 85,
      "total_tokens": 97
    }
  }
}
```

#### 示例1-B：文本生成（专家模式）

```bash
curl -X POST "$BASE_URL/api/v1/invoke" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "text_generation",
    "provider": "openai",
    "model": "gpt-4",
    "input": {
      "prompt": "写一首关于春天的诗"
    },
    "config": {
      "temperature": 0.7,
      "max_tokens": 500
    }
  }'
```

> **专家模式**：明确指定 `provider: "openai"`，直接使用OpenAI服务

#### 示例2：图片生成（省心模式）

```bash
curl -X POST "$BASE_URL/api/v1/invoke" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "image_generation",
    "input": {
      "prompt": "未来城市的科幻场景，有飞行汽车和高楼大厦，霓虹灯光，赛博朋克风格"
    },
    "config": {
      "size": "1024x1024"
    }
  }'
```

> **省心模式**：未指定 `provider` 和 `model`，系统自动使用默认的 `dmxapi` 服务商和 `gemini-2.5-flash-image` 模型（图片生成强制异步处理）
>
> **图片尺寸**：通过 `config.size` 参数控制，支持自定义尺寸（如`512x512`、`1024x1024`、`1920x1080`等），默认 `1024x1024`

**响应**:
```json
{
  "task_id": "task_xyz789abc123",
  "status": "queued",
  "message": "Image generation task has been queued for processing",
  "status_poll_url": "/api/v1/tasks/task_xyz789abc123"
}
```

#### 示例3：语音转文字（使用file_id - 推荐）

**完整工作流**：先上传文件，再使用file_id进行ASR

```bash
# Step 1: 上传音频文件
FILE_RESPONSE=$(curl -X POST "$BASE_URL/api/v1/files" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@meeting.mp3")

# 提取file_id
FILE_ID=$(echo $FILE_RESPONSE | jq -r '.file_id')

# Step 2: 使用file_id进行语音识别（省心模式）
curl -X POST "$BASE_URL/api/v1/invoke" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"task_type\": \"speech_to_text\",
    \"input\": {
      \"file_id\": \"$FILE_ID\"
    },
    \"config\": {
      \"language\": \"zh\"
    }
  }"
```

> **统一架构**：使用 `file_id` 而非直接上传或提供URL，遵循平台的统一文件管理架构
> **省心模式**：自动使用默认的 `dmxapi` 语音识别服务

**响应**:
```json
{
  "task_id": "task_speech456",
  "status": "queued",
  "message": "Task has been queued for processing",
  "status_poll_url": "/api/v1/tasks/task_speech456"
}
```

> **注意**：语音识别任务通常为异步处理，使用返回的 `task_id` 查询结果

#### 示例4：流式文本生成（省心模式）

```bash
curl -X POST "$BASE_URL/api/v1/invoke" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "text_generation",
    "input": {
      "prompt": "详细解释什么是机器学习"
    },
    "stream": true
  }'
```

> **省心模式**：流式生成也支持省心模式，自动使用默认服务商和模型

**响应**（Server-Sent Events格式）:
```
Content-Type: text/event-stream

data: {"delta": {"content": "机器"}}

data: {"delta": {"content": "学习"}}

data: {"delta": {"content": "是"}}

data: {"delta": {"content": "人工智能"}}

data: [DONE]
```

#### 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 同步调用成功 |
| 202 | 异步任务已接受 |
| 400 | 请求参数错误 |
| 401 | 认证失败（API Key无效） |
| 403 | 权限不足 |
| 408 | 请求超时 |
| 429 | 超出速率限制 |
| 500 | 服务器内部错误 |
| 503 | 服务暂时不可用 |

---

### 1.2 查询任务状态

`GET /api/v1/tasks/{task_id}`

查询异步任务的执行状态和结果。

#### 路径参数

| 参数 | 类型 | 描述 |
|------|------|------|
| task_id | string | 任务ID（由invoke接口返回） |

#### 示例

```bash
curl -X GET "$BASE_URL/api/v1/tasks/task_xyz789abc123" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应（任务进行中）

```json
{
  "task_id": "task_xyz789abc123",
  "status": "running",
  "task_type": "image_generation",
  "created_at": "2025-01-02T10:00:00Z",
  "started_at": "2025-01-02T10:00:05Z",
  "progress": 50
}
```

#### 响应（任务已完成）

```json
{
  "task_id": "task_xyz789abc123",
  "status": "completed",
  "task_type": "image_generation",
  "created_at": "2025-01-02T10:00:00Z",
  "started_at": "2025-01-02T10:00:05Z",
  "finished_at": "2025-01-02T10:02:30Z",
  "output": {
    "image_url": "$BASE_URL/storage/images/generated-12345.png",
    "width": 1024,
    "height": 1024
  }
}
```

#### 响应（任务失败）

```json
{
  "task_id": "task_xyz789abc123",
  "status": "failed",
  "task_type": "image_generation",
  "created_at": "2025-01-02T10:00:00Z",
  "started_at": "2025-01-02T10:00:05Z",
  "finished_at": "2025-01-02T10:00:10Z",
  "error": {
    "code": "PROVIDER_ERROR",
    "message": "API quota exceeded for provider"
  }
}
```

#### 任务状态说明

| 状态 | 描述 |
|------|------|
| pending | 等待处理 |
| queued | 已排队 |
| running | 执行中 |
| completed | 已完成 |
| failed | 失败 |

---

## 3. 会话管理

会话管理功能让您可以构建具有上下文记忆的多轮对话应用，系统会自动维护对话历史。

### 4.1 创建会话

`POST /api/v1/sessions`

创建一个新的对话会话。

#### 请求参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| agent_type | string | 否 | 智能体类型，默认`assistant` |
| agent_config | object | 否 | 智能体配置（模型、temperature等） |
| name | string | 否 | 会话名称 |

#### 示例

```bash
curl -X POST "$BASE_URL/api/v1/sessions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "assistant",
    "agent_config": {
      "model": "gpt-4",
      "temperature": 0.7,
      "system_prompt": "你是一个专业的技术支持助手"
    },
    "name": "客户支持会话"
  }'
```

#### 响应

```json
{
  "session_id": "sess_abc123def456",
  "agent_type": "assistant",
  "agent_config": {
    "model": "gpt-4",
    "temperature": 0.7,
    "system_prompt": "你是一个专业的技术支持助手"
  },
  "is_active": true,
  "created_at": "2025-01-02T10:00:00Z"
}
```

---

### 3.2 在会话中调用AI

`POST /api/v1/sessions/{session_id}/invoke`

在指定会话的上下文中发送消息，系统会自动维护对话历史。

#### 路径参数

| 参数 | 类型 | 描述 |
|------|------|------|
| session_id | string | 会话ID |

#### 请求参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| prompt | string | 是 | 用户消息内容 |
| stream | boolean | 否 | 是否启用流式响应，默认false |
| config | object | 否 | 临时覆盖会话配置 |

#### 示例

```bash
curl -X POST "$BASE_URL/api/v1/sessions/sess_abc123def456/invoke" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "如何重置密码？",
    "stream": false
  }'
```

#### 响应

```json
{
  "session_id": "sess_abc123def456",
  "response": {
    "content": "重置密码的步骤如下：\n1. 访问登录页面\n2. 点击"忘记密码"链接\n3. 输入您的注册邮箱...",
    "role": "assistant"
  },
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 85,
    "total_tokens": 235
  }
}
```

---

### 3.3 获取会话历史

`GET /api/v1/sessions/{session_id}/history`

获取指定会话的完整对话历史。

#### 查询参数

| 参数 | 类型 | 描述 |
|------|------|------|
| limit | integer | 返回消息数量，默认20 |
| offset | integer | 偏移量，默认0 |

#### 示例

```bash
curl -X GET "$BASE_URL/api/v1/sessions/sess_abc123def456/history?limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
{
  "session_id": "sess_abc123def456",
  "messages": [
    {
      "role": "user",
      "content": "你好",
      "timestamp": "2025-01-02T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "你好！有什么可以帮助您的吗？",
      "timestamp": "2025-01-02T10:00:02Z"
    },
    {
      "role": "user",
      "content": "如何重置密码？",
      "timestamp": "2025-01-02T10:01:00Z"
    },
    {
      "role": "assistant",
      "content": "重置密码的步骤如下：\n1. 访问登录页面...",
      "timestamp": "2025-01-02T10:01:05Z"
    }
  ],
  "total": 4
}
```

---

### 3.4 获取会话列表

`GET /api/v1/sessions`

获取当前API Key创建的所有会话列表。

#### 查询参数

| 参数 | 类型 | 描述 |
|------|------|------|
| page | integer | 页码，默认1 |
| per_page | integer | 每页数量，默认20 |

#### 示例

```bash
curl -X GET "$BASE_URL/api/v1/sessions?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
{
  "sessions": [
    {
      "id": 1,
      "session_id": "sess_abc123def456",
      "agent_type": "assistant",
      "agent_config": {
        "model": "gpt-4",
        "temperature": 0.7
      },
      "name": "客户支持会话",
      "is_active": true,
      "created_at": "2025-01-02T10:00:00Z",
      "updated_at": "2025-01-02T10:30:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "per_page": 10,
  "pages": 2
}
```

---

### 3.5 获取会话详情

`GET /api/v1/sessions/{session_id}`

获取指定会话的配置信息和元数据。

#### 示例

```bash
curl -X GET "$BASE_URL/api/v1/sessions/sess_abc123def456" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
{
  "session_id": "sess_abc123def456",
  "agent_type": "assistant",
  "agent_config": {
    "model": "gpt-4",
    "temperature": 0.7,
    "system_prompt": "你是一个专业的技术支持助手"
  },
  "name": "客户支持会话",
  "is_active": true,
  "created_at": "2025-01-02T10:00:00Z",
  "updated_at": "2025-01-02T10:30:00Z",
  "message_count": 8
}
```

---

### 3.6 删除会话

`DELETE /api/v1/sessions/{session_id}`

永久删除指定会话及其所有历史记录。

#### 示例

```bash
curl -X DELETE "$BASE_URL/api/v1/sessions/sess_abc123def456" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```
HTTP/1.1 204 No Content
```

---

## 4. 知识库

知识库功能让您可以构建和管理私有知识库，并进行语义搜索，为RAG（检索增强生成）应用提供基础能力。

### 4.1 创建知识库

`POST /api/v1/knowledge-bases`

创建一个新的知识库。

#### 请求参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| name | string | 是 | 知识库名称 |
| description | string | 否 | 知识库描述 |
| embedding_model | string | 否 | 向量化模型，默认`BAAI/bge-base-zh-v1.5` |
| chunk_size | integer | 否 | 文档分块大小，默认1000 |
| chunk_overlap | integer | 否 | 分块重叠大小，默认200 |

#### 示例

```bash
curl -X POST "$BASE_URL/api/v1/knowledge-bases" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "公司内部文档库",
    "description": "包含公司政策、规章制度、流程文档等",
    "embedding_model": "BAAI/bge-base-zh-v1.5",
    "chunk_size": 800,
    "chunk_overlap": 150
  }'
```

#### 响应

```json
{
  "kb_id": "kb_xyz789abc123",
  "name": "公司内部文档库",
  "description": "包含公司政策、规章制度、流程文档等",
  "embedding_model": "BAAI/bge-base-zh-v1.5",
  "chunk_size": 800,
  "chunk_overlap": 150,
  "created_at": "2025-01-02T10:00:00Z",
  "document_count": 0
}
```

---

### 4.2 上传文档

`POST /api/v1/knowledge-bases/{kb_id}/documents`

上传文档到指定知识库进行向量化处理。

#### 路径参数

| 参数 | 类型 | 描述 |
|------|------|------|
| kb_id | string | 知识库ID |

#### 请求格式

`multipart/form-data`

| 字段 | 类型 | 描述 |
|------|------|------|
| file | file | 文档文件（支持PDF、TXT、MD格式，最大10MB） |

#### 示例

```bash
curl -X POST "$BASE_URL/api/v1/knowledge-bases/kb_xyz789abc123/documents" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@employee_handbook.pdf"
```

#### 响应

```json
{
  "task_id": "task_doc456789",
  "status": "queued",
  "message": "Document 'employee_handbook.pdf' has been queued for processing",
  "status_poll_url": "/api/v1/tasks/task_doc456789"
}
```

> **提示**: 文档处理是异步的，使用返回的`task_id`通过任务查询接口轮询处理状态。

---

### 4.3 获取文档列表

`GET /api/v1/knowledge-bases/{kb_id}/documents`

获取指定知识库中所有文档的列表和处理状态。

#### 示例

```bash
curl -X GET "$BASE_URL/api/v1/knowledge-bases/kb_xyz789abc123/documents" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
[
  {
    "doc_id": "doc_111222333",
    "filename": "employee_handbook.pdf",
    "file_type": "pdf",
    "file_size": 2048576,
    "processing_status": "completed",
    "chunk_count": 42,
    "uploaded_at": "2025-01-02T10:00:00Z",
    "processed_at": "2025-01-02T10:05:30Z",
    "content_preview": "第一章 公司简介\n本公司成立于..."
  },
  {
    "doc_id": "doc_444555666",
    "filename": "leave_policy.pdf",
    "file_type": "pdf",
    "file_size": 1024000,
    "processing_status": "processing",
    "chunk_count": 0,
    "uploaded_at": "2025-01-02T11:00:00Z"
  }
]
```

---

### 4.4 语义搜索

`POST /api/v1/knowledge-bases/search`

在一个或多个知识库中进行语义搜索，返回最相关的文档片段。

#### 请求参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| query | string | 是 | 搜索查询文本 |
| knowledge_base_ids | array | 是 | 要搜索的知识库ID列表 |
| top_k | integer | 否 | 返回结果数量，默认5 |
| similarity_threshold | float | 否 | 相似度阈值（0-1），默认0.7 |

#### 示例

```bash
curl -X POST "$BASE_URL/api/v1/knowledge-bases/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "员工请假需要提前多久申请？",
    "knowledge_base_ids": ["kb_xyz789abc123"],
    "top_k": 3,
    "similarity_threshold": 0.75
  }'
```

#### 响应

```json
{
  "query": "员工请假需要提前多久申请？",
  "results": [
    {
      "chunk_id": "chunk_aaa111",
      "doc_id": "doc_444555666",
      "kb_id": "kb_xyz789abc123",
      "content": "第五章 请假制度\n5.1 请假申请\n员工请假需提前3个工作日向直属主管提交书面申请...",
      "similarity_score": 0.89,
      "metadata": {
        "filename": "leave_policy.pdf",
        "page": 12,
        "chunk_index": 23
      }
    },
    {
      "chunk_id": "chunk_bbb222",
      "doc_id": "doc_444555666",
      "kb_id": "kb_xyz789abc123",
      "content": "5.2 紧急请假\n如遇突发情况，员工可以口头请假，但需在24小时内补交书面申请...",
      "similarity_score": 0.82,
      "metadata": {
        "filename": "leave_policy.pdf",
        "page": 13,
        "chunk_index": 24
      }
    }
  ],
  "total_results": 2
}
```

---

### 4.5 获取知识库列表

`GET /api/v1/knowledge-bases`

获取当前API Key创建的所有知识库列表。

#### 示例

```bash
curl -X GET "$BASE_URL/api/v1/knowledge-bases" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
[
  {
    "kb_id": "kb_xyz789abc123",
    "name": "公司内部文档库",
    "description": "包含公司政策、规章制度、流程文档等",
    "embedding_model": "BAAI/bge-base-zh-v1.5",
    "document_count": 15,
    "created_at": "2025-01-02T10:00:00Z",
    "updated_at": "2025-01-02T12:30:00Z"
  },
  {
    "kb_id": "kb_abc456def789",
    "name": "技术文档库",
    "description": "API文档、开发指南等",
    "embedding_model": "BAAI/bge-base-zh-v1.5",
    "document_count": 8,
    "created_at": "2025-01-01T15:00:00Z",
    "updated_at": "2025-01-01T18:20:00Z"
  }
]
```

---

### 4.6 获取知识库详情

`GET /api/v1/knowledge-bases/{kb_id}`

获取指定知识库的详细信息。

#### 示例

```bash
curl -X GET "$BASE_URL/api/v1/knowledge-bases/kb_xyz789abc123" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
{
  "kb_id": "kb_xyz789abc123",
  "name": "公司内部文档库",
  "description": "包含公司政策、规章制度、流程文档等",
  "embedding_model": "BAAI/bge-base-zh-v1.5",
  "chunk_size": 800,
  "chunk_overlap": 150,
  "document_count": 15,
  "total_chunks": 650,
  "created_at": "2025-01-02T10:00:00Z",
  "updated_at": "2025-01-02T12:30:00Z"
}
```

---

### 4.7 删除知识库

`DELETE /api/v1/knowledge-bases/{kb_id}`

删除指定知识库及其所有文档。

#### 示例

```bash
curl -X DELETE "$BASE_URL/api/v1/knowledge-bases/kb_xyz789abc123" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 响应

```json
{
  "message": "Knowledge base deleted successfully"
}
```

---

## 错误处理

所有API错误都遵循统一的错误响应格式：

```json
{
  "detail": "错误描述信息",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-01-02T10:00:00Z"
}
```

### 常见错误码

| HTTP状态码 | 错误码 | 描述 | 解决方法 |
|-----------|--------|------|----------|
| 400 | INVALID_REQUEST | 请求参数错误 | 检查请求参数格式和必填字段 |
| 401 | UNAUTHORIZED | 认证失败 | 检查API Key是否正确且有效 |
| 403 | FORBIDDEN | 权限不足 | 确认API Key具有所需权限 |
| 404 | NOT_FOUND | 资源不存在 | 检查资源ID是否正确 |
| 408 | TIMEOUT | 请求超时 | 尝试异步模式或联系支持团队 |
| 429 | RATE_LIMIT_EXCEEDED | 超出速率限制 | 降低请求频率或升级套餐 |
| 500 | INTERNAL_ERROR | 服务器内部错误 | 联系技术支持 |
| 503 | SERVICE_UNAVAILABLE | 服务暂时不可用 | 稍后重试或查看状态页面 |

---

## 速率限制

根据您的套餐，API调用有不同的速率限制：

| 套餐 | 每分钟请求数 | 每日请求数 |
|------|-------------|-----------|
| 免费版 | 60 | 1,000 |
| 基础版 | 300 | 10,000 |
| 专业版 | 1,000 | 100,000 |
| 企业版 | 自定义 | 自定义 |

超出速率限制时，API会返回HTTP 429错误，响应头中包含：

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704182400
```

---

## SDK支持

我们提供多种语言的官方SDK，让集成更加简单：

- **Python**: `pip install nexus-ai`
- **JavaScript/TypeScript**: `npm install @nexus-ai/sdk`
- **Java**: Maven/Gradle (即将推出)
- **Go**: `go get github.com/nexus-ai/go-sdk` (即将推出)

### Python SDK快速示例

```python
from nexus_ai import NexusAI

client = NexusAI(api_key="YOUR_API_KEY")

# 文本生成
response = client.invoke(
    task_type="text_generation",
    provider="openai",
    model="gpt-4",
    input={"prompt": "你好，介绍一下人工智能"},
    config={"temperature": 0.7}
)

print(response.output.text)

# 创建会话
session = client.sessions.create(
    agent_config={"model": "gpt-4"}
)

# 在会话中对话
response = session.send("你好")
print(response.content)
```

### JavaScript SDK快速示例

```javascript
import { NexusAI } from '@nexus-ai/sdk';

const client = new NexusAI({ apiKey: 'YOUR_API_KEY' });

// 文本生成
const response = await client.invoke({
  taskType: 'text_generation',
  provider: 'openai',
  model: 'gpt-4',
  input: { prompt: '你好，介绍一下人工智能' },
  config: { temperature: 0.7 }
});

console.log(response.output.text);

// 创建会话
const session = await client.sessions.create({
  agentConfig: { model: 'gpt-4' }
});

// 在会话中对话
const chatResponse = await session.send('你好');
console.log(chatResponse.content);
```

---

## 最佳实践

### 1. 使用异步模式处理长时间任务

对于图片生成、长音频转文字等耗时任务，建议使用异步模式：

```bash
# 1. 发起异步任务
curl -X POST "$BASE_URL/api/v1/invoke" \
  -H "Prefer: respond-async" \
  ...

# 2. 轮询任务状态
curl -X GET "$BASE_URL/api/v1/tasks/{task_id}" \
  ...
```

### 4. 使用流式模式改善用户体验

对于文本生成，使用流式响应可以让用户实时看到生成内容：

```python
response = client.invoke(
    task_type="text_generation",
    model="gpt-4",
    input={"prompt": "写一篇长文章"},
    stream=True
)

for chunk in response:
    print(chunk.delta.content, end='')
```

### 4. 利用会话管理构建对话应用

使用会话API可以自动维护对话历史，无需手动管理上下文：

```python
# 创建会话一次
session = client.sessions.create()

# 多轮对话
response1 = session.send("我的名字叫张三")
response2 = session.send("我叫什么名字？")  # AI会记住之前的对话
```

### 4. 知识库+AI调用实现RAG

结合知识库搜索和AI调用，构建基于私有数据的问答系统：

```python
# 1. 搜索相关知识
search_results = client.knowledge_bases.search(
    query="员工请假政策",
    kb_ids=["kb_xyz789"]
)

# 2. 将搜索结果作为上下文
context = "\n".join([r.content for r in search_results.results])
prompt = f"基于以下信息回答问题：\n{context}\n\n问题：{user_question}"

# 3. 调用AI生成回答
response = client.invoke(
    task_type="text_generation",
    model="gpt-4",
    input={"prompt": prompt}
)
```

### 5. 妥善保管API密钥

- ❌ 不要将API Key硬编码在代码中
- ❌ 不要将API Key提交到Git仓库
- ✅ 使用环境变量存储API Key
- ✅ 使用不同的API Key区分开发/生产环境
- ✅ 定期轮换API Key

---

## 故障排除

### 常见问题

#### Q1: 为什么一直返回 401 Unauthorized？

**可能原因**:
1. 请求头中缺少 `Authorization` 字段
2. API Key 格式错误
3. API Key 已过期或被禁用

**解决方法**:
```bash
# 检查请求头是否正确
curl -X GET "$BASE_URL/api/v1/sessions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -v  # 使用 -v 查看详细的请求头信息
```

确保:
- ✅ Header 名称是 `Authorization`（注意大小写）
- ✅ Value 格式是 `Bearer YOUR_API_KEY`（Bearer 后面有一个空格）
- ✅ API Key 以 `nxs_` 开头

#### Q2: 如何查看请求是否发送成功？

使用 `-v` 参数查看详细信息：

```bash
curl -X POST "$BASE_URL/api/v1/invoke" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_type":"text_generation",...}' \
  -v
```

关注输出中的：
- `> Authorization: Bearer nxs_xxx` - 确认 Header 发送正确
- `< HTTP/1.1 200 OK` - 确认服务器响应状态

#### Q3: 速率限制是多少？

每个 API Key 都有独立的速率限制，默认为每分钟 60 次请求。

超出限制时会返回：
```json
{
  "detail": "Rate limit exceeded",
  "retry_after": 30
}
```

解决方法：
- 在代码中实现指数退避重试
- 联系管理员提升配额
- 使用多个 API Key 分散负载

#### Q4: 如何测试 API 是否正常工作？

最简单的测试方法：

```bash
# 1. 测试服务是否在线
curl "$BASE_URL/health"

# 应该返回: {"status":"healthy"}

# 2. 测试认证是否正确
curl "$BASE_URL/api/v1/sessions" \
  -H "Authorization: Bearer YOUR_API_KEY"

# 应该返回: {"sessions":[],...} 而不是 401 错误
```

#### Q5: 支持哪些编程语言？

Nexus AI 提供标准的 RESTful API，支持所有可以发送 HTTP 请求的编程语言：

- Python (推荐使用 `requests` 库)
- JavaScript/Node.js (推荐使用 `axios` 或 `fetch`)
- Java (推荐使用 `OkHttp` 或 `Apache HttpClient`)
- Go (使用标准库 `net/http`)
- PHP (使用 `cURL` 或 `Guzzle`)
- Ruby (使用 `net/http` 或 `httparty`)

### 错误码参考

| HTTP 状态码 | 含义 | 常见原因 |
|-----------|------|---------|
| 200 | 成功 | 请求已成功处理 |
| 201 | 已创建 | 资源创建成功（如创建会话） |
| 202 | 已接受 | 异步任务已接受，返回 task_id |
| 400 | 请求错误 | 请求参数格式错误或缺少必需参数 |
| 401 | 未授权 | 缺少或无效的 API Key |
| 403 | 禁止访问 | API Key 权限不足 |
| 404 | 未找到 | 请求的资源不存在 |
| 429 | 请求过多 | 超过速率限制 |
| 500 | 服务器错误 | 服务器内部错误 |
| 503 | 服务不可用 | 服务暂时不可用或正在维护 |

### 调试技巧

1. **使用 Postman 测试**
   - 导入我们提供的 Postman Collection
   - 可视化地测试和调试 API

2. **查看响应头**
   ```bash
   curl -I "$BASE_URL/api/v1/sessions" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

3. **保存请求日志**
   ```bash
   curl "$BASE_URL/api/v1/invoke" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -d '...' \
     --trace-ascii debug.log
   ```

4. **使用 JSON 工具格式化输出**
   ```bash
   # 使用 jq 格式化 JSON 响应
   curl "$BASE_URL/api/v1/sessions" \
     -H "Authorization: Bearer YOUR_API_KEY" | jq
   ```

---

## 获取帮助

- **文档中心**: https://nexus-ai.juncai-ai.com/docs
- **API状态**: https://nexus-ai.juncai-ai.com/status
- **技术支持**: support@nexus-ai.com
- **开发者社区**: https://nexus-ai.juncai-ai.com/community

---

**版权所有 © 2025 Nexus AI. 保留所有权利。**
