# Nexus AI SDK v0.1.0 Alpha - 应用开发团队安装指南

## 📦 概述

Nexus AI Python SDK v0.1.0 (Alpha) 已发布到 **TestPyPI**，供应用开发团队进行集成测试。

**版本**: 0.1.0 (Alpha)
**状态**: 开发测试版，API集成待验证
**发布地址**: https://test.pypi.org/project/nexus-ai-sdk/

---

## 🚀 快速开始

### 方法1：使用 TestPyPI 安装（推荐用于测试）

```bash
# 创建虚拟环境
python -m venv myproject_env
myproject_env\Scripts\activate  # Windows
# source myproject_env/bin/activate  # Linux/Mac

# 从 TestPyPI 安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nexus-ai-sdk

# 验证安装
python -c "from nexusai import NexusAIClient; print('✓ SDK installed successfully')"
```

**重要说明**:
- `--index-url https://test.pypi.org/simple/` - 从 TestPyPI 获取 SDK
- `--extra-index-url https://pypi.org/simple` - 从正式 PyPI 获取依赖包（httpx、pydantic等）

### 方法2：配置 pip 使用 TestPyPI（可选）

如果需要频繁安装/更新，可以配置 pip：

**Windows**: 创建 `%APPDATA%\pip\pip.ini`
```ini
[global]
index-url = https://test.pypi.org/simple/
extra-index-url = https://pypi.org/simple
```

**Linux/Mac**: 创建 `~/.config/pip/pip.conf`
```ini
[global]
index-url = https://test.pypi.org/simple/
extra-index-url = https://pypi.org/simple
```

然后直接安装：
```bash
pip install nexus-ai-sdk
```

---

## ⚙️ 配置

### 1. 创建 `.env` 文件

在你的项目根目录创建 `.env` 文件：

```bash
# API认证（必需）
NEXUS_API_KEY=nxs_your_api_key_here

# API地址（开发环境 - 默认）
NEXUS_BASE_URL=http://localhost:8000/api/v1

# 超时配置（可选）
NEXUS_TIMEOUT=30
NEXUS_MAX_RETRIES=3
```

**重要**: 当前 SDK 默认连接 `http://localhost:8000/api/v1`，适合本地开发测试。

### 2. 初始化客户端

```python
from nexusai import NexusAIClient

# 方式1：从环境变量自动读取配置
client = NexusAIClient()

# 方式2：显式传递参数
client = NexusAIClient(
    api_key="nxs_your_api_key",
    base_url="http://localhost:8000/api/v1"
)
```

---

## 💡 基础用法示例

### 文本生成

```python
from nexusai import NexusAIClient

client = NexusAIClient()

# 简单调用
response = client.text.generate(prompt="你好，请介绍一下自己")
print(response.text)
print(f"使用 token: {response.usage.total_tokens}")

# 流式输出
for chunk in client.text.stream(prompt="讲个笑话"):
    if "delta" in chunk:
        print(chunk["delta"].get("content", ""), end="", flush=True)
```

### 会话管理

```python
# 创建会话
session = client.sessions.create(
    name="客服对话",
    agent_config={"temperature": 0.7}
)

# 多轮对话
response1 = session.invoke("我叫张三")
print(response1.response.content)

response2 = session.invoke("我叫什么？")
print(response2.response.content)  # 记住了 "张三"

# 清理
session.delete()
```

### 图像生成

```python
# 生成图像（异步任务，自动轮询）
image = client.images.generate(
    prompt="一只可爱的猫咪，卡通风格",
    size="1024x1024"
)
print(f"图像URL: {image.image_url}")
```

### 文件上传

```python
# 上传文件
file_meta = client.files.upload("document.pdf")
print(f"文件ID: {file_meta.file_id}")

# 使用文件进行语音转文字
transcription = client.audio.transcribe(
    file_id=file_meta.file_id,
    language="zh"
)
print(transcription.text)
```

---

## 🔧 开发环境 vs 生产环境

### 当前阶段（开发）

```python
# 连接本地API服务（默认）
client = NexusAIClient()  # 自动使用 localhost:8000
```

### 切换到生产环境（未来）

只需修改环境变量：

```bash
# .env 文件
NEXUS_BASE_URL=https://nexus-ai.juncai-ai.com/api/v1
```

或代码中修改：

```python
client = NexusAIClient(
    base_url="https://nexus-ai.juncai-ai.com/api/v1"
)
```

**一键切换，无需改代码！**

---

## 📋 完整示例代码

参考 SDK 中的示例文件：

```bash
# 查看基础用法
python examples/basic_usage.py
```

或查看项目中的示例：
- `examples/basic_usage.py` - 核心功能演示
- `README.md` - 完整文档和更多示例

---

## ⚠️ Alpha 版本注意事项

### 当前状态
- ✅ SDK 核心功能完整实现
- ✅ 41个单元测试通过（使用 mock）
- ⏳ 真实 API 集成测试待进行（等待后端 API 完成）

### 已知限制
1. **API未完全上线**: 部分端点可能返回连接错误，这是正常的
2. **错误信息**: 某些边缘情况的错误提示可能不够友好
3. **性能**: 未进行生产环境性能优化

### 如何报告问题

如果遇到问题，请提供：
1. **错误信息**: 完整的错误堆栈
2. **复现步骤**: 最小化的示例代码
3. **环境信息**: Python版本、操作系统
4. **SDK版本**: `pip show nexus-ai-sdk`

发送到: [SDK开发团队邮箱或Issue tracker]

---

## 🔄 更新到最新版本

```bash
# 从 TestPyPI 更新
pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nexus-ai-sdk

# 查看当前版本
pip show nexus-ai-sdk
```

---

## 📚 更多资源

- **完整文档**: 查看项目根目录 `README.md`
- **API参考**: `docs/api_reference.md`（如果有）
- **更新日志**: `CHANGELOG.md`
- **测试报告**: `TEST_REPORT.md`

---

## 🤝 团队协作

### SDK 团队的承诺
- 🐛 **快速修复**: 发现的 bug 将在24小时内响应
- 📈 **持续更新**: 每周同步 API 更新
- 📖 **文档完善**: 根据反馈持续改进文档

### 应用团队的反馈
请告诉我们：
- ✨ 哪些功能好用
- 😕 哪些地方不符合预期
- 💡 需要哪些新功能
- 📝 文档哪里需要改进

---

## 🎯 下一步

1. **安装 SDK**: 按照上面的步骤安装
2. **运行示例**: 试试 `examples/basic_usage.py`
3. **集成到应用**: 开始在你的应用中使用
4. **提供反馈**: 遇到问题随时联系 SDK 团队

**祝开发顺利！** 🚀

---

**版本**: v0.1.0 (Alpha)
**发布日期**: 2025-01-03
**维护**: Nexus AI SDK Team
