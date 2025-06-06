"""
卷宗数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum
from datetime import datetime

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class VolumeStatus(str, Enum):
    """卷宗状态枚举"""
    PLANNING = "planning"       # 规划中
    WRITING = "writing"         # 写作中
    COMPLETED = "completed"     # 已完成
    REVIEWING = "reviewing"     # 审阅中
    REVISED = "revised"         # 已修订
    PUBLISHED = "published"     # 已发布


class Volume(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """卷宗模型"""

    __tablename__ = "volumes"

    # 基本信息
    title = Column(String(500), nullable=False, comment="卷宗标题")
    subtitle = Column(String(500), comment="副标题")
    volume_number = Column(Integer, nullable=False, comment="卷序号")
    status = Column(String(20), default=VolumeStatus.PLANNING.value, comment="卷宗状态")

    # 内容信息
    summary = Column(Text, comment="卷宗摘要")
    outline = Column(Text, comment="卷宗大纲")
    theme = Column(String(200), comment="主题")
    notes = Column(Text, comment="作者备注")

    # 统计信息
    total_chapters = Column(Integer, default=0, comment="总章节数")
    completed_chapters = Column(Integer, default=0, comment="已完成章节数")
    total_words = Column(Integer, default=0, comment="总字数")
    target_words = Column(Integer, comment="目标字数")

    # 时间信息
    start_date = Column(DateTime, comment="开始时间")
    end_date = Column(DateTime, comment="结束时间")
    deadline = Column(DateTime, comment="截止时间")

    # 剧情要素
    main_characters = Column(JSON, comment="主要角色")
    key_events = Column(JSON, comment="关键事件")
    plot_threads = Column(JSON, comment="剧情线索")
    conflicts = Column(JSON, comment="冲突设定")

    # 设定关联
    world_elements = Column(JSON, comment="世界观元素")
    cultivation_elements = Column(JSON, comment="修炼体系元素")
    faction_elements = Column(JSON, comment="势力元素")

    # 关系
    chapters = relationship("Chapter", back_populates="volume", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Volume(id={self.id}, title='{self.title}', volume_number={self.volume_number})>"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "subtitle": self.subtitle,
            "volume_number": self.volume_number,
            "status": self.status,
            "summary": self.summary,
            "outline": self.outline,
            "theme": self.theme,
            "notes": self.notes,
            "total_chapters": self.total_chapters,
            "completed_chapters": self.completed_chapters,
            "total_words": self.total_words,
            "target_words": self.target_words,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "main_characters": self.main_characters or [],
            "key_events": self.key_events or [],
            "plot_threads": self.plot_threads or [],
            "conflicts": self.conflicts or [],
            "world_elements": self.world_elements or [],
            "cultivation_elements": self.cultivation_elements or [],
            "faction_elements": self.faction_elements or [],
            "progress": self.calculate_progress()
        })
        return base_dict

    def calculate_progress(self) -> float:
        """计算完成进度"""
        if self.total_chapters == 0:
            return 0.0
        return round((self.completed_chapters / self.total_chapters) * 100, 2)

    def calculate_score(self) -> float:
        """计算卷宗评分"""
        score = 0.0
        
        # 基础信息完整性 (30%)
        if self.title:
            score += 10
        if self.summary:
            score += 10
        if self.outline:
            score += 10
        
        # 内容完整性 (40%)
        if self.main_characters:
            score += 10
        if self.key_events:
            score += 10
        if self.plot_threads:
            score += 10
        if self.total_chapters > 0:
            score += 10
        
        # 进度完成度 (30%)
        progress = self.calculate_progress()
        score += progress * 0.3
        
        return round(score, 2)

    def update_statistics(self):
        """更新统计信息"""
        if self.chapters:
            self.total_chapters = len(self.chapters)
            self.completed_chapters = len([c for c in self.chapters if c.status in ['completed', 'published']])
            self.total_words = sum(c.word_count or 0 for c in self.chapters)

    def validate_data(self) -> List[str]:
        """验证数据有效性"""
        errors = []
        
        # 基本验证
        if not self.title or not self.title.strip():
            errors.append("卷宗标题不能为空")
        
        if self.volume_number is None or self.volume_number <= 0:
            errors.append("卷序号必须大于0")
        
        # 字数验证
        if self.target_words and self.target_words <= 0:
            errors.append("目标字数必须大于0")
        
        # 时间验证
        if self.start_date and self.end_date and self.start_date > self.end_date:
            errors.append("开始时间不能晚于结束时间")
        
        if self.deadline and self.start_date and self.deadline < self.start_date:
            errors.append("截止时间不能早于开始时间")
        
        return errors

    def check_consistency(self, project_data: Dict[str, Any] = None) -> List[str]:
        """检查一致性"""
        issues = []
        
        # 检查角色一致性
        if project_data and "characters" in project_data:
            project_character_names = [char["name"] for char in project_data["characters"]]
            for char_name in (self.main_characters or []):
                if char_name not in project_character_names:
                    issues.append(f"主要角色 {char_name} 在项目中不存在")
        
        # 检查卷序号唯一性
        if self.volume_number and self.volume_number <= 0:
            issues.append("卷序号应大于0")
        
        # 检查状态一致性
        if self.status == VolumeStatus.COMPLETED.value and self.completed_chapters < self.total_chapters:
            issues.append("卷宗状态为已完成，但仍有未完成的章节")
        
        # 检查标题
        if not self.title:
            issues.append("卷宗缺少标题")
        
        return issues

    def get_next_chapter_number(self) -> int:
        """获取下一个章节序号"""
        if not self.chapters:
            return 1
        return max(c.chapter_number for c in self.chapters if c.chapter_number) + 1

    def get_chapters_by_status(self, status: str) -> List:
        """根据状态获取章节"""
        return [c for c in self.chapters if c.status == status]

    def get_word_count_by_status(self) -> Dict[str, int]:
        """按状态统计字数"""
        stats = {}
        for chapter in self.chapters:
            status = chapter.status
            if status not in stats:
                stats[status] = 0
            stats[status] += chapter.word_count or 0
        return stats
