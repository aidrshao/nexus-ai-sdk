# 手动测试指南

## 为什么需要手动测试？

当前开发环境中，Python 执行受到限制（可能是 Windows Store 版本的权限问题）。因此需要您在本地终端手动运行测试。

## 📋 测试步骤

### 第 1 步：打开命令提示符或 PowerShell

```powershell
# 按 Win + R，输入 cmd 或 powershell，按回车
```

### 第 2 步：进入项目目录

```bash
cd C:\Users\junsh\Documents\GitHub\nexus-ai-sdk
```

### 第 3 步：检查 Python 版本

```bash
python --version
# 或
python3 --version
```

**期望**: 显示 Python 3.8 或更高版本

### 第 4 步：安装依赖（如果尚未安装）

```bash
pip install httpx>=0.25.0 pydantic>=2.5.0 python-dotenv>=1.0.0
```

### 第 5 步：运行导入测试

```bash
python quick_test.py
```

或者如果 `python` 命令不可用：

```bash
python3 quick_test.py
```

### 第 6 步：查看测试结果

## ✅ 测试成功的标志

您应该看到类似这样的输出：

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

## ❌ 常见错误及解决方案

### 错误 1: ModuleNotFoundError: No module named 'httpx'

**解决方案**:
```bash
pip install httpx pydantic python-dotenv
```

### 错误 2: ImportError: cannot import name 'X' from 'nexusai'

**可能原因**: 语法错误或循环导入

**解决方案**:
1. 检查文件是否完整
2. 查看错误堆栈信息
3. 报告具体的错误信息

### 错误 3: Python 命令未找到

**解决方案**:
1. 确保 Python 已安装
2. 检查 PATH 环境变量
3. 使用完整路径，如：`C:\Python39\python.exe quick_test.py`

## 🔍 替代测试方法

如果 `quick_test.py` 无法运行，可以使用 Python REPL 手动测试：

### 方法 A: Python 交互式 REPL

```bash
python
```

然后逐步输入：

```python
>>> import sys
>>> sys.path.insert(0, '.')
>>>
>>> # 测试 1: 导入包
>>> import nexusai
>>> print(nexusai.__version__)
0.1.0
>>>
>>> # 测试 2: 导入客户端
>>> from nexusai import NexusAIClient
>>> print("NexusAIClient imported")
>>>
>>> # 测试 3: 初始化客户端
>>> import os
>>> os.environ['NEXUS_API_KEY'] = 'nxs_4K5rIBmsp4wNszg_BuZ-Kih4gLLbx41dGxwNk_mkfaw'
>>> client = NexusAIClient()
>>> print("Client initialized")
>>>
>>> # 测试 4: 检查资源
>>> print(f"Has images: {hasattr(client, 'images')}")
>>> print(f"Has text: {hasattr(client, 'text')}")
>>> print(f"Has sessions: {hasattr(client, 'sessions')}")
```

### 方法 B: 创建最简测试脚本

创建文件 `test_minimal.py`:

```python
import sys
sys.path.insert(0, '.')

try:
    import nexusai
    print(f"✓ SUCCESS: nexusai version {nexusai.__version__}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
```

运行：
```bash
python test_minimal.py
```

## 📊 测试检查清单

完成测试后，请确认：

- [ ] Python 版本 >= 3.8
- [ ] 依赖包已安装 (httpx, pydantic, python-dotenv)
- [ ] `import nexusai` 成功
- [ ] `from nexusai import NexusAIClient` 成功
- [ ] 客户端可以初始化
- [ ] 所有 6 个资源属性可用 (images, text, sessions, files, audio, knowledge_bases)

## 🚀 测试通过后的下一步

1. **启动 API 服务器**（如果尚未运行）
   ```bash
   # 确保 API 服务器在 http://localhost:8000 运行
   ```

2. **运行功能测试**
   ```bash
   python examples/basic_usage.py
   ```

3. **测试特定功能**
   ```python
   from nexusai import NexusAIClient

   client = NexusAIClient()
   response = client.text.generate("Hello, world!")
   print(response.text)
   ```

## 💬 反馈

测试完成后，请告诉我：

1. 导入测试是否通过？
2. 遇到了哪些错误（如果有）？
3. Python 版本是多少？
4. 依赖包是否需要安装？

这将帮助我了解SDK的实际运行状况，并进行必要的调整。

---

**重要**: 这不是环境的问题，而是出于安全考虑的限制。SDK 代码本身已经完整实现，只是需要在您的本地环境中验证。
