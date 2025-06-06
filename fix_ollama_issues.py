#!/usr/bin/env python3
"""
Ollama问题修复脚本
自动检测和修复常见的Ollama连接和模型检测问题
"""

import asyncio
import subprocess
import sys
import time
import platform
import httpx
from typing import Dict, List, Any, Optional

class OllamaFixer:
    """Ollama问题修复器"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.default_model = "mollysama/rwkv-7-g1:0.4B"
        self.system = platform.system().lower()
        
    def print_step(self, step: str, message: str):
        """打印步骤信息"""
        print(f"\n🔧 [{step}] {message}")
        
    def print_success(self, message: str):
        """打印成功信息"""
        print(f"✅ {message}")
        
    def print_warning(self, message: str):
        """打印警告信息"""
        print(f"⚠️  {message}")
        
    def print_error(self, message: str):
        """打印错误信息"""
        print(f"❌ {message}")
        
    def run_command(self, command: List[str], timeout: int = 30) -> Dict[str, Any]:
        """运行命令并返回结果"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "命令执行超时",
                "returncode": -1
            }
        except FileNotFoundError:
            return {
                "success": False,
                "stdout": "",
                "stderr": "命令不存在",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def check_ollama_installation(self) -> bool:
        """检查Ollama是否已安装"""
        self.print_step("1/6", "检查Ollama安装状态")
        
        result = self.run_command(["ollama", "--version"])
        if result["success"]:
            self.print_success(f"Ollama已安装: {result['stdout']}")
            return True
        else:
            self.print_error("Ollama未安装或不在PATH中")
            self.print_warning("请访问 https://ollama.ai/ 下载安装Ollama")
            return False
    
    def check_ollama_service(self) -> bool:
        """检查Ollama服务状态"""
        self.print_step("2/6", "检查Ollama服务状态")
        
        # 检查进程
        if self.system == "windows":
            result = self.run_command(["tasklist", "/FI", "IMAGENAME eq ollama.exe"])
            service_running = "ollama.exe" in result["stdout"]
        else:
            result = self.run_command(["pgrep", "-f", "ollama"])
            service_running = result["success"] and result["stdout"]
        
        if service_running:
            self.print_success("Ollama服务正在运行")
            return True
        else:
            self.print_warning("Ollama服务未运行")
            return False
    
    def start_ollama_service(self) -> bool:
        """启动Ollama服务"""
        self.print_step("3/6", "启动Ollama服务")
        
        try:
            if self.system == "windows":
                # Windows下在后台启动
                subprocess.Popen(
                    ["ollama", "serve"],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Linux/Mac下在后台启动
                subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # 等待服务启动
            self.print_warning("等待服务启动...")
            time.sleep(5)
            
            # 验证服务是否启动成功
            if self.check_ollama_service():
                self.print_success("Ollama服务启动成功")
                return True
            else:
                self.print_error("Ollama服务启动失败")
                return False
                
        except Exception as e:
            self.print_error(f"启动Ollama服务失败: {e}")
            return False
    
    async def test_api_connection(self) -> bool:
        """测试API连接"""
        self.print_step("4/6", "测试API连接")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=10.0)
                if response.status_code == 200:
                    self.print_success(f"API连接正常 ({self.base_url})")
                    return True
                else:
                    self.print_error(f"API响应异常: {response.status_code}")
                    return False
        except httpx.ConnectError:
            self.print_error(f"无法连接到API ({self.base_url})")
            return False
        except httpx.TimeoutException:
            self.print_error("API连接超时")
            return False
        except Exception as e:
            self.print_error(f"API连接测试失败: {e}")
            return False
    
    async def check_models(self) -> List[str]:
        """检查已安装的模型"""
        self.print_step("5/6", "检查已安装模型")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=30.0)
                if response.status_code == 200:
                    data = response.json()
                    models = [model.get("name", "") for model in data.get("models", [])]
                    
                    if models:
                        self.print_success(f"检测到 {len(models)} 个模型:")
                        for model in models:
                            print(f"   • {model}")
                        return models
                    else:
                        self.print_warning("未检测到任何模型")
                        return []
                else:
                    self.print_error(f"获取模型列表失败: {response.status_code}")
                    return []
        except Exception as e:
            self.print_error(f"检查模型失败: {e}")
            return []
    
    def install_default_model(self) -> bool:
        """安装默认模型"""
        self.print_step("6/6", f"安装默认模型 {self.default_model}")
        
        self.print_warning("正在下载模型，这可能需要几分钟时间...")
        result = self.run_command(["ollama", "pull", self.default_model], timeout=600)  # 10分钟超时
        
        if result["success"]:
            self.print_success(f"默认模型 {self.default_model} 安装成功")
            return True
        else:
            self.print_error(f"模型安装失败: {result['stderr']}")
            
            # 尝试安装备选模型
            backup_models = ["llama2:7b-chat", "qwen:7b-chat", "mistral:7b"]
            for backup_model in backup_models:
                self.print_warning(f"尝试安装备选模型: {backup_model}")
                result = self.run_command(["ollama", "pull", backup_model], timeout=600)
                if result["success"]:
                    self.print_success(f"备选模型 {backup_model} 安装成功")
                    return True
            
            self.print_error("所有模型安装都失败了")
            return False
    
    async def run_full_fix(self):
        """运行完整的修复流程"""
        print("🔧 NovelCraft Ollama 问题修复工具")
        print("=" * 50)
        
        # 1. 检查安装
        if not self.check_ollama_installation():
            print("\n❌ 修复失败: Ollama未安装")
            print("请先安装Ollama: https://ollama.ai/")
            return False
        
        # 2. 检查服务
        service_running = self.check_ollama_service()
        if not service_running:
            if not self.start_ollama_service():
                print("\n❌ 修复失败: 无法启动Ollama服务")
                return False
        
        # 3. 测试连接
        if not await self.test_api_connection():
            print("\n❌ 修复失败: API连接异常")
            print("请检查防火墙设置或手动重启Ollama服务")
            return False
        
        # 4. 检查模型
        models = await self.check_models()
        has_default = self.default_model in models
        
        # 5. 安装默认模型（如果需要）
        if not has_default:
            if not self.install_default_model():
                print("\n⚠️  警告: 默认模型安装失败，但基本功能可用")
        
        # 最终验证
        print("\n🔍 最终验证...")
        final_models = await self.check_models()
        
        if final_models:
            print("\n✅ 修复完成！Ollama配置正常")
            print(f"   • 服务地址: {self.base_url}")
            print(f"   • 可用模型: {len(final_models)} 个")
            if self.default_model in final_models:
                print(f"   • 默认模型: {self.default_model} ✓")
            print("\n💡 现在可以在NovelCraft中正常使用AI功能了")
            return True
        else:
            print("\n⚠️  部分修复完成，但未检测到可用模型")
            print("请手动下载模型: ollama pull llama2")
            return False

async def main():
    """主函数"""
    fixer = OllamaFixer()
    
    try:
        success = await fixer.run_full_fix()
        if success:
            print("\n🎉 修复成功！")
        else:
            print("\n❌ 修复未完全成功，请查看上述建议")
    except KeyboardInterrupt:
        print("\n\n⏹️  修复被用户中断")
    except Exception as e:
        print(f"\n\n❌ 修复过程中发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())
