# Nexus AI SDK - 测试指南

## 📋 测试前准备

### 1. 项目结构验证 ✅

所有必需文件已创建完成：

```bash
cd c:\Users\junsh\Documents\GitHub\nexus-ai-sdk
bash verify_structure.sh
```

**结果**: ✅ 18个Python文件，所有配置文件就绪

### 2. 环境配置验证 ✅

- ✅ API Key 已配置: `nxs_4K5rIBmsp4wNszg_BuZ-Kih4gLLbx41dGxwNk_mkfaw`
- ✅ 默认 base_url: `http://localhost:8000/api/v1`
- ✅ `.env` 文件已创建

## 🧪 测试步骤

### 步骤 1: 检查依赖

```bash
python check_dependencies.py
```

**预期输出**:
```
✓ httpx 0.x.x
✓ pydantic 2.x.x
✓ python-dotenv (imported as dotenv)
✓ All dependencies installed!
```

**如果缺少依赖**，运行：
```bash
pip install httpx>=0.25.0 pydantic>=2.5.0 python-dotenv>=1.0.0
```

### 步骤 2: 测试导入

有三种方式测试导入：

#### 方式 A: 快速测试脚本（推荐）

```bash
python quick_test.py
```

**预期输出**:
```
============================================================
NEXUS AI SDK - Import Test
============================================================

[1/6] Testing: import nexusai
     ✓ SUCCESS
     Version: 0.1.0

[2/6] Testing: from nexusai import NexusAIClient
     ✓ SUCCESS

[3/6] Testing: from nexusai import config
     ✓ SUCCESS
     Default base_url: http://localhost:8000/api/v1

[4/6] Testing: from nexusai import error
     ✓ SUCCESS
     Available exceptions: 9/9

[5/6] Testing: Initialize NexusAIClient
     ✓ SUCCESS
     Client initialized

[6/6] Testing: Client resource properties
     ✓ client.images: True
     ✓ client.text: True
     ✓ client.sessions: True
     ✓ client.files: True
     ✓ client.audio: True
     ✓ client.knowledge_bases: True
     ✓ SUCCESS

============================================================
✓ ALL IMPORT TESTS PASSED!
============================================================
```

#### 方式 B: 详细测试脚本

```bash
python test_import.py
```

#### 方式 C: Python REPL 交互式测试

```bash
python
```

然后逐行执行：

```python
import sys
sys.path.insert(0, '.')

# 测试基础导入
import nexusai
print(f"Version: {nexusai.__version__}")  # 应该显示 0.1.0

# 测试客户端导入
from nexusai import NexusAIClient
print("NexusAIClient imported successfully")

# 测试配置
from nexusai import config
print(f"Base URL: {config.base_url}")  # 应该显示 http://localhost:8000/api/v1

# 测试错误模块
from nexusai import error
print(f"Has AuthenticationError: {hasattr(error, 'AuthenticationError')}")

# 初始化客户端（需要先设置API key）
import os
os.environ['NEXUS_API_KEY'] = 'nxs_4K5rIBmsp4wNszg_BuZ-Kih4gLLbx41dGxwNk_mkfaw'
client = NexusAIClient()
print("Client initialized!")

# 检查资源模块
print(f"Has images: {hasattr(client, 'images')}")
print(f"Has text: {hasattr(client, 'text')}")
print(f"Has sessions: {hasattr(client, 'sessions')}")
print(f"Has files: {hasattr(client, 'files')}")
print(f"Has audio: {hasattr(client, 'audio')}")
print(f"Has knowledge_bases: {hasattr(client, 'knowledge_bases')}")
```

### 步骤 3: 启动 API 服务器

在测试实际功能之前，需要确保 Nexus AI API 服务器在本地运行：

```bash
# 在另一个终端启动您的 API 服务器
# 确保监听在 http://localhost:8000
```

### 步骤 4: 测试基础功能

运行基础示例：

```bash
python examples/basic_usage.py
```

**这个脚本会测试**:
1. ✅ 文本生成（简单模式）
2. ✅ 流式文本生成
3. ✅ 会话管理（创建、对话、历史）
4. ✅ 图像生成

### 步骤 5: 测试单个功能

创建自定义测试脚本：

```python
# test_text_generation.py
from nexusai import NexusAIClient

client = NexusAIClient()

# 测试文本生成
print("Testing text generation...")
response = client.text.generate("你好，请介绍一下自己")
print(f"Response: {response.text}")
print(f"Tokens used: {response.usage.total_tokens if response.usage else 'N/A'}")
```

运行：
```bash
python test_text_generation.py
```

## ✅ 验收标准检查清单

根据 `acceptance_criteria_final.md`：

### 基础架构 (FP)
- [x] FP-01: 项目结构完整
- [x] FP-02: 依赖项配置正确
- [x] FP-03: 版本号 0.1.0
- [ ] FP-04: 可安装性 ← **当前测试**
- [ ] FP-05: 包导入 ← **当前测试**
- [x] FP-06: LICENSE 和 README

### 配置与初始化 (CI)
- [ ] CI-01: 默认配置 localhost ← **导入测试后验证**
- [ ] CI-02: 环境变量配置 ← **导入测试后验证**
- [ ] CI-03: 参数优先级 ← **需要功能测试**
- [ ] CI-04: API Key 缺失检查 ← **需要功能测试**
- [ ] CI-05: 上下文管理器 ← **需要功能测试**

## 🐛 常见问题排查

### 问题 1: ImportError

**错误**: `ModuleNotFoundError: No module named 'httpx'`

**解决**:
```bash
pip install httpx pydantic python-dotenv
```

### 问题 2: AuthenticationError

**错误**: `AuthenticationError: API key is required`

**解决**: 确保 `.env` 文件存在且包含：
```
NEXUS_API_KEY=nxs_4K5rIBmsp4wNszg_BuZ-Kih4gLLbx41dGxwNk_mkfaw
```

### 问题 3: Connection Error

**错误**: `NetworkError: Connection refused`

**解决**: 确保 API 服务器运行在 `http://localhost:8000`

### 问题 4: 版本不匹配

**错误**: Pydantic 版本 < 2.5.0

**解决**:
```bash
pip install --upgrade pydantic>=2.5.0
```

## 📊 测试报告模板

完成测试后，请记录结果：

```
测试日期: 2025-01-03
测试人员: [您的名字]

✅ 依赖检查: PASS
✅ 导入测试: PASS
✅ 客户端初始化: PASS
□  文本生成: [PASS/FAIL]
□  流式生成: [PASS/FAIL]
□  会话管理: [PASS/FAIL]
□  图像生成: [PASS/FAIL]
□  文件上传: [PASS/FAIL]
□  音频处理: [PASS/FAIL]
□  知识库: [PASS/FAIL]

备注:
[记录任何问题或观察]
```

## 🚀 下一步

导入测试通过后：

1. **单元测试开发** (第四阶段)
   - 使用 pytest
   - 模拟 HTTP 响应
   - 测试覆盖率 > 80%

2. **集成测试**
   - 真实 API 调用
   - 端到端场景

3. **文档完善**
   - API 参考文档
   - 更多示例

4. **发布准备**
   - TestPyPI 验证
   - CI/CD 配置

---

**当前状态**: 等待导入测试执行 ⏳

**执行命令**: `python quick_test.py`
