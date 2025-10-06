# SDK错误处理快速参考指南

**目标读者**: 后端团队
**SDK版本**: 0.2.0
**更新日期**: 2025-10-04

---

## 📊 当前测试状态

### 测试成功率: **76.7%** (46/60)

### 失败分类统计

| 分类 | 数量 | 占比 | 优先级 |
|------|------|------|--------|
| 🔴 后端Bug | 6个 | 42.9% | **P0 - 立即修复** |
| 🟡 后端配置 | 3个 | 21.4% | **P1 - 需要配置** |
| 🔵 功能未实现 | 3个 | 21.4% | P2 - 未来考虑 |
| ⚪ 第三方服务 | 1个 | 7.1% | 等待恢复 |
| 🟢 SDK环境 | 1个 | 7.1% | SDK已修复 |

---

## 🔴 P0 - 立即修复 (预计+8项测试, 4小时)

### 1. ASR文件生命周期Bug
**影响测试**: TEST 43-44
**错误**: `Failed to read file from local storage: No such file or directory`
**原因**: 文件上传到COS后立即删除本地文件，ASR任务无法读取

**SDK错误处理**:
```python
try:
    file_obj = client.files.upload(file=("audio.mp3", data, "audio/mpeg"))
    response = client.invoke(...)  # ASR task
except APIError as e:
    # SDK正确捕获并显示错误
    # status_code: 500
    # error_code: AI_SERVICE_ERROR
    # message: "Failed to read file from local storage: [Errno 2] ..."
```

**修复建议**:
```python
# 选项A: 延迟删除本地文件
def upload_file(...):
    save_to_local(file_data, local_path)
    cos_url = upload_to_cos(local_path)
    # os.remove(local_path)  # ❌ 注释掉，等任务完成后删除

# 选项B: 从COS读取文件
def process_asr(file_id):
    file_meta = get_file_metadata(file_id)
    audio_data = download_from_cos(file_meta["cos_url"])  # ✅ 从COS读取
```

**修复位置**: `file_service.py`, `llm_gateway.py`

---

### 2. Session History未保存
**影响测试**: TEST 31
**错误**: 断言失败 - History返回空列表
**原因**: Session invoke后未保存消息到session.messages

**SDK错误处理**:
```python
session = client.sessions.create()
session.invoke(input={"prompt": "Hello"})
history = session.get_history()

# SDK正确解析响应，但后端返回空列表
assert len(history.messages) > 0  # ❌ FAIL
```

**修复建议**:
```python
def session_invoke(session_id, input_data):
    session = get_session(session_id)

    # ✅ 保存用户消息
    session.messages.append({
        "role": "user",
        "content": input_data["prompt"]
    })

    # 调用LLM...

    # ✅ 保存助手消息
    session.messages.append({
        "role": "assistant",
        "content": llm_response.text
    })

    save_session(session)
```

**修复位置**: `session_service.py`

---

### 3. 文件列表未保存元数据
**影响测试**: TEST 51
**错误**: 断言失败 - Files.list()返回空列表
**原因**: 文件上传后未保存到全局存储

**SDK错误处理**:
```python
file1 = client.files.upload(...)
file2 = client.files.upload(...)
files = client.files.list()

# SDK正确解析响应，但后端返回空列表
assert len(files.files) >= 2  # ❌ FAIL
```

**修复建议**:
```python
def upload_file(file_data, filename):
    file_id = generate_file_id()
    file_metadata = {...}

    # ✅ 保存到全局存储
    uploaded_files[file_id] = file_metadata
    # 或保存到数据库
    db.files.insert(file_metadata)

    return file_metadata
```

**修复位置**: `file_service.py`

---

### 4. max_tokens参数未传递
**影响测试**: TEST 2
**错误**: 断言失败 - 返回23个token，请求5个token
**原因**: config中获取了max_tokens，但未传递给LLM

**SDK错误处理**:
```python
response = client.invoke(
    task_type="text_generation",
    input={"prompt": "Say hello"},
    config={"max_tokens": 5}
)

# SDK正确接收响应，但token数量不符合请求
assert response.usage.completion_tokens <= 5  # ❌ FAIL (返回23)
```

**修复建议**:
```python
def text_generation(input_data, config):
    llm_response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=config.get("max_tokens", 1000),  # ✅ 传递参数
        temperature=config.get("temperature", 0.7)
    )
```

**修复位置**: `llm_gateway.py`

---

### 5. 流式响应文本为空
**影响测试**: TEST 23
**错误**: 断言失败 - 收集到的文本长度为0
**原因**: SSE流中所有chunk的delta.content都为空字符串

**SDK错误处理**:
```python
collected_text = ""
for chunk in client.invoke_stream(...):
    delta = chunk.delta.content
    if delta:
        collected_text += delta

# SDK正确解析SSE，但所有delta都是空字符串
assert len(collected_text) > 0  # ❌ FAIL
```

**修复建议**:
```python
async def generate_stream():
    for chunk in llm_stream:
        # 检查delta提取逻辑
        delta_content = chunk.choices[0].delta.content

        # 调试输出
        logger.debug(f"LLM chunk: {chunk}")
        logger.debug(f"Delta content: '{delta_content}'")

        if delta_content:  # 只发送非空内容
            yield f"data: {json.dumps({'chunk': {'delta': {'content': delta_content}}})}\n\n"
```

**修复位置**: `llm_gateway.py` (SSE生成逻辑)

---

## 🟡 P1 - 配置问题 (预计+3项测试, 4小时)

### 1. OpenAI API密钥未配置
**影响测试**: TEST 5
**错误**: `OpenAI API error: 401 Unauthorized`

**SDK错误处理**:
```python
try:
    response = client.invoke(
        task_type="text_generation",
        config={"provider": "openai"}
    )
except ServerError as e:
    # SDK正确捕获并显示
    # status_code: 500
    # error_code: AI_SERVICE_ERROR
    # message: "OpenAI API error: Client error '401 Unauthorized'..."
```

**修复建议**:
```bash
# 配置环境变量
export OPENAI_API_KEY="sk-..."

# 或在.env文件中
OPENAI_API_KEY=sk-...
```

---

### 2. Tencent COS存储未配置
**影响测试**: TEST 38, 42
**错误**: `Unsupported storage provider: tencent_cos`

**SDK错误处理**:
```python
try:
    results = client.knowledge_bases.search(kb_id="xxx", query="test")
except NotFoundError as e:
    # SDK正确捕获并显示
    # status_code: 404
    # error_code: NOT_FOUND
    # message: "Unsupported storage provider: tencent_cos"
```

**修复建议**:
```python
# 1. 实现TencentCOSProvider类
# 2. 注册到STORAGE_PROVIDERS
STORAGE_PROVIDERS = {
    "local": LocalStorageProvider,
    "tencent_cos": TencentCOSProvider,  # ✅ 添加
}

# 3. 配置环境变量
TENCENT_COS_SECRET_ID=...
TENCENT_COS_SECRET_KEY=...
TENCENT_COS_REGION=...
TENCENT_COS_BUCKET=...
```

---

## 🔵 P2 - 功能未实现 (未来考虑)

### 1. TTS功能未实现
**影响测试**: TEST 45-46
**状态**: 功能范围外，不是Bug

**SDK错误处理**:
```python
try:
    response = client.invoke(task_type="text_to_speech", ...)
except ValidationError as e:
    # SDK正确捕获
    # status_code: 422
    # error_code: VALIDATION_ERROR
    # validation_errors: [{"loc": ["body", "task_type"], "msg": "String should match pattern..."}]
```

---

### 2. JSON文件类型不支持
**影响测试**: TEST 52
**状态**: 设计限制，不是Bug

**SDK错误处理**:
```python
try:
    file_obj = client.files.upload(file=("data.json", ...))
except InvalidRequestError as e:
    # SDK正确捕获
    # status_code: 400
    # error_code: INVALID_REQUEST
    # message: "Unsupported file type '.json'. Allowed types: .mp3, .wav, ..."
```

---

## ⚪ 第三方服务问题

### DMXAPI 503服务不可用
**影响测试**: TEST 24 (Image Generation)
**状态**: 等待DMXAPI服务恢复

**SDK错误处理**:
```python
try:
    response = client.invoke(task_type="image_generation", ...)
except APIError as e:
    # SDK正确捕获
    # status_code: 500
    # error_code: AI_SERVICE_ERROR
    # message: "DMXAPI image generation error: Server error '503 Service Unavailable'..."
```

**注意**: 后端团队建议使用安全、描述性的prompt测试图片功能
- ✅ 推荐: "beautiful landscape", "modern office", "blue sky"
- ❌ 避免: "test", "cat", 简单单词

---

## 🟢 SDK环境问题

### Unicode输出编码错误
**影响测试**: TEST 60
**状态**: SDK测试脚本已修复

**原因**: Windows终端默认GBK编码，无法显示emoji

**SDK修复**:
```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

---

## 📊 修复路线图

```
当前: 76.7% (46/60)
  ↓ [修复P0] 预计4小时
第一阶段: 90.0% (54/60)
  ↓ [修复P1] 预计4小时
目标达成: 95.0% (57/60)
```

### 修复收益分析

| 修复项 | 时间 | 测试增加 | 成功率提升 |
|--------|------|----------|-----------|
| ASR文件生命周期 | 2h | +2 | +3.3% |
| Session History | 1h | +1 | +1.7% |
| 文件列表元数据 | 1h | +1 | +1.7% |
| max_tokens参数 | 30m | +1 | +1.7% |
| 流式文本为空 | 1h | +1 | +1.7% |
| **P0小计** | **5.5h** | **+6** | **+10.0%** |
| OpenAI配置 | 10m | +1 | +1.7% |
| COS配置 | 4h | +2 | +3.3% |
| **P1小计** | **4h** | **+3** | **+5.0%** |
| **总计** | **9.5h** | **+9** | **+15.0%** |

---

## 📋 SDK错误处理能力总结

### ✅ SDK已经能正确处理的错误

1. **所有HTTP错误码** - 映射到专用异常类
2. **后端错误代码** - 准确提取error.code和error.message
3. **验证错误** - 提供字段级错误详情
4. **第三方API错误** - 完整传递OpenAI、DMXAPI错误信息
5. **网络错误** - 连接失败、超时等
6. **文件上传错误** - 文件类型、大小限制等

### 🔧 SDK改进建议

1. **客户端验证** - 在请求前验证task_type、文件类型
2. **可重试标记** - 为503、502等错误添加is_retryable属性
3. **常量暴露** - 提供SUPPORTED_FILE_TYPES等常量
4. **错误恢复建议** - 在异常消息中提供修复建议

---

## 🎯 后端团队下一步行动

### 立即行动 (今天完成)

1. ✅ **修复ASR文件生命周期** - 选择方案A或B实现
2. ✅ **修复Session History保存** - 在invoke时保存消息
3. ✅ **修复文件列表保存** - 在upload时保存元数据
4. ✅ **修复max_tokens传递** - 传递给LLM API

### 短期行动 (本周完成)

5. ✅ **配置OpenAI API密钥** - 或明确告知用户未配置
6. ✅ **配置Tencent COS** - 或实现Provider类
7. ✅ **调查流式文本为空** - 检查LLM提供商返回

### 验证步骤

修复完成后，运行SDK完整测试套件：
```bash
python test_comprehensive_invoke.py
```

预期结果: **≥90%** (54/60)

---

## 📝 Image Width/Height测试准备

后端团队已修复width/height代码逻辑（`llm_gateway.py:530-558`），等待验证。

### SDK测试脚本已准备好

文件: `test_image_width_height.py`

测试用例（遵循后端建议）:
```python
# ✅ 使用安全、描述性的prompt
test_cases = [
    {
        "prompt": "beautiful mountain landscape at sunset with golden light",
        "size": "1024x1024",
        "expected": 1024x1024
    },
    {
        "prompt": "modern office workspace with natural lighting and plants",
        "size": "1664x936",
        "expected": 1664x1664
    },
    {
        "prompt": "clear blue sky with white fluffy clouds on a sunny day",
        "size": "1024x1792",
        "expected": 1024x1792
    }
]
```

### 运行命令

```bash
# 确保后端服务运行
docker-compose up -d

# 运行width/height测试
python test_image_width_height.py
```

### 预期结果

如果后端width/height解析正确：
```
✅ PASS - Dimensions correct!
  Expected: 1024x1024
  Actual:   1024x1024
```

如果DMXAPI 503:
```
⚠️  DMXAPI service unavailable (503)
This is a temporary third-party service issue, not a bug
```

---

**文档版本**: 1.0
**维护者**: SDK团队
**完整文档**: 见 `SDK_ERROR_HANDLING_DOCUMENTATION.md`
