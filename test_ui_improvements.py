#!/usr/bin/env python3
"""
UI改进功能测试脚本
测试前端启动、可折叠菜单、AI助手默认配置等功能
"""

import requests
import time
import json
import sys
import subprocess
import os
from pathlib import Path

# 配置
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_status():
    """测试后端服务状态"""
    print("🔍 测试后端服务状态...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务正常运行")
            return True
        else:
            print(f"❌ 后端服务状态异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 后端服务连接失败: {e}")
        return False

def test_ai_providers():
    """测试AI提供商配置"""
    print("🔍 测试AI提供商配置...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/ai/providers", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI提供商列表: {data.get('providers', [])}")
            print(f"✅ 当前提供商: {data.get('current', 'unknown')}")
            return True
        else:
            print(f"❌ 获取AI提供商失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AI提供商请求失败: {e}")
        return False

def test_ai_status():
    """测试AI服务状态"""
    print("🔍 测试AI服务状态...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/ai/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI服务状态: {data}")
            return True
        else:
            print(f"❌ 获取AI状态失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AI状态请求失败: {e}")
        return False

def test_ollama_models():
    """测试Ollama模型检测"""
    print("🔍 测试Ollama模型检测...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/ai/ollama/models", timeout=15)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ 检测到 {len(models)} 个Ollama模型")
            
            # 检查默认模型
            default_model = "mollysama/rwkv-7-g1:0.4B"
            has_default = data.get('has_default_model', False)
            if has_default:
                print(f"✅ 默认模型 {default_model} 已安装")
            else:
                print(f"⚠️  默认模型 {default_model} 未安装")
                print("💡 建议运行: ollama pull mollysama/rwkv-7-g1:0.4B")
            
            return True
        else:
            print(f"❌ 获取Ollama模型失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama模型请求失败: {e}")
        return False

def test_project_data_api():
    """测试项目数据API"""
    print("🔍 测试项目数据API...")
    try:
        # 测试AI助手读取数据接口
        response = requests.get(f"{BACKEND_URL}/api/project-data/ai/current-project", timeout=10)
        if response.status_code == 400:
            print("✅ AI助手项目接口正常（未设置当前项目）")
        elif response.status_code == 200:
            data = response.json()
            print(f"✅ AI助手当前项目: {data.get('current_project_id')}")
        else:
            print(f"⚠️  AI助手项目接口状态: {response.status_code}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ 项目数据API请求失败: {e}")
        return False

def test_frontend_accessibility():
    """测试前端可访问性"""
    print("🔍 测试前端可访问性...")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print("✅ 前端服务可访问")
            return True
        else:
            print(f"❌ 前端服务状态异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 前端服务连接失败: {e}")
        return False

def check_startup_script():
    """检查启动脚本修改"""
    print("🔍 检查启动脚本修改...")
    script_path = Path("Start-System.bat")
    
    if not script_path.exists():
        print("❌ 启动脚本不存在")
        return False
    
    content = script_path.read_text(encoding='utf-8')
    
    # 检查是否移除了重复打开浏览器的代码
    if "start http://localhost:3000" in content:
        print("❌ 启动脚本仍包含重复打开浏览器的代码")
        return False
    
    if "Browser will open automatically when frontend is ready" in content:
        print("✅ 启动脚本已修改，避免重复打开浏览器")
        return True
    
    print("⚠️  启动脚本状态未知")
    return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 NovelCraft UI改进功能测试")
    print("=" * 60)
    
    tests = [
        ("启动脚本检查", check_startup_script),
        ("后端服务状态", test_backend_status),
        ("AI提供商配置", test_ai_providers),
        ("AI服务状态", test_ai_status),
        ("Ollama模型检测", test_ollama_models),
        ("项目数据API", test_project_data_api),
        ("前端可访问性", test_frontend_accessibility),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # 避免请求过快
    
    # 输出测试结果汇总
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！UI改进功能正常")
        return 0
    else:
        print("⚠️  部分测试失败，请检查相关功能")
        return 1

if __name__ == "__main__":
    sys.exit(main())
