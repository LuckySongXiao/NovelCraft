"""
项目数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from typing import Dict, Any, List

from .base import BaseModel, TaggedMixin, VersionedMixin


class ProjectType(str, Enum):
    """项目类型枚举"""
    FANTASY = "fantasy"          # 奇幻
    WUXIA = "wuxia"             # 武侠
    XIANXIA = "xianxia"         # 仙侠
    SCIFI = "scifi"             # 科幻
    MODERN = "modern"           # 现代
    HISTORICAL = "historical"    # 历史
    ROMANCE = "romance"         # 言情
    MYSTERY = "mystery"         # 悬疑
    HORROR = "horror"           # 恐怖
    OTHER = "other"             # 其他


class ProjectStatus(str, Enum):
    """项目状态枚举"""
    PLANNING = "planning"        # 规划中
    WRITING = "writing"         # 写作中
    REVIEWING = "reviewing"     # 审阅中
    COMPLETED = "completed"     # 已完成
    PUBLISHED = "published"     # 已发布
    ARCHIVED = "archived"       # 已归档


class Project(BaseModel, TaggedMixin, VersionedMixin):
    """项目模型"""

    __tablename__ = "projects"

    # 基本信息
    name = Column(String(255), nullable=False, index=True, comment="项目名称")
    title = Column(String(500), comment="小说标题")
    subtitle = Column(String(500), comment="副标题")
    author = Column(String(100), comment="作者")

    # 项目属性
    project_type = Column(SQLEnum(ProjectType), default=ProjectType.FANTASY, comment="项目类型")
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PLANNING, comment="项目状态")

    # 描述信息
    summary = Column(Text, comment="简介")
    description = Column(Text, comment="详细描述")
    outline = Column(Text, comment="大纲")

    # 统计信息
    word_count = Column(Integer, default=0, comment="字数统计")
    chapter_count = Column(Integer, default=0, comment="章节数量")
    character_count = Column(Integer, default=0, comment="人物数量")

    # 设置信息
    settings = Column(JSON, comment="项目设置，JSON格式")
    project_metadata = Column(JSON, comment="元数据，JSON格式")

    # 模板信息
    template_id = Column(Integer, comment="使用的模板ID")
    template_name = Column(String(100), comment="模板名称")

    # 预置项目标识
    is_preset = Column(Boolean, default=False, comment="是否为预置项目")

    # 关联关系
    # world_settings = relationship("WorldSetting", back_populates="project")
    # characters = relationship("Character", back_populates="project")
    # factions = relationship("Faction", back_populates="project")
    # plots = relationship("Plot", back_populates="project")
    # chapters = relationship("Chapter", back_populates="project")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.settings:
            self.settings = self.get_default_settings()
        if not self.project_metadata:
            self.project_metadata = {}

    def get_default_settings(self) -> Dict[str, Any]:
        """获取默认设置"""
        return {
            "ai_enabled": True,
            "auto_save": True,
            "auto_backup": True,
            "consistency_check": True,
            "word_count_target": 100000,
            "chapter_target": 50,
            "writing_style": "third_person",
            "language": "zh-CN",
            "theme": "default"
        }

    def get_setting(self, key: str, default=None):
        """获取设置值"""
        if self.settings and key in self.settings:
            return self.settings[key]
        return default

    def set_setting(self, key: str, value: Any):
        """设置配置值"""
        if not self.settings:
            self.settings = {}
        self.settings[key] = value

    def get_metadata(self, key: str, default=None):
        """获取元数据"""
        if self.project_metadata and key in self.project_metadata:
            return self.project_metadata[key]
        return default

    def set_metadata(self, key: str, value: Any):
        """设置元数据"""
        if not self.project_metadata:
            self.project_metadata = {}
        self.project_metadata[key] = value

    def update_statistics(self):
        """更新统计信息"""
        # 这里需要根据关联的数据更新统计信息
        # 在实际使用时会通过服务层来实现
        pass

    def get_progress(self) -> Dict[str, Any]:
        """获取项目进度"""
        target_words = self.get_setting("word_count_target", 100000)
        target_chapters = self.get_setting("chapter_target", 50)

        return {
            "word_progress": (self.word_count / target_words * 100) if target_words > 0 else 0,
            "chapter_progress": (self.chapter_count / target_chapters * 100) if target_chapters > 0 else 0,
            "status": self.status.value,
            "completion_rate": self.calculate_completion_rate()
        }

    def calculate_completion_rate(self) -> float:
        """计算完成率"""
        if self.status == ProjectStatus.COMPLETED:
            return 100.0
        elif self.status == ProjectStatus.PUBLISHED:
            return 100.0
        elif self.status == ProjectStatus.WRITING:
            # 基于字数和章节数计算
            word_rate = min(self.word_count / self.get_setting("word_count_target", 100000), 1.0)
            chapter_rate = min(self.chapter_count / self.get_setting("chapter_target", 50), 1.0)
            return (word_rate + chapter_rate) / 2 * 100
        else:
            return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典，包含额外信息"""
        result = super().to_dict()
        result["progress"] = self.get_progress()
        result["tags"] = self.get_tags()
        return result
