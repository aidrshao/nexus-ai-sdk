好的，根据您提供的《Nexus AI Python SDK v0.1.0 详细实施方案》，我为您制定了一份详尽的验收测试清单。

这份清单旨在确保SDK的每一个功能、每一个细节都严格遵循设计文档，保证其质量、稳定性和用户体验。只有当以下所有检查项都通过时，我们才能确认SDK v0.1.0版本已完全开发好并准备发布。

---

## Nexus AI Python SDK v0.1.0 验收测试清单

**验收目标**: 确认SDK v0.1.0的开发工作已全面完成，产品质量达到发布标准。

**最终验收标准**: **所有**清单项目均已通过验证，无任何`Critical`或`Major`级别的未解决问题。

---

### 一、 基础架构与打包 (Foundation & Packaging)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | FP-01 | **项目结构完整性** | 最终代码库的目录结构与文档`1.2 详细项目结构`中定义的完全一致。 | | |
| `[ ]` | FP-02 | **依赖项检查** | `pyproject.toml`中定义的生产和开发依赖项与文档`1.1 核心依赖选择`一致，版本号兼容。 | | |
| `[ ]` | FP-03 | **版本信息** | `nexusai/__version__.py` 文件存在，且版本号为 `0.1.0`。 | | |
| `[ ]` | FP-04 | **可安装性** | 在干净的Python 3.8+ 环境中，可以通过`pip install .` 或 `poetry install` 成功安装SDK包。 | | |
| `[ ]` | FP-05 | **包导入** | 安装后，可以成功执行 `import nexusai` 和 `from nexusai import NexusAIClient` 等核心导入语句。 | | |
| `[ ]` | FP-06 | **许可证与说明** | 项目根目录下包含 `LICENSE` (MIT) 和 `README.md` 文件。 | | |

### 二、 配置与客户端初始化 (Configuration & Client Initialization)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | CI-01 | **默认配置** | 不设置任何环境变量时，`NexusAIClient` 默认指向 `base_url="http://localhost:8000/api/v1"`。 | | 验证开发友好性 |
| `[ ]` | CI-02 | **环境变量配置** | 设置 `NEXUS_API_KEY`, `NEXUS_BASE_URL`, `NEXUS_TIMEOUT` 等环境变量后，客户端初始化时能正确读取并应用这些配置。 | | |
| `[ ]` | CI-03 | **实例化参数覆盖** | 通过 `NexusAIClient(api_key="...", base_url="...")` 实例化时，传入的参数优先级高于环境变量。 | | |
| `[ ]` | CI-04 | **API Key缺失** | 在未设置环境变量且未在初始化时传入`api_key`的情况下，实例化`NexusAIClient`应立即抛出 `AuthenticationError`。 | | 关键安全检查 |
| `[ ]` | CI-05 | **客户端上下文管理** | `NexusAIClient` 支持 `with` 语句，在退出 `with` 代码块时，底层的`httpx.Client`应被关闭。 | | |

### 三、 核心功能与资源模块 (Core Features & Resources)

#### 3.1 错误处理 (Error Handling)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | EH-01 | **认证失败 (401)** | 使用无效的API Key发起请求时，SDK应捕获401状态码并抛出 `nexusai.error.AuthenticationError`。 | | 模拟HTTP 401 |
| `[ ]` | EH-02 | **权限不足 (403)** | 模拟API返回403时，SDK应抛出 `nexusai.error.PermissionError`。 | | 模拟HTTP 403 |
| `[ ]` | EH-03 | **资源未找到 (404)** | 请求一个不存在的资源（如 `client.sessions.get("non_exist_id")`）时，SDK应抛出 `nexusai.error.NotFoundError`。 | | 模拟HTTP 404 |
| `[ ]` | EH-04 | **请求参数错误 (400)** | 发送格式错误或缺少必要参数的请求时，SDK应抛出 `nexusai.error.InvalidRequestError`。 | | 模拟HTTP 400 |
| `[ ]` | EH-05 | **速率限制 (429)** | 模拟API返回429时，SDK应抛出 `nexusai.error.RateLimitError`，并且可以访问到 `retry_after` 属性。 | | 模拟HTTP 429 |
| `[ ]` | EH-06 | **服务器错误 (5xx)** | 模拟API返回500或503时，SDK应抛出 `nexusai.error.ServerError`。 | | 模拟HTTP 500 |
| `[ ]` | EH-07 | **请求超时** | 设置一个极短的`timeout`并发起一个耗时较长的请求，SDK应抛出 `nexusai.error.APITimeoutError`。 | | |
| `[ ]` | EH-08 | **任务轮询超时** | 轮询一个永远不返回 "completed" 或 "failed" 状态的任务，`TaskPoller` 应在达到`poll_timeout`后抛出 `APITimeoutError`。 | | |
| `[ ]` | EH-09 | **任务失败** | 轮询一个最终状态为 "failed" 的任务，`TaskPoller` 应抛出包含错误信息的 `APIError`。 | | |

#### 3.2 图像生成 (`images`)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | IMG-01 | **阻塞式生成成功** | 调用 `client.images.generate(...)`，SDK应先请求创建任务，然后自动轮询任务状态，最终成功返回一个包含`image_url`等信息的 `Image` Pydantic模型对象。 | | 核心Happy Path |
| `[ ]` | IMG-02 | **参数传递** | 调用 `generate` 时传入的 `prompt`, `model`, `size`, `quality` 等所有参数都已正确地包含在发送给 `/invoke` 接口的请求体中。 | | |

#### 3.3 文本生成 (`text`)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | TXT-01 | **同步生成** | 调用同步的`generate`接口，可以成功返回完整的文本生成结果。 | | 阻塞式 |
| `[ ]` | TXT-02 | **异步任务式生成** | 调用`generate_async`接口（根据文档推断，应指需要轮询的模式），可以成功返回任务ID，并通过轮询获取最终结果。 | | |
| `[ ]` | TXT-03 | **流式生成** | 调用 `stream` 接口，可以返回一个迭代器。遍历该迭代器能逐个获取服务端发送的SSE事件块（`Dict`）。 | | |
| `[ ]` | TXT-04 | **流式结束处理** | 流式响应在遇到 `data: [DONE]` 标记时应正确停止迭代。 | | |

#### 3.4 会话管理 (`sessions`)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | SES-01 | **创建会话** | `client.sessions.create(...)` 成功调用并返回一个 `Session` 对象，该对象包含 `id` 等属性。 | | |
| `[ ]` | SES-02 | **获取会话** | `client.sessions.get(session_id)` 成功返回一个对应的 `Session` 对象。 | | |
| `[ ]` | SES-03 | **列出所有会话** | `client.sessions.list()` 成功返回一个 `SessionModel` 对象的列表。 | | |
| `[ ]` | SES-04 | **会话内同步调用** | 在 `Session` 对象上调用 `.invoke(prompt)` 方法，可以同步返回包含AI回复的 `SessionResponse` 对象。 | | |
| `[ ]` | SES-05 | **会话内流式调用** | 在 `Session` 对象上调用 `.stream(prompt)` 方法，可以返回一个迭代器，并能逐块接收流式响应。 | | |
| `[ ]` | SES-06 | **获取历史消息** | 在 `Session` 对象上调用 `.history()` 方法，可以返回一个 `Message` 对象列表。 | | |
| `[ ]` | SES-07 | **删除会话** | 在 `Session` 对象上调用 `.delete()` 方法后，该会话的 `is_active` 属性变为 `False`，并且后续无法再操作。 | | |

#### 3.5 其他资源模块 (Audio, KnowledgeBases, Files)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | RES-01 | **音频处理 (`audio`)** | `audio` 模块的 ASR/TTS 功能可以正确处理异步任务逻辑，并返回结果。 | | |
| `[ ]` | RES-02 | **知识库 (`knowledge_bases`)** | `knowledge_bases` 模块支持文档上传和搜索功能，接口调用符合预期。 | | |
| `[ ]` | RES-03 | **文件管理 (`files`)** | `files` 模块的通用文件上传接口可正常工作。 | | |

### 四、 代码质量与测试 (Code Quality & Testing)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | TQ-01 | **单元测试覆盖率** | 单元测试覆盖率达到或超过 **80%**。 | | M4验收标准 |
| `[ ]` | TQ-02 | **集成测试** | `tests/integration` 目录下的测试用例均已通过，覆盖了核心的用户使用场景。 | | |
| `[ ]` | TQ-03 | **代码格式化** | 运行 `black --check .` 命令，不报告任何需要修改的文件。 | | |
| `[ ]` | TQ-04 | **代码检查** | 运行 `ruff check .` 命令，不报告任何错误或关键警告。 | | |
| `[ ]` | TQ-05 | **静态类型检查** | 运行 `mypy nexusai` 命令，不报告任何类型错误。所有公共API均有类型提示。 | | |
| `[ ]` | TQ-06 | **持续集成 (CI)** | `.github/workflows/tests.yml` 配置正确，能够在 `push` 和 `pull_request` 时自动触发。 | | |
| `[ ]` | TQ-07 | **多Python版本测试** | CI流程应在所有目标Python版本（3.8, 3.9, 3.10, 3.11, 3.12）上成功运行并通过所有测试。 | | |

### 五、 文档与示例 (Documentation & Examples)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | DOC-01 | **README** | `README.md` 内容完善，包含项目简介、安装指南和快速上手示例。 | | M5验收标准 |
| `[ ]` | DOC-02 | **API参考** | `docs/api_reference.md` 内容完整，覆盖所有公开的类、方法和参数，并有清晰的说明。所有公共方法都有Docstring。 | | |
| `[ ]` | DOC-03 | **入门指南** | `docs/getting_started.md` 内容清晰易懂，能引导新用户在5分钟内完成首次API调用。 | | 成功标准 |
| `[ ]` | DOC-04 | **示例代码可运行** | `examples/` 目录下的所有示例脚本（如`basic_usage.py`, `streaming_example.py`等）均可独立、无错误地运行。 | | M5验收标准 |

### 六、 发布准备 (Release Readiness)

| 状态 | 检查项 ID | 检查内容 | 预期结果 | 负责人 | 备注 |
| :--: | :--- | :--- | :--- | :--- | :--- |
| `[ ]` | REL-01 | **发布流程** | PyPI发布流程已定义并测试过（可在TestPyPI上验证），发布脚本可用。 | | |
| `[ ]` | REL-02 | **变更日志 (Changelog)** | 项目已准备好 v0.1.0 版本的变更日志。 | | |
| `[ ]` | REL-03 | **安全检查** | 已检查代码中无硬编码的敏感信息（如API密钥），日志中不会打印完整的密钥。 | | |
| `[ ]` | REL-04 | **最终审核** | 最终代码已通过至少一位核心开发者的审查和批准 (Code Review)。 | | |

---
**验收通过确认:**

**测试负责人:** _________________________

**开发负责人:** _________________________

**批准日期:** _________________________