# Nexus AI SDK - 应用开发团队问题解答

**更新时间**: 2025-10-06
**SDK版本**: keystone-ai v0.2.1a1

---

## 📋 问题清单解答

### 🔴 A. 文本生成模型

#### 问题1: Nexus AI 支持哪些文本模型？

**三档模型体系**：

**🥇 高端模型 (Premium Tier)** - 顶级推理能力
- `gpt-5` - 最快的高端模型，复杂推理 + 速度要求
- `gemini-2.5-pro` - 最强推理能力，深度分析（较慢）

**🥈 中端模型 (Standard Tier)** - 日常通用任务
- `gpt-5-mini` - 通用任务、对话、平衡性能

**🥉 经济模型 (Budget Tier)** - 成本优先
- `deepseek-v3.2-exp` - **默认模型**，最便宜，大批量场景
- `gpt-4o-mini` - 经济型备选方案

---

#### 问题2: 模型名称的传递格式？

**完整格式**（推荐）：
```python
"gpt-5"
"gpt-5-mini"
"gemini-2.5-pro"
"deepseek-v3.2-exp"
"gpt-4o-mini"
```

**默认模型**: 如果不传 `model` 参数，默认使用 `deepseek-v3.2-exp` (最经济)

---

#### 问题3: Temperature参数的有效范围？

✅ **完全支持 0.0 - 2.0**

**推荐设置**：
- 0.0 - 0.3: 事实性任务（摘要、翻译）
- 0.7: 平衡创造力（通用对话）
- 0.9 - 1.5: 创意任务（故事、头脑风暴）

---

### 🔴 B. 图片生成模型

#### 问题4: Nexus AI 支持哪些图片生成模型？

| 模型 | 提供商 | 质量 | 速度 | 推荐度 |
|------|--------|------|------|--------|
| `doubao-seedream-4-0-250828` | 字节跳动豆包 | 🌟🌟🌟 | ⚡⚡⚡ 快 | **默认推荐** |
| `gemini-2.5-flash-image` | Google Gemini | 🌟🌟🌟 | ⚡⚡ 中 | 备选方案 |

---

#### 问题5: 模型名称的传递格式？

```python
"doubao-seedream-4-0-250828"  # 默认推荐（如不传model参数）
"gemini-2.5-flash-image"      # 备选方案
```

---

#### 问题6: 图片尺寸的传递格式？

**选项1: 比例字符串** ✅ **仅支持此格式**

```python
"1:1"    # 正方形 (1024x1024)
"16:9"   # 横向宽屏 (1792x1024)
"9:16"   # 竖向宽屏 (1024x1792)
"4:3"    # 标准横向 (1365x1024)
"3:4"    # 标准竖向 (1024x1365)
"21:9"   # 超宽屏 (2389x1024)
```

❌ **不支持**: 自定义像素尺寸（如 `"1920x1080"`）

---

#### 问题7: 是否支持自定义风格提示词（style prompt）？

**不支持单独的 `style` 参数**

✅ **正确做法**: 将风格描述融入主 prompt

```python
# ✅ 正确
prompt = "赛博朋克风格的科技背景，霓虹灯光，未来主义，高质量渲染"

# ❌ 错误（API不支持style参数）
prompt = "科技背景"
style = "赛博朋克"  # 不存在这个参数
```

---

### 🔴 C. API调用示例

#### 问题8: 实际调用示例

**文本生成示例**：

```python
from nexusai import NexusAIClient

client = NexusAIClient(api_key="your_api_key")

# 示例1: 使用默认模型（最经济）
response = client.text.generate(
    prompt="写一篇关于AI的文章",
    # model 参数可省略，默认使用 deepseek-v3.2-exp
    temperature=0.7,
    max_tokens=2000
)
print(response.text)

# 示例2: 使用中端模型（平衡性能）
response = client.text.generate(
    prompt="总结这篇文章的要点",
    model="gpt-5-mini",
    temperature=0.7,
    max_tokens=1500
)

# 示例3: 使用高端模型（快速推理）
response = client.text.generate(
    prompt="分析这份复杂的法律合同",
    model="gpt-5",  # 高端模型，最快
    temperature=0.3,
    max_tokens=3000
)

# 示例4: 使用经济备选模型
response = client.text.generate(
    prompt="将这段文字翻译成英文",
    model="gpt-4o-mini",  # 经济型备选
    temperature=0.5,
    max_tokens=1000
)
```

**图片生成示例**：

```python
# 示例1: 使用默认模型（推荐）
image = client.image.generate(
    prompt="一个科技感的背景图，蓝色调，简洁现代",
    aspect_ratio="16:9"
    # model 参数可省略，默认使用 doubao-seedream-4-0-250828
)
print(f"图片URL: {image.url}")

# 示例2: 明确指定模型
image = client.image.generate(
    prompt="专业商务人士头像，正面照，白色背景",
    model="doubao-seedream-4-0-250828",
    aspect_ratio="1:1",
    num_images=1
)

# 示例3: 批量生成（员工头像矩阵）
images = client.image.generate(
    prompt="专业商务人士头像，正面照，白色背景，多样化人物",
    model="doubao-seedream-4-0-250828",
    aspect_ratio="1:1",
    num_images=8  # 一次生成8张
)
for img in images:
    print(f"图片 {img.index + 1}: {img.url}")
```

---

## 🚧 需要产品团队决策的问题

以下问题属于**商业决策**，需要产品/商业化团队确认：

### 🔴 D. 单价成本 (问题9-10)

我们**无权决定定价**，但提供技术参考：

**参考：Google官方定价**（供对标）

| 模型类型 | 参考定价 |
|---------|---------|
| Gemini 1.5 Flash | $0.075/1M tokens (输入) |
| Gemini 1.5 Pro | $1.25/1M tokens (输入) |
| Imagen 4.0 | ~$0.02/张 |

**建议定价策略**：
1. 高端模型（gpt-5, gemini-2.5-pro）: Pro用户专享
2. 中端模型（gpt-5-mini）: 免费版可用，Pro版更高配额
3. 经济模型（deepseek-v3.2-exp, gpt-4o-mini）: 所有用户可用，默认使用deepseek

---

### 🔴 E. 配额策略 (问题11-12)

**建议配额方案**（供参考）：

#### 免费版
- **文本生成**: 50次/月（仅限经济模型 deepseek-v3.2-exp / gpt-4o-mini）
- **图片生成**: 20张/月（仅限 doubao 模型）
- **员工图片**: 1张/员工
- **会话**: 5个活跃会话
- **知识库**: 1个，最多10个文档

#### Pro版
- **文本生成**: 500次/月（所有模型，包括 gpt-5 / gemini-2.5-pro / gpt-5-mini）
- **图片生成**: 200张/月（所有模型）
- **员工图片**: 3张/员工
- **会话**: 无限制
- **知识库**: 10个，无限文档

**数据库强制限制**: ✅ **强烈推荐**

```python
# 建议在配置更新API添加验证
if user.subscription_tier == "free" and len(image_configs) > 1:
    raise ValidationError("免费版每个员工最多配置1张图片")
```

---

### 🔴 F. 成本预估功能 (问题13)

**建议: ✅ 在 v9.0 实现**

**理由**：
1. 提升用户信任（成本透明化）
2. 避免恶意刷量
3. 行业标准做法（OpenAI/Midjourney都有）

**实现示例**：

```python
@router.post("/matrix/estimate-cost")
def estimate_generation_cost(employee_ids: List[int], config: MatrixConfig):
    """生成前成本预估"""
    total_images = len(employee_ids) * len(config.image_configs)

    # 模型单价（待产品团队确认）
    IMAGE_PRICING = {
        "doubao-seedream-4-0-250828": 1.5,  # ¥1.5/张（示例）
        "gemini-2.5-flash-image": 2.0       # ¥2.0/张（示例）
    }

    cost_per_image = IMAGE_PRICING.get(config.image_model, 1.5)
    total_cost = total_images * cost_per_image

    return {
        "total_images": total_images,
        "cost_yuan": total_cost,
        "breakdown": {
            "model": config.image_model,
            "cost_per_image": cost_per_image
        }
    }
```

**UI流程建议**：
```
用户配置 → 点击"生成矩阵" → 弹窗显示成本 → 用户确认 → 开始生成
```

示例弹窗：
```
⚠️ 成本确认
本次生成将消耗：
- 图片数量：16张 (8员工 × 2图片)
- 预计成本：¥24.00
- 使用模型：doubao-seedream-4-0-250828

您的余额：¥128.50

[取消]  [确认生成]
```

---

## 📊 数据库Schema建议

### Enum定义（供你直接使用）

```python
from enum import Enum

class TextModel(str, Enum):
    """文本模型枚举"""
    # 高端模型
    GPT_5 = "gpt-5"
    GEMINI_2_5_PRO = "gemini-2.5-pro"

    # 中端模型
    GPT_5_MINI = "gpt-5-mini"

    # 经济模型
    DEEPSEEK_V3_2 = "deepseek-v3.2-exp"  # 默认
    GPT_4O_MINI = "gpt-4o-mini"

class ImageModel(str, Enum):
    """图片模型枚举"""
    DOUBAO = "doubao-seedream-4-0-250828"  # 默认
    GEMINI_IMAGE = "gemini-2.5-flash-image"

class AspectRatio(str, Enum):
    """图片比例枚举"""
    SQUARE = "1:1"
    LANDSCAPE_16_9 = "16:9"
    PORTRAIT_9_16 = "9:16"
    LANDSCAPE_4_3 = "4:3"
    PORTRAIT_3_4 = "3:4"
    ULTRAWIDE = "21:9"

class SubscriptionTier(str, Enum):
    """订阅层级"""
    FREE = "free"
    PRO = "pro"
```

---

## 🚀 下一步行动建议

### ✅ 可以立即开始的工作（方案B）

1. **数据库Schema** - 使用上面的Enum定义
2. **Pydantic Schemas** - 字段验证逻辑
3. **CRUD基础框架** - get/update员工配置
4. **单元测试框架**

### ⏸️ 等待产品确认的工作

1. **成本计算模块** - 需要确认单价
2. **配额限制逻辑** - 需要确认免费/Pro配额
3. **成本预估UI** - 需要确认是否v9.0实现

**预计时间节省**: 选择方案B可节省 **2天开发时间**

---

## 📚 完整技术文档

- **快速开始**: [QUICKSTART_GUIDE.md](QUICKSTART_GUIDE.md)
- **完整API参考**: [API_REFERENCE_FOR_DEVELOPERS.md](API_REFERENCE_FOR_DEVELOPERS.md)
- **README**: [README.md](README.md)
- **代码示例**: [examples/basic_usage.py](examples/basic_usage.py)

---

**技术问题已全部解答** ✅
**商业问题请产品团队决策** ⏳
**建议立即启动基础开发（方案B）** 🚀
