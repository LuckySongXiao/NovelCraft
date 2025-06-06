#!/usr/bin/env python3
"""
测试默认AI配置脚本
验证Ollama和mollysama/rwkv-7-g1:0.4B模型的配置
"""

import asyncio
import httpx
import json
from typing import Dict, Any

# 默认配置
DEFAULT_CONFIG = {
    "provider": "ollama",
    "base_url": "http://localhost:11434",
    "model": "mollysama/rwkv-7-g1:0.4B",
    "max_tokens": 2000,
    "temperature": 0.7
}

class OllamaTestClient:
    """Ollama测试客户端"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        
    async def check_service(self) -> Dict[str, Any]:
        """检查Ollama服务状态"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=10.0)
                response.raise_for_status()
                return {
                    "status": "success",
                    "message": "Ollama服务运行正常",
                    "data": response.json()
                }
        except httpx.ConnectError:
            return {
                "status": "error",
                "message": "无法连接到Ollama服务，请确保Ollama已安装并正在运行",
                "suggestion": "运行 'ollama serve' 启动服务"
            }
        except httpx.TimeoutException:
            return {
                "status": "error",
                "message": "连接Ollama服务超时",
                "suggestion": "检查服务状态或网络连接"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"检查服务时发生错误: {str(e)}",
                "suggestion": "请检查Ollama安装和配置"
            }
    
    async def check_model(self, model_name: str) -> Dict[str, Any]:
        """检查指定模型是否可用"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=10.0)
                response.raise_for_status()
                models_data = response.json()
                
                available_models = [model["name"] for model in models_data.get("models", [])]
                
                if model_name in available_models:
                    return {
                        "status": "success",
                        "message": f"模型 {model_name} 已安装并可用",
                        "available": True
                    }
                else:
                    return {
                        "status": "warning",
                        "message": f"模型 {model_name} 未安装",
                        "available": False,
                        "suggestion": f"运行 'ollama pull {model_name}' 下载模型",
                        "available_models": available_models
                    }
        except Exception as e:
            return {
                "status": "error",
                "message": f"检查模型时发生错误: {str(e)}",
                "available": False
            }
    
    async def test_generation(self, model_name: str, prompt: str = "你好，请简单介绍一下自己。") -> Dict[str, Any]:
        """测试模型文本生成"""
        try:
            data = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": DEFAULT_CONFIG["temperature"],
                    "num_predict": 100  # 限制输出长度用于测试
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                
                return {
                    "status": "success",
                    "message": "模型生成测试成功",
                    "prompt": prompt,
                    "response": result.get("response", ""),
                    "model": model_name
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"模型生成测试失败: {str(e)}",
                "suggestion": "请检查模型是否正确安装和配置"
            }

async def main():
    """主测试函数"""
    print("=" * 60)
    print("NovelCraft 默认AI配置测试")
    print("=" * 60)
    print()
    
    # 显示默认配置
    print("📋 默认配置信息:")
    for key, value in DEFAULT_CONFIG.items():
        print(f"   {key}: {value}")
    print()
    
    # 创建测试客户端
    client = OllamaTestClient(DEFAULT_CONFIG["base_url"])
    
    # 1. 检查Ollama服务
    print("🔍 [1/3] 检查Ollama服务状态...")
    service_result = await client.check_service()
    print(f"   状态: {service_result['status']}")
    print(f"   信息: {service_result['message']}")
    if service_result['status'] == 'error':
        print(f"   建议: {service_result.get('suggestion', '')}")
        print("\n❌ 测试终止：Ollama服务不可用")
        return
    
    if service_result['status'] == 'success':
        models_count = len(service_result['data'].get('models', []))
        print(f"   已安装模型数量: {models_count}")
    print()
    
    # 2. 检查默认模型
    print("🔍 [2/3] 检查默认模型...")
    model_result = await client.check_model(DEFAULT_CONFIG["model"])
    print(f"   状态: {model_result['status']}")
    print(f"   信息: {model_result['message']}")
    
    if not model_result['available']:
        print(f"   建议: {model_result.get('suggestion', '')}")
        if model_result.get('available_models'):
            print("   可用模型:")
            for model in model_result['available_models'][:5]:  # 只显示前5个
                print(f"     - {model}")
        print("\n⚠️  默认模型未安装，跳过生成测试")
        return
    print()
    
    # 3. 测试文本生成
    print("🔍 [3/3] 测试文本生成...")
    generation_result = await client.test_generation(DEFAULT_CONFIG["model"])
    print(f"   状态: {generation_result['status']}")
    print(f"   信息: {generation_result['message']}")
    
    if generation_result['status'] == 'success':
        print(f"   提示: {generation_result['prompt']}")
        print(f"   回复: {generation_result['response'][:200]}...")  # 限制显示长度
    else:
        print(f"   建议: {generation_result.get('suggestion', '')}")
    print()
    
    # 总结
    print("=" * 60)
    if (service_result['status'] == 'success' and 
        model_result['available'] and 
        generation_result['status'] == 'success'):
        print("✅ 所有测试通过！默认AI配置工作正常。")
        print("💡 您可以在NovelCraft中正常使用AI功能。")
    else:
        print("⚠️  部分测试未通过，请按照上述建议进行配置。")
        print("📖 详细配置指南请参考: Ollama默认配置指南.md")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生错误: {e}")
        print("请检查Python环境和依赖包安装")
