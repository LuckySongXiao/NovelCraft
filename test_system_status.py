#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统状态测试脚本
测试 NovelCraft 系统的各个组件状态
"""

import asyncio
import httpx
import json
import sys
import time
from datetime import datetime

class SystemStatusTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.ollama_url = "http://localhost:11434"
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        
    def print_status(self, service, status, message=""):
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {service:<20} {message}")
        
    async def test_ollama_direct(self):
        """直接测试 Ollama API"""
        self.print_header("Ollama 服务测试")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 测试模型列表
                response = await client.get(f"{self.ollama_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    models = data.get("models", [])
                    self.print_status("Ollama API", True, f"正常 - 发现 {len(models)} 个模型")
                    for model in models[:3]:  # 显示前3个模型
                        print(f"   📦 {model['name']}")
                    return True
                else:
                    self.print_status("Ollama API", False, f"状态码: {response.status_code}")
                    return False
        except Exception as e:
            self.print_status("Ollama API", False, f"错误: {str(e)}")
            return False
            
    async def test_backend(self):
        """测试后端服务"""
        self.print_header("后端服务测试")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 测试健康检查
                response = await client.get(f"{self.backend_url}/api/v1/ai/status")
                if response.status_code == 200:
                    data = response.json()
                    self.print_status("后端 API", True, "正常响应")
                    self.print_status("AI 提供商", True, f"当前: {data.get('provider', 'unknown')}")
                    self.print_status("AI 连接", data.get('connected', False), 
                                    f"状态: {data.get('status', 'unknown')}")
                    
                    # 测试模型列表
                    response = await client.get(f"{self.backend_url}/api/v1/ai/ollama/models")
                    if response.status_code == 200:
                        models_data = response.json()
                        model_count = models_data.get('count', 0)
                        self.print_status("模型列表", True, f"获取到 {model_count} 个模型")
                    else:
                        self.print_status("模型列表", False, f"状态码: {response.status_code}")
                    
                    return True
                else:
                    self.print_status("后端 API", False, f"状态码: {response.status_code}")
                    return False
        except Exception as e:
            self.print_status("后端 API", False, f"错误: {str(e)}")
            return False
            
    async def test_frontend(self):
        """测试前端服务"""
        self.print_header("前端服务测试")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.frontend_url)
                if response.status_code == 200:
                    self.print_status("前端服务", True, "正常访问")
                    return True
                else:
                    self.print_status("前端服务", False, f"状态码: {response.status_code}")
                    return False
        except Exception as e:
            self.print_status("前端服务", False, f"错误: {str(e)}")
            return False
            
    async def test_ai_generation(self):
        """测试 AI 文本生成"""
        self.print_header("AI 功能测试")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                test_data = {
                    "prompt": "请简单介绍一下人工智能",
                    "max_tokens": 50,
                    "temperature": 0.7
                }
                
                response = await client.post(
                    f"{self.backend_url}/api/v1/ai/generate",
                    json=test_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get('text', '')
                    self.print_status("AI 生成", True, f"成功生成 {len(generated_text)} 字符")
                    print(f"   📝 生成内容: {generated_text[:100]}...")
                    return True
                else:
                    self.print_status("AI 生成", False, f"状态码: {response.status_code}")
                    return False
        except Exception as e:
            self.print_status("AI 生成", False, f"错误: {str(e)}")
            return False
            
    async def run_all_tests(self):
        """运行所有测试"""
        print(f"🚀 NovelCraft 系统状态检查")
        print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = {}
        
        # 测试各个组件
        results['ollama'] = await self.test_ollama_direct()
        results['backend'] = await self.test_backend()
        results['frontend'] = await self.test_frontend()
        results['ai_generation'] = await self.test_ai_generation()
        
        # 总结
        self.print_header("测试总结")
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        print(f"📊 测试结果: {passed_tests}/{total_tests} 通过")
        
        if passed_tests == total_tests:
            print("🎉 所有测试通过！系统运行正常。")
            return True
        else:
            print("⚠️  部分测试失败，请检查相关服务。")
            return False

async def main():
    tester = SystemStatusTester()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
