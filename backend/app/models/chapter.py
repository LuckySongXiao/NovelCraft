"""
章节数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum
from datetime import datetime

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class ChapterStatus(str, Enum):
    """章节状态枚举"""
    DRAFT = "draft"             # 草稿
    WRITING = "writing"         # 写作中
    COMPLETED = "completed"     # 已完成
    REVIEWING = "reviewing"     # 审阅中
    REVISED = "revised"         # 已修订
    PUBLISHED = "published"     # 已发布


class Chapter(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """章节模型"""

    __tablename__ = "chapters"

    # 基本信息
    title = Column(String(500), comment="章节标题")
    subtitle = Column(String(500), comment="副标题")
    chapter_number = Column(Integer, comment="章节序号")
    volume_id = Column(Integer, ForeignKey("volumes.id"), comment="所属卷宗ID")
    status = Column(String(20), default=ChapterStatus.DRAFT.value, comment="章节状态")

    # 内容信息
    content = Column(Text, comment="章节内容")
    summary = Column(Text, comment="章节摘要")
    outline = Column(Text, comment="章节大纲")
    notes = Column(Text, comment="作者备注")

    # 统计信息
    word_count = Column(Integer, default=0, comment="字数")
    character_count = Column(Integer, default=0, comment="字符数")
    paragraph_count = Column(Integer, default=0, comment="段落数")
    estimated_reading_time = Column(Integer, default=0, comment="预估阅读时间(分钟)")

    # 剧情信息
    plot_points = Column(JSON, comment="剧情要点")
    character_appearances = Column(JSON, comment="出场角色")
    location_settings = Column(JSON, comment="场景设定")
    time_setting = Column(String(200), comment="时间设定")

    # 写作信息
    writing_date = Column(DateTime, comment="写作日期")
    last_edited = Column(DateTime, comment="最后编辑时间")
    edit_count = Column(Integer, default=0, comment="编辑次数")

    # 质量评估
    quality_score = Column(Float, default=0, comment="质量评分")
    readability_score = Column(Float, default=0, comment="可读性评分")
    consistency_score = Column(Float, default=0, comment="一致性评分")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    plot_id = Column(Integer, ForeignKey("plots.id"), comment="剧情ID")
    previous_chapter_id = Column(Integer, ForeignKey("chapters.id"), comment="上一章ID")
    next_chapter_id = Column(Integer, ForeignKey("chapters.id"), comment="下一章ID")

    # 发布信息
    published_date = Column(DateTime, comment="发布日期")
    published_platform = Column(String(100), comment="发布平台")
    view_count = Column(Integer, default=0, comment="阅读量")
    like_count = Column(Integer, default=0, comment="点赞数")
    comment_count = Column(Integer, default=0, comment="评论数")

    # 关系
    volume = relationship("Volume", back_populates="chapters")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.plot_points:
            self.plot_points = []
        if not self.character_appearances:
            self.character_appearances = []
        if not self.location_settings:
            self.location_settings = []

        # 设置写作日期
        if not self.writing_date:
            self.writing_date = datetime.now()

    def update_content(self, content: str):
        """更新章节内容"""
        self.content = content
        self.last_edited = datetime.now()
        self.edit_count += 1
        self._calculate_statistics()

    def _calculate_statistics(self):
        """计算统计信息"""
        if self.content:
            # 字数统计
            self.word_count = len(self.content.replace(" ", "").replace("\n", ""))
            self.character_count = len(self.content)

            # 段落统计
            self.paragraph_count = len([p for p in self.content.split("\n") if p.strip()])

            # 预估阅读时间（按每分钟300字计算）
            self.estimated_reading_time = max(1, self.word_count // 300)

    def add_plot_point(self, plot_point: Dict[str, Any]):
        """添加剧情要点"""
        self.plot_points.append(plot_point)

    def add_character_appearance(self, character_id: int, role: str, importance: str = "normal"):
        """添加出场角色"""
        appearance_data = {
            "character_id": character_id,
            "role": role,
            "importance": importance
        }
        if appearance_data not in self.character_appearances:
            self.character_appearances.append(appearance_data)

    def add_location_setting(self, location_name: str, description: str = ""):
        """添加场景设定"""
        location_data = {
            "name": location_name,
            "description": description
        }
        if location_data not in self.location_settings:
            self.location_settings.append(location_data)

    def get_main_characters(self) -> List[int]:
        """获取主要角色ID列表"""
        main_characters = []
        for appearance in self.character_appearances:
            if appearance.get("importance") in ["high", "main"]:
                main_characters.append(appearance.get("character_id"))
        return main_characters

    def get_chapter_summary(self) -> str:
        """获取章节摘要"""
        if self.summary:
            return self.summary

        # 自动生成简单摘要
        summary_parts = []

        # 主要角色
        main_chars = len(self.get_main_characters())
        if main_chars > 0:
            summary_parts.append(f"{main_chars}个主要角色")

        # 场景数量
        if self.location_settings:
            summary_parts.append(f"{len(self.location_settings)}个场景")

        # 剧情要点
        if self.plot_points:
            summary_parts.append(f"{len(self.plot_points)}个剧情要点")

        # 字数
        if self.word_count > 0:
            summary_parts.append(f"{self.word_count}字")

        return " | ".join(summary_parts) if summary_parts else "暂无摘要"

    def calculate_quality_score(self) -> float:
        """计算质量评分"""
        score = 0

        # 基于字数（合理范围内加分）
        if 1000 <= self.word_count <= 5000:
            score += 20
        elif 500 <= self.word_count < 1000:
            score += 15
        elif self.word_count > 5000:
            score += 10

        # 基于内容完整性
        if self.content and self.title:
            score += 20

        if self.summary:
            score += 10

        if self.outline:
            score += 10

        # 基于剧情要点
        score += min(len(self.plot_points) * 5, 20)

        # 基于角色出场
        score += min(len(self.character_appearances) * 3, 15)

        # 基于编辑次数（适度编辑加分）
        if 1 <= self.edit_count <= 5:
            score += 5
        elif self.edit_count > 5:
            score += 2

        self.quality_score = min(score, 100)
        return self.quality_score

    def calculate_readability_score(self) -> float:
        """计算可读性评分"""
        if not self.content:
            return 0

        score = 50  # 基础分

        # 段落长度分析
        paragraphs = [p.strip() for p in self.content.split("\n") if p.strip()]
        if paragraphs:
            avg_paragraph_length = sum(len(p) for p in paragraphs) / len(paragraphs)
            if 50 <= avg_paragraph_length <= 200:
                score += 20
            elif 200 < avg_paragraph_length <= 300:
                score += 10

        # 句子长度分析（简单实现）
        sentences = self.content.replace("。", "。|").replace("！", "！|").replace("？", "？|").split("|")
        sentences = [s.strip() for s in sentences if s.strip()]
        if sentences:
            avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)
            if 10 <= avg_sentence_length <= 50:
                score += 20
            elif 50 < avg_sentence_length <= 80:
                score += 10

        # 对话比例
        dialogue_count = self.content.count('"') + self.content.count("'")
        if dialogue_count > 0:
            dialogue_ratio = dialogue_count / len(self.content) * 1000
            if 5 <= dialogue_ratio <= 30:
                score += 10

        self.readability_score = min(score, 100)
        return self.readability_score

    def check_consistency(self, project_data: Dict[str, Any] = None) -> List[str]:
        """检查一致性"""
        issues = []

        # 检查角色一致性
        if project_data and "characters" in project_data:
            project_character_ids = [char["id"] for char in project_data["characters"]]
            for appearance in self.character_appearances:
                char_id = appearance.get("character_id")
                if char_id not in project_character_ids:
                    issues.append(f"角色ID {char_id} 在项目中不存在")

        # 检查章节顺序
        if self.chapter_number and self.chapter_number <= 0:
            issues.append("章节序号应大于0")

        # 检查内容完整性
        if not self.content and self.status in [ChapterStatus.COMPLETED.value, ChapterStatus.PUBLISHED.value]:
            issues.append("已完成/已发布的章节不应为空")

        # 检查标题
        if not self.title:
            issues.append("章节缺少标题")

        return issues

    def get_reading_progress(self, current_position: int) -> float:
        """获取阅读进度百分比"""
        if not self.content or current_position <= 0:
            return 0.0

        progress = (current_position / len(self.content)) * 100
        return min(progress, 100.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = super().to_dict()
        result["chapter_summary"] = self.get_chapter_summary()
        result["quality_score"] = self.calculate_quality_score()
        result["readability_score"] = self.calculate_readability_score()
        result["main_character_count"] = len(self.get_main_characters())
        result["consistency_issues"] = self.check_consistency()
        result["tags"] = self.get_tags()
        return result
