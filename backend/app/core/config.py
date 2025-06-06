"""
应用配置模块
"""
from typing import Optional, List


class Settings:
    """应用设置类"""

    # 应用基本信息
    app_name: str = "NovelCraft"
    app_version: str = "1.0.0"
    description: str = "小说管理系统"

    # 服务器配置
    host: str = "localhost"
    port: int = 8000
    debug: bool = True

    # 数据库配置
    database_url: str = "sqlite:///./novelcraft.db"
    database_echo: bool = False

    # 安全配置
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS配置
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]

    # AI配置 - 多平台支持
    # OpenAI配置
    openai_api_key: Optional[str] = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-3.5-turbo"

    # Claude配置
    claude_api_key: Optional[str] = None
    claude_base_url: str = "https://api.anthropic.com"
    claude_model: str = "claude-3-sonnet-20240229"

    # 智谱AI配置
    zhipu_api_key: Optional[str] = None
    zhipu_base_url: str = "https://open.bigmodel.cn/api/paas/v4"
    zhipu_model: str = "glm-4"

    # 硅基流动配置
    siliconflow_api_key: Optional[str] = None
    siliconflow_base_url: str = "https://api.siliconflow.cn/v1"
    siliconflow_model: str = "deepseek-chat"

    # 谷歌AI配置
    google_api_key: Optional[str] = None
    google_base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    google_model: str = "gemini-pro"

    # GROK配置
    grok_api_key: Optional[str] = None
    grok_base_url: str = "https://api.x.ai/v1"
    grok_model: str = "grok-beta"

    # Ollama配置
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mollysama/rwkv-7-g1:0.4B"

    # 自定义OpenAI兼容接口配置
    custom_api_key: Optional[str] = None
    custom_base_url: Optional[str] = None
    custom_model: Optional[str] = None

    # 默认AI提供商和模型
    default_ai_provider: str = "ollama"  # openai, claude, zhipu, siliconflow, google, grok, ollama, custom
    default_ai_model: str = "mollysama/rwkv-7-g1:0.4B"
    max_tokens: int = 2000
    temperature: float = 0.7

    # AI功能开关
    ai_enabled: bool = True
    ai_auto_save: bool = True
    ai_consistency_check: bool = True

    # 文件存储配置
    upload_dir: str = "./uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [".txt", ".md", ".docx", ".pdf"]

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"

    # 缓存配置
    cache_ttl: int = 3600  # 1小时

    # 分页配置
    default_page_size: int = 20
    max_page_size: int = 100


# 创建全局设置实例
settings = Settings()


def get_settings() -> Settings:
    """获取设置实例"""
    return settings


# 数据库配置
DATABASE_CONFIG = {
    "url": settings.database_url,
    "echo": settings.database_echo,
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

# AI模型配置 - 多平台支持
AI_PROVIDERS_CONFIG = {
    "openai": {
        "api_key": settings.openai_api_key,
        "base_url": settings.openai_base_url,
        "model": settings.openai_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    },
    "claude": {
        "api_key": settings.claude_api_key,
        "base_url": settings.claude_base_url,
        "model": settings.claude_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    },
    "zhipu": {
        "api_key": settings.zhipu_api_key,
        "base_url": settings.zhipu_base_url,
        "model": settings.zhipu_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    },
    "siliconflow": {
        "api_key": settings.siliconflow_api_key,
        "base_url": settings.siliconflow_base_url,
        "model": settings.siliconflow_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    },
    "google": {
        "api_key": settings.google_api_key,
        "base_url": settings.google_base_url,
        "model": settings.google_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    },
    "grok": {
        "api_key": settings.grok_api_key,
        "base_url": settings.grok_base_url,
        "model": settings.grok_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    },
    "ollama": {
        "base_url": settings.ollama_base_url,
        "model": settings.ollama_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    },
    "custom": {
        "api_key": settings.custom_api_key,
        "base_url": settings.custom_base_url,
        "model": settings.custom_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    }
}

# 默认AI配置
AI_CONFIG = {
    "provider": settings.default_ai_provider,
    "enabled": settings.ai_enabled,
    "auto_save": settings.ai_auto_save,
    "consistency_check": settings.ai_consistency_check,
    "providers": AI_PROVIDERS_CONFIG
}

# 文件上传配置
UPLOAD_CONFIG = {
    "dir": settings.upload_dir,
    "max_size": settings.max_file_size,
    "allowed_types": settings.allowed_file_types,
}
