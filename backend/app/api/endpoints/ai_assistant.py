"""
AI 助手 API 端点
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import logging

from ...services.ai_service import ai_manager

logger = logging.getLogger(__name__)
router = APIRouter()


def build_kwargs(request):
    """构建AI参数"""
    kwargs = {}
    if request.max_tokens:
        kwargs["max_tokens"] = request.max_tokens
    if request.temperature:
        kwargs["temperature"] = request.temperature
    if hasattr(request, 'top_p') and request.top_p:
        kwargs["top_p"] = request.top_p
    if hasattr(request, 'frequency_penalty') and request.frequency_penalty:
        kwargs["frequency_penalty"] = request.frequency_penalty
    if hasattr(request, 'presence_penalty') and request.presence_penalty:
        kwargs["presence_penalty"] = request.presence_penalty
    return kwargs


class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """聊天请求模型"""
    messages: List[ChatMessage]
    project_id: Optional[int] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None


class GenerateRequest(BaseModel):
    """生成请求模型"""
    prompt: str
    project_id: Optional[int] = None
    context_type: Optional[str] = None  # setting, character, plot, chapter
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None


class ProviderSwitchRequest(BaseModel):
    """切换提供商请求模型"""
    provider: str


class ConfigUpdateRequest(BaseModel):
    """配置更新请求模型"""
    provider: str
    config: dict


@router.get("/providers")
async def get_providers():
    """获取可用的AI提供商列表"""
    try:
        providers = ai_manager.get_available_providers()
        current = ai_manager.get_current_provider()
        return {
            "providers": providers,
            "current": current,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"获取AI提供商列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取AI提供商列表失败")


@router.post("/switch-provider")
async def switch_provider(request: ProviderSwitchRequest):
    """切换AI提供商"""
    try:
        await ai_manager.switch_provider(request.provider)
        return {
            "message": f"已切换到 {request.provider}",
            "current_provider": ai_manager.get_current_provider(),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"切换AI提供商失败: {e}")
        raise HTTPException(status_code=400, detail=f"切换AI提供商失败: {str(e)}")


@router.post("/config")
async def update_config(request: ConfigUpdateRequest):
    """更新AI配置"""
    try:
        # 更新配置到AI管理器
        await ai_manager.update_provider_config(request.provider, request.config)
        return {
            "message": f"已更新 {request.provider} 配置",
            "status": "success"
        }
    except Exception as e:
        logger.error(f"更新AI配置失败: {e}")
        raise HTTPException(status_code=400, detail=f"更新AI配置失败: {str(e)}")


@router.get("/config/{provider}")
async def get_config(provider: str):
    """获取指定提供商的配置"""
    try:
        config = ai_manager.get_provider_config(provider)
        return {
            "provider": provider,
            "config": config,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"获取AI配置失败: {e}")
        raise HTTPException(status_code=400, detail=f"获取AI配置失败: {str(e)}")


@router.get("/status")
async def get_ai_status():
    """获取AI服务状态"""
    try:
        is_connected = await ai_manager.check_connection()
        return {
            "provider": ai_manager.get_current_provider(),
            "connected": is_connected,
            "status": "online" if is_connected else "offline"
        }
    except Exception as e:
        logger.error(f"检查AI服务状态失败: {e}")
        return {
            "provider": ai_manager.get_current_provider(),
            "connected": False,
            "status": "error",
            "error": str(e)
        }


@router.get("/ollama/models")
async def get_ollama_models():
    """获取Ollama本地可用模型列表"""
    try:
        logger.info("开始获取Ollama模型列表...")

        # 详细诊断
        from ...core.config import settings
        logger.info(f"使用Ollama配置: base_url={settings.ollama_base_url}, model={settings.ollama_model}")

        models = await ai_manager.get_ollama_models()
        logger.info(f"获取到 {len(models) if models else 0} 个模型")

        # 检查是否获取到模型
        if not models:
            logger.warning("未检测到Ollama模型")

            # 尝试直接使用命令行获取模型列表作为备用方案
            import subprocess
            try:
                logger.info("尝试使用命令行方式获取Ollama模型...")
                result = subprocess.run(['ollama', 'list'],
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout.strip():
                    cmd_models = []
                    lines = result.stdout.strip().split('\n')

                    # 跳过标题行
                    for line in lines[1:]:  # 跳过 "NAME ID SIZE MODIFIED" 这一行
                        if line.strip():
                            # 解析格式: "mollysama/rwkv-7-g1:0.4B    bed9c223e852    501 MB    3 weeks ago"
                            parts = line.split()
                            if len(parts) >= 4:
                                name = parts[0]
                                model_id = parts[1]
                                size_str = parts[2] + " " + parts[3]  # "501 MB"
                                modified = " ".join(parts[4:])  # "3 weeks ago"

                                # 转换大小为字节
                                size_bytes = 0
                                try:
                                    if "MB" in size_str:
                                        size_bytes = int(float(parts[2]) * 1024 * 1024)
                                    elif "GB" in size_str:
                                        size_bytes = int(float(parts[2]) * 1024 * 1024 * 1024)
                                except:
                                    size_bytes = 0

                                cmd_models.append({
                                    "name": name,
                                    "size": size_bytes,
                                    "modified_at": modified,
                                    "digest": model_id,
                                    "details": {}
                                })
                                logger.info(f"解析模型: {name} ({size_str})")

                    if cmd_models:
                        logger.info(f"通过命令行获取到 {len(cmd_models)} 个模型")
                        return {
                            "models": cmd_models,
                            "count": len(cmd_models),
                            "status": "success",
                            "message": f"通过命令行方式检测到 {len(cmd_models)} 个本地模型",
                            "source": "command_line",
                            "note": "由于Ollama API服务问题，使用命令行方式获取模型列表"
                        }
                else:
                    logger.warning(f"命令行获取模型失败: {result.stderr}")
            except Exception as cmd_error:
                logger.warning(f"命令行方式获取模型失败: {cmd_error}")

            return {
                "models": [],
                "count": 0,
                "status": "warning",
                "message": "未检测到本地Ollama模型",
                "suggestions": [
                    "请确保Ollama服务正在运行: ollama serve",
                    "检查Ollama服务地址配置 (默认: http://localhost:11434)",
                    f"下载默认模型: ollama pull mollysama/rwkv-7-g1:0.4B",
                    "或下载其他模型: ollama pull llama2",
                    "查看可用模型: ollama list",
                    "检查防火墙是否阻止端口11434",
                    "尝试重启Ollama服务"
                ]
            }

        # 检查是否包含默认模型
        default_model = "mollysama/rwkv-7-g1:0.4B"
        has_default = any(model.get("name") == default_model for model in models)

        result = {
            "models": models,
            "count": len(models),
            "status": "success",
            "message": f"成功检测到 {len(models)} 个本地模型",
            "has_default_model": has_default,
            "default_model": default_model
        }

        if not has_default:
            result["suggestions"] = [
                f"建议下载默认模型: ollama pull {default_model}",
                "默认模型具有更好的中文支持和较小的资源占用"
            ]

        return result
    except Exception as e:
        error_msg = str(e)
        logger.error(f"获取Ollama模型列表失败: {error_msg}")

        # 根据错误类型提供不同的建议
        suggestions = []
        if "Connection" in error_msg or "连接" in error_msg:
            suggestions = [
                "Ollama服务未启动，请运行: ollama serve",
                "检查Ollama是否已安装: ollama --version",
                "如未安装，请访问: https://ollama.ai/",
                "检查端口11434是否被占用"
            ]
        elif "timeout" in error_msg.lower() or "超时" in error_msg:
            suggestions = [
                "连接超时，请检查Ollama服务状态",
                "重启Ollama服务: 先停止再运行 ollama serve",
                "检查系统资源使用情况"
            ]
        elif "404" in error_msg:
            suggestions = [
                "API端点不存在，请检查Ollama版本",
                "更新Ollama到最新版本",
                "确认Ollama服务正常运行"
            ]
        else:
            suggestions = [
                "请安装Ollama: https://ollama.ai/",
                "启动Ollama服务: ollama serve",
                "下载模型: ollama pull mollysama/rwkv-7-g1:0.4B",
                "检查防火墙设置",
                "查看Ollama日志获取详细错误信息"
            ]

        return {
            "models": [],
            "count": 0,
            "status": "error",
            "error": error_msg,
            "suggestions": suggestions
        }


@router.get("/ollama/test-connection")
async def test_ollama_connection():
    """测试Ollama连接状态"""
    try:
        from ...services.ai_service import OllamaService
        from ...core.config import settings

        # 创建临时Ollama服务实例进行测试
        ollama_config = {
            "base_url": settings.ollama_base_url,
            "model": settings.ollama_model
        }
        ollama_service = OllamaService(ollama_config)

        # 测试连接
        is_connected = await ollama_service.check_connection()

        if is_connected:
            # 获取模型列表
            models = await ollama_service.get_available_models()
            return {
                "status": "success",
                "connected": True,
                "message": "Ollama连接正常",
                "service_url": settings.ollama_base_url,
                "models_count": len(models),
                "models": [model.get("name") for model in models[:5]]  # 只返回前5个模型名称
            }
        else:
            return {
                "status": "error",
                "connected": False,
                "message": "无法连接到Ollama服务",
                "service_url": settings.ollama_base_url,
                "suggestions": [
                    "检查Ollama是否已安装",
                    "启动Ollama服务: ollama serve",
                    "确认服务地址正确",
                    "检查防火墙设置"
                ]
            }
    except Exception as e:
        logger.error(f"测试Ollama连接失败: {e}")
        return {
            "status": "error",
            "connected": False,
            "message": f"连接测试失败: {str(e)}",
            "service_url": getattr(settings, 'ollama_base_url', 'http://localhost:11434'),
            "suggestions": [
                "请安装Ollama: https://ollama.ai/",
                "启动Ollama服务: ollama serve",
                "检查网络连接",
                "查看详细错误日志"
            ]
        }


@router.get("/ollama/models/{model_name}")
async def get_ollama_model_info(model_name: str):
    """获取Ollama指定模型的详细信息"""
    try:
        model_info = await ai_manager.get_ollama_model_info(model_name)
        if model_info is None:
            raise HTTPException(status_code=404, detail=f"模型 {model_name} 不存在")

        return {
            "model": model_info,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取Ollama模型信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取Ollama模型信息失败: {str(e)}")


@router.post("/chat")
async def chat_completion(request: ChatRequest):
    """AI聊天对话"""
    try:
        # 检查AI服务状态
        if not await ai_manager.check_connection():
            raise HTTPException(
                status_code=503,
                detail=f"AI服务 ({ai_manager.get_current_provider()}) 连接失败，请检查配置和网络连接"
            )

        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        kwargs = build_kwargs(request)

        # 使用思维链处理
        result = await ai_manager.chat_completion_with_thinking(messages, **kwargs)

        return {
            "response": result["content"],
            "thinking": result["thinking"],
            "raw_response": result["raw_response"],
            "provider": ai_manager.get_current_provider(),
            "status": "success"
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"AI配置错误: {e}")
        raise HTTPException(status_code=400, detail=f"AI配置错误: {str(e)}")
    except Exception as e:
        logger.error(f"AI聊天对话失败: {e}")
        raise HTTPException(status_code=500, detail=f"AI聊天对话失败: {str(e)}")


@router.post("/generate-setting")
async def generate_setting(request: GenerateRequest):
    """AI生成设定"""
    try:
        # 检查AI服务状态
        if not await ai_manager.check_connection():
            raise HTTPException(
                status_code=503,
                detail=f"AI服务 ({ai_manager.get_current_provider()}) 连接失败，请检查配置和网络连接"
            )

        # 构建设定生成的提示词
        prompt = f"""
请根据以下要求生成小说世界设定：

{request.prompt}

请生成详细的世界设定，包括：
1. 世界观背景
2. 地理环境
3. 历史文化
4. 政治体系
5. 经济制度
6. 特殊规则或法则

请用中文回答，格式清晰，内容丰富。
"""

        kwargs = build_kwargs(request)
        result = await ai_manager.generate_text_with_thinking(prompt, **kwargs)

        return {
            "content": result["content"],
            "thinking": result["thinking"],
            "raw_response": result["raw_response"],
            "type": "world_setting",
            "provider": ai_manager.get_current_provider(),
            "status": "success"
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"AI配置错误: {e}")
        raise HTTPException(status_code=400, detail=f"AI配置错误: {str(e)}")
    except Exception as e:
        logger.error(f"AI生成设定失败: {e}")
        raise HTTPException(status_code=500, detail=f"AI生成设定失败: {str(e)}")


@router.post("/generate-character")
async def generate_character(request: GenerateRequest):
    """AI生成人物"""
    try:
        # 检查AI服务状态
        if not await ai_manager.check_connection():
            raise HTTPException(
                status_code=503,
                detail=f"AI服务 ({ai_manager.get_current_provider()}) 连接失败，请检查配置和网络连接"
            )

        prompt = f"""
请根据以下要求生成小说人物：

{request.prompt}

请生成详细的人物设定，包括：
1. 基本信息（姓名、年龄、性别、身份）
2. 外貌特征
3. 性格特点
4. 能力技能
5. 背景故事
6. 人际关系
7. 成长轨迹

请用中文回答，格式清晰，人物形象生动。
"""

        kwargs = build_kwargs(request)
        result = await ai_manager.generate_text_with_thinking(prompt, **kwargs)

        return {
            "content": result["content"],
            "thinking": result["thinking"],
            "raw_response": result["raw_response"],
            "type": "character",
            "provider": ai_manager.get_current_provider(),
            "status": "success"
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"AI配置错误: {e}")
        raise HTTPException(status_code=400, detail=f"AI配置错误: {str(e)}")
    except Exception as e:
        logger.error(f"AI生成人物失败: {e}")
        raise HTTPException(status_code=500, detail=f"AI生成人物失败: {str(e)}")


@router.post("/generate-plot")
async def generate_plot(request: GenerateRequest):
    """AI生成剧情"""
    try:
        # 检查AI服务状态
        if not await ai_manager.check_connection():
            raise HTTPException(
                status_code=503,
                detail=f"AI服务 ({ai_manager.get_current_provider()}) 连接失败，请检查配置和网络连接"
            )

        prompt = f"""
请根据以下要求生成小说剧情：

{request.prompt}

请生成详细的剧情大纲，包括：
1. 主要情节线
2. 关键转折点
3. 人物冲突
4. 情节发展
5. 高潮设计
6. 结局安排

请用中文回答，剧情逻辑清晰，富有张力。
"""

        kwargs = build_kwargs(request)
        result = await ai_manager.generate_text_with_thinking(prompt, **kwargs)

        return {
            "content": result["content"],
            "thinking": result["thinking"],
            "raw_response": result["raw_response"],
            "type": "plot",
            "provider": ai_manager.get_current_provider(),
            "status": "success"
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"AI配置错误: {e}")
        raise HTTPException(status_code=400, detail=f"AI配置错误: {str(e)}")
    except Exception as e:
        logger.error(f"AI生成剧情失败: {e}")
        raise HTTPException(status_code=500, detail=f"AI生成剧情失败: {str(e)}")


@router.post("/continue-writing")
async def continue_writing(request: GenerateRequest):
    """AI续写"""
    try:
        # 检查AI服务状态
        if not await ai_manager.check_connection():
            raise HTTPException(
                status_code=503,
                detail=f"AI服务 ({ai_manager.get_current_provider()}) 连接失败，请检查配置和网络连接"
            )

        prompt = f"""
请根据以下内容进行续写：

{request.prompt}

续写要求：
1. 保持文风一致
2. 情节自然流畅
3. 人物性格符合设定
4. 推进故事发展
5. 保持悬念和张力

请用中文续写，文笔流畅，情节合理。
"""

        kwargs = build_kwargs(request)
        result = await ai_manager.generate_text_with_thinking(prompt, **kwargs)

        return {
            "content": result["content"],
            "thinking": result["thinking"],
            "raw_response": result["raw_response"],
            "type": "continuation",
            "provider": ai_manager.get_current_provider(),
            "status": "success"
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"AI配置错误: {e}")
        raise HTTPException(status_code=400, detail=f"AI配置错误: {str(e)}")
    except Exception as e:
        logger.error(f"AI续写失败: {e}")
        raise HTTPException(status_code=500, detail=f"AI续写失败: {str(e)}")


@router.post("/check-consistency")
async def check_consistency(request: GenerateRequest):
    """AI一致性检查"""
    try:
        # 检查AI服务状态
        if not await ai_manager.check_connection():
            raise HTTPException(
                status_code=503,
                detail=f"AI服务 ({ai_manager.get_current_provider()}) 连接失败，请检查配置和网络连接"
            )

        prompt = f"""
请检查以下内容的一致性：

{request.prompt}

检查要点：
1. 人物设定是否前后一致
2. 世界观设定是否有矛盾
3. 时间线是否合理
4. 情节逻辑是否通顺
5. 细节描述是否冲突

请指出发现的问题并提供修改建议。
"""

        kwargs = build_kwargs(request)
        result = await ai_manager.generate_text_with_thinking(prompt, **kwargs)

        return {
            "content": result["content"],
            "thinking": result["thinking"],
            "raw_response": result["raw_response"],
            "type": "consistency_check",
            "provider": ai_manager.get_current_provider(),
            "status": "success"
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"AI配置错误: {e}")
        raise HTTPException(status_code=400, detail=f"AI配置错误: {str(e)}")
    except Exception as e:
        logger.error(f"AI一致性检查失败: {e}")
        raise HTTPException(status_code=500, detail=f"AI一致性检查失败: {str(e)}")
