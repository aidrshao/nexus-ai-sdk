# Nexus AI Python SDK - Documentation Index

**Package**: `keystone-ai`
**Version**: v0.2.1
**PyPI**: https://pypi.org/project/keystone-ai/

---

## 📚 Documentation Overview

This page provides a complete index of all available documentation for the Nexus AI Python SDK.

---

## 🚀 Getting Started

### For First-Time Users

1. **[README.md](README.md)** - Project overview and quick start
2. **[QUICKSTART_GUIDE.md](QUICKSTART_GUIDE.md)** - 5-minute tutorial
   - Installation
   - Basic text generation
   - Image generation
   - Session management
   - Model selection guide

### For Application Developers

3. **[APPLICATION_DEVELOPER_RESPONSE.md](APPLICATION_DEVELOPER_RESPONSE.md)** - FAQ and common questions
   - 13 common questions answered
   - Model configuration details
   - API usage examples
   - Quota and pricing strategies

---

## 📖 Technical Reference

### API Documentation

4. **[API_REFERENCE_FOR_DEVELOPERS.md](API_REFERENCE_FOR_DEVELOPERS.md)** - Complete API reference
   - All supported models (6 text + 2 image)
   - Complete API endpoints
   - Parameters and response formats
   - Error handling
   - Best practices

### Model Information

5. **[MODEL_UPDATE_SUMMARY.md](MODEL_UPDATE_SUMMARY.md)** - Model selection guide
   - 3-tier model system
   - Default configurations
   - Pricing recommendations
   - Enum definitions for database

---

## 💻 Code Examples

### Working Examples

6. **[examples/basic_usage.py](examples/basic_usage.py)** - Core features
   - Text generation
   - Streaming
   - Session management
   - Image generation

7. **[examples/error_handling.py](examples/error_handling.py)** - Error handling patterns
   - All error types
   - Retry mechanisms
   - Production-ready patterns

---

## 🛠️ Advanced Topics

### Error Handling

8. **[ERROR_HANDLING_QUICK_REFERENCE.md](ERROR_HANDLING_QUICK_REFERENCE.md)** - Error handling guide
   - Error types and codes
   - Quick reference table
   - Common scenarios

### Version History

9. **[CHANGELOG.md](CHANGELOG.md)** - Complete version history
   - Release notes for all versions
   - Breaking changes
   - Migration guides

---

## 🎯 Release Information

### Current Release

10. **[RELEASE_v0.2.1.md](RELEASE_v0.2.1.md)** - v0.2.1 release notes
    - First stable release announcement
    - Production validation details
    - Known limitations
    - Migration instructions

---

## 📊 Quick Reference

### Installation

```bash
# Stable release
pip install keystone-ai

# 国内镜像加速
pip install keystone-ai -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Basic Usage

```python
from nexusai import NexusAIClient

# Initialize
client = NexusAIClient(api_key="your_api_key")

# Generate text (uses default model: deepseek-v3.2-exp)
response = client.text.generate("Hello, AI!")
print(response.text)

# Generate image (uses default model: doubao-seedream-4-0-250828)
image = client.image.generate("A sunset", aspect_ratio="16:9")
print(image.url)
```

### Supported Models

**Text Models** (Default: `deepseek-v3.2-exp`):
- 🥇 Premium: `gpt-5`, `gemini-2.5-pro`
- 🥈 Standard: `gpt-5-mini`
- 🥉 Budget: `deepseek-v3.2-exp`, `gpt-4o-mini`

**Image Models** (Default: `doubao-seedream-4-0-250828`):
- `doubao-seedream-4-0-250828` (ByteDance)
- `gemini-2.5-flash-image` (Google)

---

## 🔗 External Resources

### Official Links

- **PyPI Package**: https://pypi.org/project/keystone-ai/
- **GitHub Repository**: https://github.com/aidrshao/nexus-ai-sdk
- **Production API**: https://nexus-ai.juncai-ai.com/api/v1
- **Official Website**: https://nexus-ai.juncai-ai.com

### Support Channels

- **GitHub Issues**: https://github.com/aidrshao/nexus-ai-sdk/issues
- **Email Support**: support@nexus-ai.com

---

## 📝 Documentation Roadmap

### Coming Soon

- **Interactive Tutorial** - Step-by-step interactive guide
- **Video Tutorials** - Video walkthroughs
- **API Playground** - Try the API in your browser
- **Read the Docs Site** - Dedicated documentation website

---

## 🤝 Contributing to Documentation

Found an error or want to improve the documentation?

1. **Report Issues**: [Open an issue](https://github.com/aidrshao/nexus-ai-sdk/issues)
2. **Submit PR**: Fork the repo and submit a pull request
3. **Contact Us**: Email support@nexus-ai.com

---

## 📅 Last Updated

**Date**: October 6, 2025
**SDK Version**: v0.2.1
**Status**: Stable Release

---

**Thank you for using Nexus AI Python SDK!** 🚀

For the latest updates, visit our [GitHub repository](https://github.com/aidrshao/nexus-ai-sdk).
