#!/usr/bin/env python3
"""
验证 keystone-ai v0.2.1 图片生成功能

此脚本验证：
1. SDK版本正确
2. 图片生成功能可用
3. 任务轮询自动处理
"""

import sys
from nexusai import NexusAIClient
import nexusai

def verify_version():
    """验证SDK版本"""
    print("=" * 60)
    print("步骤1: 验证SDK版本")
    print("=" * 60)

    version = nexusai.__version__
    print(f"当前SDK版本: {version}")

    if version == "0.2.1":
        print("✅ 版本正确！")
        return True
    else:
        print(f"❌ 版本错误！当前版本是 {version}，需要 0.2.1")
        print("\n请运行以下命令升级:")
        print("pip install --upgrade keystone-ai")
        return False

def verify_image_generation():
    """验证图片生成功能"""
    print("\n" + "=" * 60)
    print("步骤2: 验证图片生成功能")
    print("=" * 60)

    try:
        # 初始化客户端
        client = NexusAIClient()
        print("✅ 客户端初始化成功")

        # 测试图片生成
        print("\n正在生成测试图片...")
        print("提示词: '一个简单的测试图片'")
        print("模型: doubao-seedream-4-0-250828 (默认)")
        print("比例: 1:1")

        # SDK会自动处理任务轮询！
        image = client.image.generate(
            prompt="一个简单的测试图片",
            aspect_ratio="1:1"
        )

        print("\n✅ 图片生成成功！")
        print(f"图片URL: {image.url}")
        print(f"图片尺寸: {image.width}x{image.height}")

        print("\n" + "=" * 60)
        print("重要提示:")
        print("=" * 60)
        print("✅ SDK已自动处理任务轮询")
        print("✅ 你不需要自己实现轮询系统")
        print("✅ 只需调用 client.image.generate() 即可")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ 图片生成失败: {e}")
        return False

def verify_batch_generation():
    """验证批量图片生成"""
    print("\n" + "=" * 60)
    print("步骤3: 验证批量图片生成（可选）")
    print("=" * 60)

    try:
        client = NexusAIClient()

        print("\n正在批量生成3张图片...")

        # 批量生成
        images = client.image.generate(
            prompt="测试图片",
            aspect_ratio="1:1",
            num_images=3
        )

        print(f"\n✅ 成功生成 {len(images)} 张图片！")
        for i, img in enumerate(images, 1):
            print(f"  图片{i}: {img.url[:50]}...")

        return True

    except Exception as e:
        print(f"\n⚠️ 批量生成测试跳过: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Nexus AI SDK v0.2.1 功能验证")
    print("=" * 60)

    # 步骤1: 验证版本
    if not verify_version():
        sys.exit(1)

    # 步骤2: 验证图片生成
    if not verify_image_generation():
        print("\n" + "=" * 60)
        print("验证失败！可能的原因：")
        print("=" * 60)
        print("1. API密钥未配置或无效")
        print("   解决方法: 设置环境变量 NEXUS_API_KEY=your_api_key")
        print("2. 网络连接问题")
        print("   解决方法: 检查网络连接")
        print("3. 后端服务问题")
        print("   解决方法: 联系support@nexus-ai.com")
        sys.exit(1)

    # 步骤3: 验证批量生成（可选）
    verify_batch_generation()

    print("\n" + "=" * 60)
    print("✅ 所有验证通过！")
    print("=" * 60)
    print("\nkeystone-ai v0.2.1 图片生成功能完全可用！")
    print("你可以在应用中直接使用，无需自己实现轮询。")
    print("\n更多文档:")
    print("- Quick Start: https://github.com/aidrshao/nexus-ai-sdk/blob/main/QUICKSTART_GUIDE.md")
    print("- API Reference: https://github.com/aidrshao/nexus-ai-sdk/blob/main/API_REFERENCE_FOR_DEVELOPERS.md")

if __name__ == "__main__":
    main()
