# 邮件草稿：通知应用开发团队

---

**收件人**: 应用开发团队
**主题**: 🎉 Nexus AI Python SDK v0.1.0 已发布到TestPyPI - 可以开始集成了！

---

Hi 团队，

好消息！**Nexus AI Python SDK v0.1.0 (Alpha)** 已经成功发布到 TestPyPI，你们现在可以开始集成开发了！

## 📦 快速安装

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nexus-ai-sdk
```

**验证安装**:
```bash
python -c "from nexusai import NexusAIClient; print('✓ SDK安装成功！')"
```

## 🚀 快速开始

### 1. 创建 `.env` 配置文件

```bash
NEXUS_API_KEY=nxs_your_api_key_here
NEXUS_BASE_URL=http://localhost:8000/api/v1
```

### 2. 编写第一个示例

```python
from nexusai import NexusAIClient

# 初始化客户端
client = NexusAIClient()

# 文本生成
response = client.text.generate("你好，请介绍一下自己")
print(response.text)

# 图像生成
image = client.images.generate("一只可爱的猫咪，卡通风格")
print(f"图像URL: {image.image_url}")

# 会话对话
session = client.sessions.create(name="客服对话")
response = session.invoke("我想了解产品信息")
print(response.response.content)
```

## 📚 完整文档

详细的安装和使用指南请查看附件：

**必读文档**:
1. **APP_DEV_INSTALL_GUIDE.md** ⭐ - 完整的安装和使用指南
2. **TESTPYPI_PUBLISHED.md** - 发布公告和快速参考
3. **README.md** - SDK完整文档

或访问 TestPyPI 项目主页：
https://test.pypi.org/project/nexus-ai-sdk/0.1.0/

## ✨ 核心功能

SDK已实现以下功能，都可以立即使用：

- ✅ **文本生成** - 同步、异步、流式三种模式
  ```python
  # 同步
  response = client.text.generate("写一首诗")

  # 流式
  for chunk in client.text.stream("讲个故事"):
      print(chunk["delta"].get("content", ""), end="")
  ```

- ✅ **图像生成** - 自动任务轮询
  ```python
  image = client.images.generate("未来城市，赛博朋克风格")
  ```

- ✅ **会话管理** - 多轮对话，自动记忆上下文
  ```python
  session = client.sessions.create(name="客服")
  session.invoke("我叫张三")
  session.invoke("我叫什么名字？")  # 会记住"张三"
  ```

- ✅ **文件上传** - 统一文件管理
  ```python
  file_meta = client.files.upload("document.pdf")
  ```

- ✅ **音频处理** - ASR语音转文字、TTS文字转语音
  ```python
  # 语音转文字
  transcription = client.audio.transcribe(file_id=file_id, language="zh")

  # 文字转语音
  task = client.audio.tts(text="你好世界", voice="alloy")
  ```

- ✅ **知识库** - RAG检索增强生成
  ```python
  # 创建知识库
  kb = client.knowledge_bases.create(name="公司文档")

  # 上传文档
  task = client.knowledge_bases.upload_document(kb.kb_id, "policy.pdf")

  # 搜索
  results = client.knowledge_bases.search(
      query="年假政策是什么？",
      knowledge_base_ids=[kb.kb_id]
  )
  ```

## ⚠️ Alpha 版本说明

**当前状态**:
- ✅ SDK核心功能完整实现
- ✅ 41个单元测试通过
- ✅ 8个功能测试通过
- ⏳ 后端API部分端点待完成

**已知情况**:
- 部分API端点可能返回连接错误（后端开发中，这是正常的）
- 你们可以先使用mock数据测试集成逻辑
- 等后端API ready后，无需修改代码，直接连接即可

**向后兼容保证**:
- SDK接口已经稳定
- 后续版本（v0.2.0, v1.0.0）保持向后兼容
- 你们现在编写的代码不需要修改

## 🔄 环境切换

**开发环境**（当前默认）:
```bash
NEXUS_BASE_URL=http://localhost:8000/api/v1
```

**生产环境**（未来一键切换）:
```bash
NEXUS_BASE_URL=https://nexus-ai.juncai-ai.com/api/v1
```

只需修改环境变量，代码无需任何改动！

## 🆘 遇到问题？

**安装问题**:
- 确保同时指定 `--index-url` 和 `--extra-index-url`
- 查看 APP_DEV_INSTALL_GUIDE.md 的"遇到问题"章节

**使用问题**:
- API连接失败 → 检查后端服务是否启动
- 导入错误 → 验证安装：`python -c "from nexusai import NexusAIClient"`
- 其他问题 → 查看完整文档或联系SDK团队

**反馈渠道**:
- 📧 Email: [你的邮箱]
- 💬 群组: [开发团队群聊]
- 🐛 提Issue: [如果有GitHub]

## 🎯 建议的开发流程

1. **本周**:
   - 安装SDK
   - 阅读文档
   - 运行示例代码
   - 设计应用架构

2. **下周**:
   - 开始编写应用代码
   - 使用mock数据测试
   - 准备真实API对接

3. **API ready后**:
   - 切换到真实API
   - 集成测试
   - 提供反馈

## 📊 SDK特性亮点

- 🔐 **类型安全** - 完整的类型提示，IDE自动补全友好
- 🏠 **开发友好** - 默认localhost，零配置即可开发
- ⚡ **异步支持** - 自动处理长时间任务（图像生成等）
- 📡 **流式输出** - 支持实时流式文本生成
- 🎯 **错误清晰** - 9种专门的异常类型，便于调试
- 🔄 **环境切换** - 一个环境变量搞定开发/生产切换

## 📝 附件清单

请查看邮件附件或项目文档目录：

1. APP_DEV_INSTALL_GUIDE.md - 应用开发团队安装指南（必读）
2. TESTPYPI_PUBLISHED.md - TestPyPI发布公告
3. README.md - SDK完整文档
4. CHANGELOG.md - 版本变更历史
5. examples/basic_usage.py - 基础用法示例代码

## 🎉 期待你们的反馈！

这是我们第一个Alpha版本，非常期待听到你们的反馈：

- ✨ 哪些功能好用？
- 😕 哪些地方不符合预期？
- 💡 需要哪些新功能？
- 📝 文档哪里需要改进？

你们的反馈将帮助我们打造更好的SDK！

---

**祝开发顺利！** 🚀

SDK开发团队
2025-10-03

---

**快速链接**:
- TestPyPI项目: https://test.pypi.org/project/nexus-ai-sdk/0.1.0/
- 安装命令: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nexus-ai-sdk`

---

**P.S.**: 如有任何问题，随时联系我们！我们会在24小时内响应。
