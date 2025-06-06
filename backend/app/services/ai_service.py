"""
AI服务抽象层 - 支持多平台AI模型调用
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union, Tuple
import httpx
import json
import logging
import re
from enum import Enum

from ..core.config import AI_CONFIG, AI_PROVIDERS_CONFIG

logger = logging.getLogger(__name__)


def process_thinking_chain(text: str) -> Tuple[str, Optional[str]]:
    """
    处理思维链内容，分离思维过程和最终结果

    Args:
        text: 原始AI响应文本

    Returns:
        Tuple[str, Optional[str]]: (最终结果, 思维过程)
    """
    # 匹配 <think>...</think> 标签
    think_pattern = r'<think>(.*?)</think>'
    thinking_matches = re.findall(think_pattern, text, re.DOTALL | re.IGNORECASE)

    # 移除思维链标签，获取纯净结果
    clean_text = re.sub(think_pattern, '', text, flags=re.DOTALL | re.IGNORECASE).strip()

    # 合并所有思维过程
    thinking_process = None
    if thinking_matches:
        thinking_process = '\n\n'.join(thinking_matches).strip()

    return clean_text, thinking_process


class AIProvider(str, Enum):
    """AI提供商枚举"""
    OPENAI = "openai"
    CLAUDE = "claude"
    ZHIPU = "zhipu"
    SILICONFLOW = "siliconflow"
    GOOGLE = "google"
    GROK = "grok"
    OLLAMA = "ollama"
    CUSTOM = "custom"


class AIServiceBase(ABC):
    """AI服务基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None

    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        pass

    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """聊天补全"""
        pass

    @abstractmethod
    async def check_connection(self) -> bool:
        """检查连接状态"""
        pass

    async def generate_text_with_thinking(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        生成文本并处理思维链

        Returns:
            Dict[str, Any]: {
                "content": str,  # 纯净的生成内容
                "thinking": Optional[str],  # 思维过程（如果有）
                "raw_response": str  # 原始响应
            }
        """
        raw_response = await self.generate_text(prompt, **kwargs)
        content, thinking = process_thinking_chain(raw_response)

        return {
            "content": content,
            "thinking": thinking,
            "raw_response": raw_response
        }

    async def chat_completion_with_thinking(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        聊天补全并处理思维链

        Returns:
            Dict[str, Any]: {
                "content": str,  # 纯净的生成内容
                "thinking": Optional[str],  # 思维过程（如果有）
                "raw_response": str  # 原始响应
            }
        """
        raw_response = await self.chat_completion(messages, **kwargs)
        content, thinking = process_thinking_chain(raw_response)

        return {
            "content": content,
            "thinking": thinking,
            "raw_response": raw_response
        }


class OpenAIService(AIServiceBase):
    """OpenAI服务实现"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://api.openai.com/v1")
        self.model = config.get("model", "gpt-3.5-turbo")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat_completion(messages, **kwargs)

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """聊天补全"""
        if not self.api_key:
            raise ValueError("OpenAI API密钥未配置")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.config.get("max_tokens", 2000)),
            "temperature": kwargs.get("temperature", self.config.get("temperature", 0.7))
        }

        # 添加高级参数支持
        if "top_p" in kwargs:
            data["top_p"] = kwargs["top_p"]
        if "frequency_penalty" in kwargs:
            data["frequency_penalty"] = kwargs["frequency_penalty"]
        if "presence_penalty" in kwargs:
            data["presence_penalty"] = kwargs["presence_penalty"]

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"OpenAI API调用失败: {e}")
                raise

    async def check_connection(self) -> bool:
        """检查连接状态"""
        try:
            await self.generate_text("测试连接", max_tokens=10)
            return True
        except Exception:
            return False


class ClaudeService(AIServiceBase):
    """Claude服务实现"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://api.anthropic.com")
        self.model = config.get("model", "claude-3-sonnet-20240229")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if not self.api_key:
            raise ValueError("Claude API密钥未配置")

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        data = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", self.config.get("max_tokens", 2000)),
            "messages": [{"role": "user", "content": prompt}]
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/v1/messages",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                return result["content"][0]["text"]
            except Exception as e:
                logger.error(f"Claude API调用失败: {e}")
                raise

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """聊天补全"""
        # 将消息转换为Claude格式
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        return await self.generate_text(prompt, **kwargs)

    async def check_connection(self) -> bool:
        """检查连接状态"""
        try:
            await self.generate_text("测试连接", max_tokens=10)
            return True
        except Exception:
            return False


class OllamaService(AIServiceBase):
    """Ollama服务实现"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", "llama2")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.get("temperature", 0.7)),
                "num_predict": kwargs.get("max_tokens", self.config.get("max_tokens", 2000)),
                "top_p": kwargs.get("top_p", 1.0),
                "repeat_penalty": kwargs.get("frequency_penalty", 0.0) + 1.0  # Ollama使用repeat_penalty
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=data,
                    timeout=120.0
                )
                response.raise_for_status()
                result = response.json()
                return result["response"]
            except Exception as e:
                logger.error(f"Ollama API调用失败: {e}")
                raise

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """聊天补全"""
        data = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.get("temperature", 0.7)),
                "num_predict": kwargs.get("max_tokens", self.config.get("max_tokens", 2000)),
                "top_p": kwargs.get("top_p", 1.0),
                "repeat_penalty": kwargs.get("frequency_penalty", 0.0) + 1.0  # Ollama使用repeat_penalty
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=data,
                    timeout=120.0
                )
                response.raise_for_status()
                result = response.json()
                return result["message"]["content"]
            except Exception as e:
                logger.error(f"Ollama API调用失败: {e}")
                raise

    async def check_connection(self) -> bool:
        """检查连接状态"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=10.0)
                response.raise_for_status()
                return True
        except Exception:
            return False

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """获取本地可用的模型列表"""
        try:
            # 增加连接超时时间和重试机制
            async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0)) as client:
                # 直接获取模型列表，不进行健康检查（因为Ollama根路径可能不支持GET请求）
                response = await client.get(f"{self.base_url}/api/tags", timeout=30.0)

                # 详细记录响应信息
                logger.info(f"Ollama API响应状态码: {response.status_code}")
                logger.info(f"Ollama API响应头: {dict(response.headers)}")

                if response.status_code == 502:
                    logger.error("Ollama服务返回502错误，可能服务未正确启动")
                    # 尝试重新启动Ollama服务的建议
                    return []

                response.raise_for_status()
                result = response.json()

                logger.info(f"Ollama API原始响应: {result}")

                models = []
                for model in result.get("models", []):
                    model_info = {
                        "name": model.get("name", ""),
                        "size": model.get("size", 0),
                        "modified_at": model.get("modified_at", ""),
                        "digest": model.get("digest", ""),
                        "details": model.get("details", {})
                    }
                    models.append(model_info)
                    logger.debug(f"处理模型: {model_info}")

                logger.info(f"成功获取到 {len(models)} 个Ollama模型")
                return models

        except httpx.ConnectError as e:
            logger.error(f"无法连接到Ollama服务 ({self.base_url}): {e}")
            logger.error("请检查: 1) Ollama是否已安装 2) 服务是否正在运行 3) 端口11434是否可用")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API HTTP错误: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 502:
                logger.error("502错误通常表示Ollama服务未正确启动，请尝试重启Ollama服务")
            elif e.response.status_code == 404:
                logger.error("404错误表示API端点不存在，请检查Ollama版本是否支持/api/tags端点")
            return []
        except httpx.TimeoutException as e:
            logger.error(f"连接Ollama服务超时: {e}")
            return []
        except Exception as e:
            logger.error(f"获取Ollama模型列表时发生未知错误: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            return []

    async def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """获取指定模型的详细信息"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/show",
                    json={"name": model_name},
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()

                logger.info(f"成功获取模型 {model_name} 的详细信息")
                return result
        except httpx.ConnectError:
            logger.warning(f"无法连接到Ollama服务 ({self.base_url})")
            return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"模型 {model_name} 不存在")
            else:
                logger.error(f"获取模型信息时API返回错误状态码: {e.response.status_code}")
            return None
        except httpx.TimeoutException:
            logger.warning(f"获取模型信息超时")
            return None
        except Exception as e:
            logger.error(f"获取模型 {model_name} 信息失败: {e}")
            return None




class ZhipuService(AIServiceBase):
    """智谱AI服务实现"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://open.bigmodel.cn/api/paas/v4")
        self.model = config.get("model", "glm-4")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat_completion(messages, **kwargs)

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """聊天补全"""
        if not self.api_key:
            raise ValueError("智谱AI API密钥未配置")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.config.get("max_tokens", 2000)),
            "temperature": kwargs.get("temperature", self.config.get("temperature", 0.7))
        }

        # 添加高级参数支持
        if "top_p" in kwargs:
            data["top_p"] = kwargs["top_p"]

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"智谱AI API调用失败: {e}")
                raise

    async def check_connection(self) -> bool:
        """检查连接状态"""
        try:
            await self.generate_text("测试连接", max_tokens=10)
            return True
        except Exception:
            return False


class SiliconFlowService(OpenAIService):
    """硅基流动服务实现（兼容OpenAI格式）"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "https://api.siliconflow.cn/v1")
        self.model = config.get("model", "deepseek-chat")


class GoogleService(AIServiceBase):
    """谷歌AI服务实现"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://generativelanguage.googleapis.com/v1beta")
        self.model = config.get("model", "gemini-pro")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if not self.api_key:
            raise ValueError("Google AI API密钥未配置")

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "maxOutputTokens": kwargs.get("max_tokens", self.config.get("max_tokens", 2000)),
                "temperature": kwargs.get("temperature", self.config.get("temperature", 0.7))
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                logger.error(f"Google AI API调用失败: {e}")
                raise

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """聊天补全"""
        # 将消息转换为Google格式
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        return await self.generate_text(prompt, **kwargs)

    async def check_connection(self) -> bool:
        """检查连接状态"""
        try:
            await self.generate_text("测试连接", max_tokens=10)
            return True
        except Exception:
            return False


class GrokService(OpenAIService):
    """GROK服务实现（兼容OpenAI格式）"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "https://api.x.ai/v1")
        self.model = config.get("model", "grok-beta")


class CustomService(OpenAIService):
    """自定义OpenAI兼容服务实现"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # 自定义服务可能不需要API密钥
        if not self.api_key:
            self.api_key = "dummy-key"


class AIServiceFactory:
    """AI服务工厂类"""

    _services = {
        AIProvider.OPENAI: OpenAIService,
        AIProvider.CLAUDE: ClaudeService,
        AIProvider.ZHIPU: ZhipuService,
        AIProvider.SILICONFLOW: SiliconFlowService,
        AIProvider.GOOGLE: GoogleService,
        AIProvider.GROK: GrokService,
        AIProvider.OLLAMA: OllamaService,
        AIProvider.CUSTOM: CustomService
    }

    @classmethod
    def create_service(cls, provider: Union[str, AIProvider], config: Optional[Dict[str, Any]] = None) -> AIServiceBase:
        """创建AI服务实例"""
        if isinstance(provider, str):
            provider = AIProvider(provider)

        if config is None:
            config = AI_PROVIDERS_CONFIG.get(provider.value, {})

        service_class = cls._services.get(provider)
        if not service_class:
            raise ValueError(f"不支持的AI提供商: {provider}")

        return service_class(config)


class AIManager:
    """AI管理器 - 统一的AI服务接口"""

    def __init__(self):
        self.current_provider = AI_CONFIG.get("provider", "ollama")
        self.service = None
        self.provider_configs = AI_PROVIDERS_CONFIG.copy()
        self._initialize_service()

    def _initialize_service(self):
        """初始化AI服务"""
        try:
            config = self.provider_configs.get(self.current_provider, {})
            self.service = AIServiceFactory.create_service(self.current_provider, config)
        except Exception as e:
            logger.error(f"初始化AI服务失败: {e}")
            self.service = None

    async def switch_provider(self, provider: Union[str, AIProvider]):
        """切换AI提供商"""
        self.current_provider = provider
        self._initialize_service()

    async def update_provider_config(self, provider: str, config: Dict[str, Any]):
        """更新提供商配置"""
        if provider not in self.provider_configs:
            raise ValueError(f"不支持的AI提供商: {provider}")

        # 更新配置
        self.provider_configs[provider].update(config)

        # 如果是当前提供商，重新初始化服务
        if provider == self.current_provider:
            self._initialize_service()

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """获取提供商配置"""
        if provider not in self.provider_configs:
            raise ValueError(f"不支持的AI提供商: {provider}")

        # 返回配置副本，隐藏敏感信息
        config = self.provider_configs[provider].copy()
        if 'api_key' in config and config['api_key']:
            config['api_key'] = '***' + config['api_key'][-4:] if len(config['api_key']) > 4 else '***'
        return config

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if not self.service:
            raise RuntimeError("AI服务未初始化")
        return await self.service.generate_text(prompt, **kwargs)

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """聊天补全"""
        if not self.service:
            raise RuntimeError("AI服务未初始化")
        return await self.service.chat_completion(messages, **kwargs)

    async def generate_text_with_thinking(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成文本并处理思维链"""
        if not self.service:
            raise RuntimeError("AI服务未初始化")
        return await self.service.generate_text_with_thinking(prompt, **kwargs)

    async def chat_completion_with_thinking(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """聊天补全并处理思维链"""
        if not self.service:
            raise RuntimeError("AI服务未初始化")
        return await self.service.chat_completion_with_thinking(messages, **kwargs)

    async def check_connection(self) -> bool:
        """检查连接状态"""
        if not self.service:
            return False
        return await self.service.check_connection()

    def get_available_providers(self) -> List[str]:
        """获取可用的AI提供商列表"""
        return list(self.provider_configs.keys())

    def get_current_provider(self) -> str:
        """获取当前AI提供商"""
        return self.current_provider

    async def get_ollama_models(self) -> List[Dict[str, Any]]:
        """获取Ollama本地可用模型列表"""
        try:
            # 创建临时的Ollama服务实例
            ollama_config = self.provider_configs.get("ollama", {})
            ollama_service = OllamaService(ollama_config)
            return await ollama_service.get_available_models()
        except Exception as e:
            logger.error(f"获取Ollama模型列表失败: {e}")
            return []

    async def get_ollama_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """获取Ollama指定模型的详细信息"""
        try:
            # 创建临时的Ollama服务实例
            ollama_config = self.provider_configs.get("ollama", {})
            ollama_service = OllamaService(ollama_config)
            return await ollama_service.get_model_info(model_name)
        except Exception as e:
            logger.error(f"获取Ollama模型信息失败: {e}")
            return None


# 全局AI管理器实例
ai_manager = AIManager()
