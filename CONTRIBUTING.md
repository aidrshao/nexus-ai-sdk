# Contributing to Nexus AI Python SDK

感谢你对 Nexus AI Python SDK 的贡献！我们欢迎所有形式的贡献，包括 bug 报告、功能建议、文档改进和代码贡献。

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [报告 Bug](#报告-bug)
- [提交功能建议](#提交功能建议)
- [提交代码](#提交代码)
- [开发环境设置](#开发环境设置)
- [测试指南](#测试指南)
- [代码规范](#代码规范)

---

## 行为准则

本项目遵循开源社区的基本准则：
- 尊重所有贡献者
- 建设性地提供反馈
- 专注于对项目最有利的方向
- 保持友好和专业的态度

---

## 如何贡献

### 报告 Bug

如果你发现了 bug，请：

1. **检查是否已有相关 issue**：在 [Issues](https://github.com/aidrshao/nexus-ai-sdk/issues) 中搜索
2. **创建新 issue**，包含以下信息：
   - **SDK 版本**：`pip show keystone-ai` 查看版本
   - **Python 版本**：`python --version`
   - **操作系统**：Windows/macOS/Linux
   - **复现步骤**：详细的代码示例
   - **期望行为**：你期望发生什么
   - **实际行为**：实际发生了什么
   - **错误信息**：完整的错误堆栈

**Bug 报告模板**：
```markdown
**SDK 版本**: 0.2.1
**Python 版本**: 3.9.0
**操作系统**: Windows 11

**复现步骤**:
```python
from nexusai import NexusAI
client = NexusAI(api_key="xxx")
response = client.text.generate(prompt="test")
```

**期望行为**: 返回生成的文本
**实际行为**: 抛出 TimeoutError
**错误信息**: [粘贴完整错误信息]
```

---

### 提交功能建议

如果你有新功能的想法，请：

1. **创建 Feature Request issue**
2. **描述功能**：
   - 用例场景：为什么需要这个功能
   - 建议的 API 设计
   - 可能的实现方案（可选）
3. **等待讨论**：维护者会评估可行性

---

### 提交代码

#### 1️⃣ Fork 和克隆仓库

```bash
# Fork 仓库到你的账号
# 然后克隆到本地
git clone https://github.com/YOUR_USERNAME/nexus-ai-sdk.git
cd nexus-ai-sdk

# 添加上游仓库
git remote add upstream https://github.com/aidrshao/nexus-ai-sdk.git
```

#### 2️⃣ 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/bug-description
```

#### 3️⃣ 开发和测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 进行你的修改
# ...

# 运行测试
pytest

# 检查代码规范
ruff check .
mypy nexusai
```

#### 4️⃣ 提交代码

```bash
git add .
git commit -m "feat: add new feature description"
# 或
git commit -m "fix: resolve issue with ..."
```

**Commit 消息规范**：
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 重构代码
- `chore:` 构建/工具相关

#### 5️⃣ 推送并创建 Pull Request

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request，描述：
- **改动内容**：简要说明做了什么
- **相关 Issue**：`Fixes #123` 或 `Closes #456`
- **测试情况**：如何测试的
- **破坏性变更**：是否有 API 变更

---

## 开发环境设置

### 前置要求

- Python 3.8+
- pip 或 Poetry

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/aidrshao/nexus-ai-sdk.git
cd nexus-ai-sdk

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装开发依赖
pip install -e ".[dev]"

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Key
```

### 项目结构

```
nexus-ai-sdk/
├── nexusai/              # 主包代码
│   ├── __init__.py
│   ├── _internal/        # 内部实现
│   ├── resources/        # API 资源（text, image, files, sessions）
│   ├── models.py         # 数据模型
│   └── error.py          # 错误定义
├── tests/                # 测试代码
├── examples/             # 示例代码
├── docs/                 # 文档
└── pyproject.toml        # 项目配置
```

---

## 测试指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_text.py

# 运行特定测试函数
pytest tests/test_text.py::test_generate_basic

# 查看覆盖率
pytest --cov=nexusai --cov-report=html
```

### 编写测试

每个新功能都应该有对应的测试：

```python
# tests/test_new_feature.py
import pytest
from nexusai import NexusAI

def test_new_feature():
    client = NexusAI(api_key="test-key")
    result = client.new_feature.do_something()
    assert result.success == True
```

---

## 代码规范

### Python 代码风格

我们使用以下工具保证代码质量：

- **Ruff**：代码检查和格式化
- **MyPy**：类型检查
- **Black**：代码格式化（可选）

```bash
# 代码检查
ruff check nexusai

# 自动修复
ruff check --fix nexusai

# 类型检查
mypy nexusai
```

### 代码规范要点

1. **类型注解**：所有公共 API 必须有类型注解
   ```python
   def generate(self, prompt: str, model: str | None = None) -> TextResponse:
       ...
   ```

2. **文档字符串**：所有公共函数/类必须有 docstring
   ```python
   def generate(self, prompt: str) -> TextResponse:
       """生成文本内容

       Args:
           prompt: 输入提示词

       Returns:
           TextResponse: 生成结果

       Raises:
           APIError: API 调用失败
       """
   ```

3. **错误处理**：使用明确的异常类型
   ```python
   from nexusai.error import APIError, ValidationError

   if not prompt:
       raise ValidationError("prompt cannot be empty")
   ```

4. **导入顺序**：
   - 标准库
   - 第三方库
   - 本地模块

---

## 发布流程（仅维护者）

```bash
# 1. 更新版本号
# 编辑 nexusai/__version__.py 和 pyproject.toml

# 2. 更新 CHANGELOG.md

# 3. 构建
python -m build

# 4. 发布到 PyPI
twine upload dist/*

# 5. 创建 Git tag
git tag -a v0.2.2 -m "Release v0.2.2"
git push origin v0.2.2
```

---

## 获取帮助

- **文档**：[完整文档索引](DOCUMENTATION.md)
- **API 参考**：[API_REFERENCE_FOR_DEVELOPERS.md](API_REFERENCE_FOR_DEVELOPERS.md)
- **FAQ**：[APPLICATION_DEVELOPER_RESPONSE.md](APPLICATION_DEVELOPER_RESPONSE.md)
- **Issues**：[GitHub Issues](https://github.com/aidrshao/nexus-ai-sdk/issues)

---

## 许可证

本项目采用 MIT 许可证。贡献代码即表示你同意将你的贡献以相同许可证发布。

---

感谢你的贡献！🎉
