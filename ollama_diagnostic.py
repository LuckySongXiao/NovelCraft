#!/usr/bin/env python3
"""
Ollama诊断工具
用于检测和修复Ollama连接和模型检测问题
"""

import asyncio
import httpx
import json
import subprocess
import sys
import platform
from typing import Dict, List, Any, Optional

class OllamaDiagnostic:
    """Ollama诊断工具类"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.results = []
        
    def log_result(self, test_name: str, status: str, message: str, details: Optional[Dict] = None):
        """记录测试结果"""
        result = {
            "test": test_name,
            "status": status,  # success, warning, error
            "message": message,
            "details": details or {}
        }
        self.results.append(result)
        
        # 实时显示结果
        status_icon = {"success": "✅", "warning": "⚠️", "error": "❌"}
        print(f"{status_icon.get(status, '❓')} {test_name}: {message}")
        if details:
            for key, value in details.items():
                print(f"   {key}: {value}")
    
    def check_system_info(self):
        """检查系统信息"""
        print("\n🔍 [1/8] 系统信息检查")
        
        system_info = {
            "操作系统": platform.system(),
            "系统版本": platform.release(),
            "架构": platform.machine(),
            "Python版本": sys.version.split()[0]
        }
        
        self.log_result(
            "系统信息",
            "success",
            "系统信息收集完成",
            system_info
        )
    
    def check_ollama_installation(self):
        """检查Ollama安装"""
        print("\n🔍 [2/8] Ollama安装检查")
        
        try:
            # 检查ollama命令是否可用
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log_result(
                    "Ollama安装",
                    "success",
                    f"Ollama已安装: {version}"
                )
            else:
                self.log_result(
                    "Ollama安装",
                    "error",
                    "Ollama命令执行失败",
                    {"错误输出": result.stderr}
                )
        except subprocess.TimeoutExpired:
            self.log_result(
                "Ollama安装",
                "error",
                "Ollama命令执行超时"
            )
        except FileNotFoundError:
            self.log_result(
                "Ollama安装",
                "error",
                "未找到Ollama命令，请安装Ollama",
                {"安装地址": "https://ollama.ai/"}
            )
        except Exception as e:
            self.log_result(
                "Ollama安装",
                "error",
                f"检查Ollama安装时发生错误: {str(e)}"
            )
    
    async def check_service_connection(self):
        """检查服务连接"""
        print("\n🔍 [3/8] 服务连接检查")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/", timeout=10.0)
                
                if response.status_code == 200:
                    self.log_result(
                        "服务连接",
                        "success",
                        f"成功连接到Ollama服务 ({self.base_url})"
                    )
                else:
                    self.log_result(
                        "服务连接",
                        "warning",
                        f"服务响应异常，状态码: {response.status_code}"
                    )
        except httpx.ConnectError:
            self.log_result(
                "服务连接",
                "error",
                f"无法连接到Ollama服务 ({self.base_url})",
                {"建议": "运行 'ollama serve' 启动服务"}
            )
        except httpx.TimeoutException:
            self.log_result(
                "服务连接",
                "error",
                "连接超时",
                {"建议": "检查网络连接或服务状态"}
            )
        except Exception as e:
            self.log_result(
                "服务连接",
                "error",
                f"连接检查失败: {str(e)}"
            )
    
    async def check_api_endpoints(self):
        """检查API端点"""
        print("\n🔍 [4/8] API端点检查")
        
        endpoints = [
            ("/api/tags", "模型列表API"),
            ("/api/version", "版本信息API"),
            ("/api/generate", "文本生成API"),
            ("/api/chat", "聊天API"),
            ("/api/show", "模型信息API")
        ]
        
        for endpoint, description in endpoints:
            try:
                async with httpx.AsyncClient() as client:
                    if endpoint in ["/api/generate", "/api/chat", "/api/show"]:
                        # 这些端点需要POST请求
                        response = await client.post(
                            f"{self.base_url}{endpoint}",
                            json={"model": "test"},
                            timeout=5.0
                        )
                    else:
                        response = await client.get(f"{self.base_url}{endpoint}", timeout=5.0)
                    
                    if response.status_code in [200, 400, 404]:  # 400/404也表示端点存在
                        self.log_result(
                            description,
                            "success",
                            f"端点可用 (状态码: {response.status_code})"
                        )
                    else:
                        self.log_result(
                            description,
                            "warning",
                            f"端点响应异常 (状态码: {response.status_code})"
                        )
            except Exception as e:
                self.log_result(
                    description,
                    "error",
                    f"端点检查失败: {str(e)}"
                )
    
    async def check_model_list(self):
        """检查模型列表"""
        print("\n🔍 [5/8] 模型列表检查")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=30.0)
                response.raise_for_status()
                
                data = response.json()
                models = data.get("models", [])
                
                if models:
                    model_info = []
                    for model in models:
                        model_info.append({
                            "名称": model.get("name", "未知"),
                            "大小": f"{model.get('size', 0) / (1024**3):.2f} GB",
                            "修改时间": model.get("modified_at", "未知")
                        })
                    
                    self.log_result(
                        "模型列表",
                        "success",
                        f"检测到 {len(models)} 个模型",
                        {"模型列表": model_info}
                    )
                else:
                    self.log_result(
                        "模型列表",
                        "warning",
                        "未检测到任何模型",
                        {"建议": "使用 'ollama pull <model>' 下载模型"}
                    )
        except Exception as e:
            self.log_result(
                "模型列表",
                "error",
                f"获取模型列表失败: {str(e)}"
            )
    
    async def check_default_model(self):
        """检查默认模型"""
        print("\n🔍 [6/8] 默认模型检查")
        
        default_model = "mollysama/rwkv-7-g1:0.4B"
        
        try:
            async with httpx.AsyncClient() as client:
                # 先获取模型列表
                response = await client.get(f"{self.base_url}/api/tags", timeout=30.0)
                response.raise_for_status()
                
                data = response.json()
                models = [model.get("name", "") for model in data.get("models", [])]
                
                if default_model in models:
                    self.log_result(
                        "默认模型",
                        "success",
                        f"默认模型 {default_model} 已安装"
                    )
                else:
                    self.log_result(
                        "默认模型",
                        "warning",
                        f"默认模型 {default_model} 未安装",
                        {
                            "建议": f"运行 'ollama pull {default_model}' 下载模型",
                            "可用模型": models[:5] if models else ["无"]
                        }
                    )
        except Exception as e:
            self.log_result(
                "默认模型",
                "error",
                f"检查默认模型失败: {str(e)}"
            )
    
    async def test_model_generation(self):
        """测试模型生成"""
        print("\n🔍 [7/8] 模型生成测试")
        
        try:
            # 先获取可用模型
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=30.0)
                response.raise_for_status()
                
                data = response.json()
                models = data.get("models", [])
                
                if not models:
                    self.log_result(
                        "模型生成测试",
                        "warning",
                        "无可用模型进行测试"
                    )
                    return
                
                # 选择第一个模型进行测试
                test_model = models[0].get("name", "")
                
                # 测试生成
                test_data = {
                    "model": test_model,
                    "prompt": "Hello",
                    "stream": False,
                    "options": {
                        "num_predict": 10
                    }
                }
                
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=test_data,
                    timeout=60.0
                )
                response.raise_for_status()
                
                result = response.json()
                generated_text = result.get("response", "")
                
                self.log_result(
                    "模型生成测试",
                    "success",
                    f"模型 {test_model} 生成测试成功",
                    {
                        "输入": "Hello",
                        "输出": generated_text[:100] + "..." if len(generated_text) > 100 else generated_text
                    }
                )
        except Exception as e:
            self.log_result(
                "模型生成测试",
                "error",
                f"模型生成测试失败: {str(e)}"
            )
    
    def check_network_and_firewall(self):
        """检查网络和防火墙"""
        print("\n🔍 [8/8] 网络和防火墙检查")
        
        try:
            # 检查端口是否被占用
            import socket
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 11434))
            sock.close()
            
            if result == 0:
                self.log_result(
                    "端口检查",
                    "success",
                    "端口 11434 可访问"
                )
            else:
                self.log_result(
                    "端口检查",
                    "error",
                    "端口 11434 不可访问",
                    {"建议": "检查Ollama服务是否启动"}
                )
        except Exception as e:
            self.log_result(
                "端口检查",
                "error",
                f"端口检查失败: {str(e)}"
            )
    
    def generate_report(self):
        """生成诊断报告"""
        print("\n" + "="*60)
        print("📋 诊断报告总结")
        print("="*60)
        
        success_count = sum(1 for r in self.results if r["status"] == "success")
        warning_count = sum(1 for r in self.results if r["status"] == "warning")
        error_count = sum(1 for r in self.results if r["status"] == "error")
        
        print(f"✅ 成功: {success_count}")
        print(f"⚠️  警告: {warning_count}")
        print(f"❌ 错误: {error_count}")
        print()
        
        if error_count > 0:
            print("🔧 需要修复的问题:")
            for result in self.results:
                if result["status"] == "error":
                    print(f"   • {result['test']}: {result['message']}")
                    if "建议" in result["details"]:
                        print(f"     建议: {result['details']['建议']}")
            print()
        
        if warning_count > 0:
            print("⚠️  需要注意的问题:")
            for result in self.results:
                if result["status"] == "warning":
                    print(f"   • {result['test']}: {result['message']}")
                    if "建议" in result["details"]:
                        print(f"     建议: {result['details']['建议']}")
            print()
        
        # 总体状态
        if error_count == 0 and warning_count == 0:
            print("🎉 所有检查通过！Ollama配置正常。")
        elif error_count == 0:
            print("✅ 基本功能正常，但有一些建议需要关注。")
        else:
            print("❌ 发现问题，请按照上述建议进行修复。")
        
        print("="*60)

async def main():
    """主函数"""
    print("🔧 NovelCraft Ollama 诊断工具")
    print("="*60)
    
    diagnostic = OllamaDiagnostic()
    
    # 执行所有检查
    diagnostic.check_system_info()
    diagnostic.check_ollama_installation()
    await diagnostic.check_service_connection()
    await diagnostic.check_api_endpoints()
    await diagnostic.check_model_list()
    await diagnostic.check_default_model()
    await diagnostic.test_model_generation()
    diagnostic.check_network_and_firewall()
    
    # 生成报告
    diagnostic.generate_report()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  诊断被用户中断")
    except Exception as e:
        print(f"\n\n❌ 诊断过程中发生错误: {e}")
        print("请检查Python环境和依赖包安装")
