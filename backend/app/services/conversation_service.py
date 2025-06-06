"""
智能对话引擎服务
实现AI助手与用户的智能对话，引导用户完成项目创建和设定管理
"""
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from enum import Enum
import logging
import json
from datetime import datetime

from .ai_project_service import AIProjectService
from .ai_service import ai_manager
from ..models.project import Project

logger = logging.getLogger(__name__)


class ConversationStage(Enum):
    """对话阶段枚举"""
    INIT = "init"                           # 初始化
    THEME_SETTING = "theme_setting"         # 主题确定
    WORLD_BUILDING = "world_building"       # 世界构建
    SYSTEM_DESIGN = "system_design"         # 体系设计
    CHARACTER_CREATION = "character_creation" # 人物创建
    FACTION_SETUP = "faction_setup"         # 势力设置
    TIMELINE_PLANNING = "timeline_planning" # 时间线规划
    STRUCTURE_DESIGN = "structure_design"   # 结构设计
    PLOT_PLANNING = "plot_planning"         # 剧情规划
    CONTENT_CREATION = "content_creation"   # 内容创作
    COMPLETED = "completed"                 # 完成


class ConversationContext:
    """对话上下文"""

    def __init__(self):
        self.stage = ConversationStage.INIT
        self.project_id: Optional[int] = None
        self.user_preferences: Dict[str, Any] = {}
        self.collected_data: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.current_questions: List[str] = []
        self.pending_confirmations: List[Dict[str, Any]] = []


class ConversationService:
    """智能对话引擎服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.ai_project_service = AIProjectService(db)
        self.ai_manager = ai_manager
        self.contexts: Dict[str, ConversationContext] = {}  # 用户会话上下文

    def start_conversation(self, user_id: str, project_id: Optional[int] = None) -> Dict[str, Any]:
        """开始智能对话"""
        # 创建或重置对话上下文
        context = ConversationContext()

        if project_id:
            # 如果指定了项目，设置为当前项目
            context.project_id = project_id
            context.stage = ConversationStage.WORLD_BUILDING
            self.ai_project_service.set_current_project(project_id)
        else:
            # 新项目创建流程
            context.stage = ConversationStage.THEME_SETTING

        self.contexts[user_id] = context

        # 生成初始问题
        initial_response = self._generate_stage_questions(context)

        return {
            "session_id": user_id,
            "stage": context.stage.value,
            "message": initial_response["message"],
            "questions": initial_response["questions"],
            "options": initial_response.get("options", [])
        }

    async def process_user_input(self, user_id: str, user_input: str, additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """处理用户输入"""
        if user_id not in self.contexts:
            raise ValueError("对话会话不存在，请先开始对话")

        context = self.contexts[user_id]

        # 记录用户输入
        context.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "user_input",
            "stage": context.stage.value,
            "content": user_input,
            "additional_data": additional_data
        })

        # 分析用户输入
        analysis_result = await self._analyze_user_input(context, user_input, additional_data)

        # 更新收集的数据
        if analysis_result.get("extracted_data"):
            self._update_collected_data(context, analysis_result["extracted_data"])

        # 检查是否可以进入下一阶段
        stage_completion = self._check_stage_completion(context)

        if stage_completion["is_complete"]:
            # 保存当前阶段的数据
            self._save_stage_data(context)

            # 进入下一阶段
            next_stage = self._get_next_stage(context.stage)
            if next_stage:
                context.stage = next_stage
                response = self._generate_stage_questions(context)
            else:
                # 对话完成
                response = self._finalize_conversation(context)
        else:
            # 继续当前阶段的对话
            response = self._continue_current_stage(context, analysis_result)

        # 记录AI响应
        context.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "ai_response",
            "stage": context.stage.value,
            "content": response
        })

        return {
            "session_id": user_id,
            "stage": context.stage.value,
            "message": response["message"],
            "questions": response.get("questions", []),
            "options": response.get("options", []),
            "progress": self._calculate_progress(context),
            "collected_data": context.collected_data
        }

    async def _analyze_user_input(self, context: ConversationContext, user_input: str, additional_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """分析用户输入，提取关键信息"""
        try:
            # 使用AI服务分析用户输入
            ai_service = self.ai_manager.get_current_service()

            analysis_prompt = f"""
            分析以下用户输入，提取关键信息：

            当前对话阶段：{context.stage.value}
            用户输入：{user_input}
            附加数据：{json.dumps(additional_data or {}, ensure_ascii=False)}

            请提取以下信息：
            1. 用户意图
            2. 关键实体和概念
            3. 情感倾向
            4. 创作偏好
            5. 具体的设定信息

            返回JSON格式的分析结果。
            """

            analysis_result = await ai_service.generate_text(analysis_prompt)

            # 尝试解析JSON结果
            try:
                return json.loads(analysis_result)
            except json.JSONDecodeError:
                # 如果解析失败，返回基础分析
                return {
                    "user_intent": "continue_conversation",
                    "extracted_data": {"raw_input": user_input},
                    "sentiment": "neutral",
                    "confidence": 0.5
                }

        except Exception as e:
            logger.error(f"分析用户输入时出错: {e}")
            return {
                "user_intent": "continue_conversation",
                "extracted_data": {"raw_input": user_input},
                "sentiment": "neutral",
                "confidence": 0.0,
                "error": str(e)
            }

    def _generate_stage_questions(self, context: ConversationContext) -> Dict[str, Any]:
        """根据当前阶段生成问题"""
        stage_templates = {
            ConversationStage.THEME_SETTING: {
                "message": "让我们开始创建您的小说项目！首先，请告诉我您想创作什么类型的小说？",
                "questions": [
                    "您希望创作什么类型的小说？（奇幻、武侠、科幻、现代等）",
                    "有什么特别的灵感或想法吗？",
                    "希望传达什么样的主题或情感？"
                ],
                "options": ["奇幻", "武侠", "科幻", "现代", "历史", "其他"]
            },
            ConversationStage.WORLD_BUILDING: {
                "message": "现在让我们构建您小说的世界观。请描述一下故事发生的世界。",
                "questions": [
                    "这个故事发生在什么样的世界？",
                    "是现实世界还是虚构世界？",
                    "有什么特殊的自然法则或规律吗？",
                    "主要故事发生在哪些地方？"
                ]
            },
            ConversationStage.SYSTEM_DESIGN: {
                "message": "让我们设计小说中的各种体系设定。",
                "questions": [
                    "这个世界的政治结构是怎样的？",
                    "使用什么货币体系？",
                    "角色有什么特殊能力或修炼体系？",
                    "有哪些主要的种族或势力？"
                ]
            },
            ConversationStage.CHARACTER_CREATION: {
                "message": "现在让我们创建小说中的主要角色。",
                "questions": [
                    "主角是什么样的人？",
                    "主角有什么特殊背景或能力？",
                    "有哪些重要的配角？",
                    "主要的对手或反派是谁？"
                ]
            },
            ConversationStage.STRUCTURE_DESIGN: {
                "message": "让我们规划小说的整体结构。",
                "questions": [
                    "您希望小说分为几个部分或卷？",
                    "每个部分大概要讲什么内容？",
                    "整体的故事发展节奏是怎样的？"
                ]
            }
        }

        return stage_templates.get(context.stage, {
            "message": "请继续我们的对话。",
            "questions": ["还有什么需要补充的吗？"]
        })

    def _update_collected_data(self, context: ConversationContext, extracted_data: Dict[str, Any]):
        """更新收集的数据"""
        stage_key = context.stage.value

        if stage_key not in context.collected_data:
            context.collected_data[stage_key] = {}

        context.collected_data[stage_key].update(extracted_data)

    def _check_stage_completion(self, context: ConversationContext) -> Dict[str, Any]:
        """检查当前阶段是否完成"""
        stage_data = context.collected_data.get(context.stage.value, {})

        # 简单的完成度检查（可以根据具体需求优化）
        required_fields = {
            ConversationStage.THEME_SETTING: ["project_type", "theme"],
            ConversationStage.WORLD_BUILDING: ["world_type", "setting"],
            ConversationStage.SYSTEM_DESIGN: ["political_system", "currency_system"],
            ConversationStage.CHARACTER_CREATION: ["main_character", "supporting_characters"],
            ConversationStage.STRUCTURE_DESIGN: ["volume_structure", "chapter_plan"]
        }

        required = required_fields.get(context.stage, [])
        completed_fields = [field for field in required if field in stage_data]

        completion_rate = len(completed_fields) / len(required) if required else 1.0

        return {
            "is_complete": completion_rate >= 0.7,  # 70%完成度即可进入下一阶段
            "completion_rate": completion_rate,
            "missing_fields": [field for field in required if field not in stage_data]
        }

    def _save_stage_data(self, context: ConversationContext):
        """保存当前阶段的数据到项目中"""
        if not context.project_id:
            return

        try:
            stage_data = context.collected_data.get(context.stage.value, {})

            # 根据阶段类型保存到相应的数据模型
            if context.stage == ConversationStage.WORLD_BUILDING:
                self.ai_project_service.write_project_data("world_setting", stage_data)
            elif context.stage == ConversationStage.CHARACTER_CREATION:
                if "characters" in stage_data:
                    for char_data in stage_data["characters"]:
                        self.ai_project_service.write_project_data("character", char_data)
            # 添加更多阶段的数据保存逻辑

        except Exception as e:
            logger.error(f"保存阶段数据时出错: {e}")

    def _get_next_stage(self, current_stage: ConversationStage) -> Optional[ConversationStage]:
        """获取下一个对话阶段"""
        stage_order = [
            ConversationStage.THEME_SETTING,
            ConversationStage.WORLD_BUILDING,
            ConversationStage.SYSTEM_DESIGN,
            ConversationStage.CHARACTER_CREATION,
            ConversationStage.FACTION_SETUP,
            ConversationStage.TIMELINE_PLANNING,
            ConversationStage.STRUCTURE_DESIGN,
            ConversationStage.PLOT_PLANNING,
            ConversationStage.CONTENT_CREATION,
            ConversationStage.COMPLETED
        ]

        try:
            current_index = stage_order.index(current_stage)
            if current_index < len(stage_order) - 1:
                return stage_order[current_index + 1]
        except ValueError:
            pass

        return None

    def _continue_current_stage(self, context: ConversationContext, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """继续当前阶段的对话"""
        # 生成后续问题
        return self._generate_stage_questions(context)

    def _finalize_conversation(self, context: ConversationContext) -> Dict[str, Any]:
        """完成对话"""
        return {
            "message": "恭喜！我们已经完成了项目的基础设置。现在您可以开始创作了！",
            "questions": [],
            "is_completed": True
        }

    def _calculate_progress(self, context: ConversationContext) -> float:
        """计算对话进度"""
        total_stages = len(ConversationStage) - 1  # 排除COMPLETED阶段
        current_stage_index = list(ConversationStage).index(context.stage)
        return min(current_stage_index / total_stages, 1.0)

    def get_conversation_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取对话总结"""
        if user_id not in self.contexts:
            return None

        context = self.contexts[user_id]

        return {
            "session_id": user_id,
            "current_stage": context.stage.value,
            "progress": self._calculate_progress(context),
            "collected_data": context.collected_data,
            "conversation_length": len(context.conversation_history),
            "project_id": context.project_id
        }

    def end_conversation(self, user_id: str) -> bool:
        """结束对话"""
        if user_id in self.contexts:
            del self.contexts[user_id]
            return True
        return False
