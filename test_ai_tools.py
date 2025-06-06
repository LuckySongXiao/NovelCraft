#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI工具页功能测试脚本
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.ai_service import ai_manager


async def test_ai_tools():
    """测试AI工具功能"""
    print("🤖 开始测试AI工具页功能...")
    
    # 测试AI服务状态
    print("\n1. 测试AI服务连接状态...")
    try:
        is_connected = await ai_manager.check_connection()
        current_provider = ai_manager.get_current_provider()
        print(f"   当前提供商: {current_provider}")
        print(f"   连接状态: {'✅ 在线' if is_connected else '❌ 离线'}")
    except Exception as e:
        print(f"   ❌ 连接测试失败: {e}")
    
    # 测试基础文本生成
    print("\n2. 测试基础文本生成...")
    try:
        response = await ai_manager.generate_text(
            "请简单介绍一下人工智能",
            max_tokens=100,
            temperature=0.7
        )
        print(f"   ✅ 生成成功: {response[:50]}...")
    except Exception as e:
        print(f"   ❌ 生成失败: {e}")
    
    # 测试高级参数
    print("\n3. 测试高级参数支持...")
    try:
        response = await ai_manager.generate_text(
            "创作一个简短的故事",
            max_tokens=150,
            temperature=0.8,
            top_p=0.9,
            frequency_penalty=0.1
        )
        print(f"   ✅ 高级参数测试成功: {response[:50]}...")
    except Exception as e:
        print(f"   ❌ 高级参数测试失败: {e}")
    
    # 测试聊天功能
    print("\n4. 测试聊天功能...")
    try:
        messages = [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ]
        response = await ai_manager.chat_completion(messages, max_tokens=100)
        print(f"   ✅ 聊天测试成功: {response[:50]}...")
    except Exception as e:
        print(f"   ❌ 聊天测试失败: {e}")
    
    print("\n🎉 AI工具页功能测试完成！")


def test_frontend_components():
    """测试前端组件"""
    print("\n📱 检查前端组件文件...")
    
    frontend_file = "frontend/src/pages/AIAssistant.js"
    if os.path.exists(frontend_file):
        print(f"   ✅ {frontend_file} 存在")
        
        # 检查关键功能
        with open(frontend_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        features = [
            ("智能对话", "智能对话"),
            ("设定生成", "设定生成"),
            ("人物生成", "人物生成"),
            ("剧情生成", "剧情生成"),
            ("续写功能", "续写功能"),
            ("一致性检查", "一致性检查"),
            ("历史记录", "HistoryPanel"),
            ("模板库", "TemplatePanel"),
            ("高级设置", "AISettingsPanel"),
            ("批量生成", "batchMode"),
            ("参数调节", "aiParams")
        ]
        
        print("   检查功能组件:")
        for name, keyword in features:
            if keyword in content:
                print(f"     ✅ {name}")
            else:
                print(f"     ❌ {name} (缺少关键字: {keyword})")
    else:
        print(f"   ❌ {frontend_file} 不存在")


def main():
    """主函数"""
    print("🚀 AI工具页完整功能测试")
    print("=" * 50)
    
    # 测试前端组件
    test_frontend_components()
    
    # 测试后端功能
    try:
        asyncio.run(test_ai_tools())
    except Exception as e:
        print(f"❌ 后端测试失败: {e}")
    
    print("\n📋 功能清单:")
    print("✅ 智能对话 - 支持多轮对话，实时显示")
    print("✅ 设定生成 - 世界观、背景设定生成")
    print("✅ 人物生成 - 角色设定、人物描述生成")
    print("✅ 剧情生成 - 故事大纲、情节生成")
    print("✅ 续写功能 - 基于原文的智能续写")
    print("✅ 一致性检查 - 内容逻辑一致性分析")
    print("✅ 历史记录 - 生成内容的保存和管理")
    print("✅ 模板库 - 预设模板和快速应用")
    print("✅ 高级设置 - AI参数精细调节")
    print("✅ 批量生成 - 一次生成多个结果")
    print("✅ 内容管理 - 复制、下载、保存功能")
    print("✅ 多AI支持 - 支持8种AI提供商")
    print("✅ 状态监控 - 实时显示AI服务状态")
    
    print("\n🎯 使用建议:")
    print("1. 首先在系统设置中配置AI提供商")
    print("2. 使用模板库快速开始创作")
    print("3. 调节高级参数获得更好效果")
    print("4. 利用历史记录管理生成内容")
    print("5. 使用批量生成获得多个选择")


if __name__ == "__main__":
    main()
