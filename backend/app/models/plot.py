"""
剧情数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class PlotType(str, Enum):
    """剧情类型枚举"""
    MAIN = "main"               # 主线
    SUB = "sub"                 # 支线
    SIDE = "side"               # 旁支
    BACKGROUND = "background"   # 背景
    FLASHBACK = "flashback"     # 回忆
    FORESHADOWING = "foreshadowing" # 伏笔


class PlotStatus(str, Enum):
    """剧情状态枚举"""
    PLANNED = "planned"         # 已规划
    WRITING = "writing"         # 写作中
    COMPLETED = "completed"     # 已完成
    REVISED = "revised"         # 已修订
    ABANDONED = "abandoned"     # 已废弃


class Plot(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """剧情模型"""

    __tablename__ = "plots"

    # 基本信息
    plot_type = Column(SQLEnum(PlotType), default=PlotType.SUB, comment="剧情类型")
    status = Column(SQLEnum(PlotStatus), default=PlotStatus.PLANNED, comment="剧情状态")
    priority = Column(Integer, default=1, comment="优先级")

    # 剧情结构
    summary = Column(Text, comment="剧情摘要")
    outline = Column(Text, comment="详细大纲")
    theme = Column(String(200), comment="主题")
    conflict = Column(Text, comment="核心冲突")
    resolution = Column(Text, comment="解决方案")

    # 剧情要素
    protagonists = Column(JSON, comment="主要角色")
    antagonists = Column(JSON, comment="对立角色")
    supporting_characters = Column(JSON, comment="配角")
    locations = Column(JSON, comment="主要场景")

    # 时间线
    start_time = Column(String(100), comment="开始时间")
    end_time = Column(String(100), comment="结束时间")
    duration = Column(String(100), comment="持续时间")
    timeline_events = Column(JSON, comment="时间线事件")

    # 剧情发展
    setup = Column(Text, comment="铺垫")
    rising_action = Column(Text, comment="上升动作")
    climax = Column(Text, comment="高潮")
    falling_action = Column(Text, comment="下降动作")
    resolution_detail = Column(Text, comment="结局")

    # 关联关系
    parent_plot_id = Column(Integer, ForeignKey("plots.id"), comment="父剧情ID")
    related_plots = Column(JSON, comment="相关剧情")

    # 影响与后果
    consequences = Column(JSON, comment="后果影响")
    character_changes = Column(JSON, comment="角色变化")
    world_changes = Column(JSON, comment="世界变化")

    # 写作信息
    word_count = Column(Integer, default=0, comment="字数")
    chapter_count = Column(Integer, default=0, comment="章节数")
    estimated_length = Column(Integer, comment="预估长度")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    children = relationship("Plot", backref="parent", remote_side="Plot.id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.protagonists:
            self.protagonists = []
        if not self.antagonists:
            self.antagonists = []
        if not self.supporting_characters:
            self.supporting_characters = []
        if not self.locations:
            self.locations = []
        if not self.timeline_events:
            self.timeline_events = []
        if not self.related_plots:
            self.related_plots = []
        if not self.consequences:
            self.consequences = []
        if not self.character_changes:
            self.character_changes = []
        if not self.world_changes:
            self.world_changes = []

    def add_character(self, character_id: int, role: str):
        """添加角色"""
        character_data = {"id": character_id, "role": role}

        if role in ["protagonist", "hero", "main"]:
            if character_data not in self.protagonists:
                self.protagonists.append(character_data)
        elif role in ["antagonist", "villain", "enemy"]:
            if character_data not in self.antagonists:
                self.antagonists.append(character_data)
        else:
            if character_data not in self.supporting_characters:
                self.supporting_characters.append(character_data)

    def add_location(self, location_name: str, importance: str = "normal"):
        """添加场景"""
        location_data = {"name": location_name, "importance": importance}
        if location_data not in self.locations:
            self.locations.append(location_data)

    def add_timeline_event(self, event_data: Dict[str, Any]):
        """添加时间线事件"""
        self.timeline_events.append(event_data)
        # 按时间排序
        self.timeline_events.sort(key=lambda x: x.get("time", ""))

    def add_related_plot(self, plot_id: int, relationship_type: str):
        """添加相关剧情"""
        relation_data = {"plot_id": plot_id, "type": relationship_type}
        if relation_data not in self.related_plots:
            self.related_plots.append(relation_data)

    def add_consequence(self, consequence_data: Dict[str, Any]):
        """添加后果"""
        self.consequences.append(consequence_data)

    def add_character_change(self, character_id: int, change_data: Dict[str, Any]):
        """添加角色变化"""
        change_record = {
            "character_id": character_id,
            "changes": change_data
        }
        self.character_changes.append(change_record)

    def get_all_characters(self) -> List[int]:
        """获取所有相关角色ID"""
        character_ids = []

        for char in self.protagonists:
            character_ids.append(char.get("id"))
        for char in self.antagonists:
            character_ids.append(char.get("id"))
        for char in self.supporting_characters:
            character_ids.append(char.get("id"))

        return list(set(character_ids))  # 去重

    def get_character_role(self, character_id: int) -> str:
        """获取角色在剧情中的作用"""
        for char in self.protagonists:
            if char.get("id") == character_id:
                return "protagonist"
        for char in self.antagonists:
            if char.get("id") == character_id:
                return "antagonist"
        for char in self.supporting_characters:
            if char.get("id") == character_id:
                return "supporting"
        return "unknown"

    def calculate_complexity_score(self) -> float:
        """计算剧情复杂度"""
        score = 0

        # 基于角色数量
        total_characters = len(self.protagonists) + len(self.antagonists) + len(self.supporting_characters)
        score += total_characters * 5

        # 基于场景数量
        score += len(self.locations) * 3

        # 基于时间线事件数量
        score += len(self.timeline_events) * 2

        # 基于相关剧情数量
        score += len(self.related_plots) * 4

        # 基于字数
        score += (self.word_count or 0) * 0.001

        # 基于剧情类型
        type_multiplier = {
            PlotType.MAIN: 2.0,
            PlotType.SUB: 1.5,
            PlotType.SIDE: 1.0,
            PlotType.BACKGROUND: 0.5,
            PlotType.FLASHBACK: 0.8,
            PlotType.FORESHADOWING: 1.2
        }
        score *= type_multiplier.get(self.plot_type, 1.0)

        return score

    def get_progress_percentage(self) -> float:
        """获取完成进度百分比"""
        if self.status == PlotStatus.COMPLETED:
            return 100.0
        elif self.status == PlotStatus.ABANDONED:
            return 0.0
        elif self.status == PlotStatus.WRITING:
            if self.estimated_length and self.word_count:
                return min((self.word_count / self.estimated_length) * 100, 95.0)
            return 50.0  # 默认进度
        elif self.status == PlotStatus.PLANNED:
            return 10.0
        else:
            return 0.0

    def validate_plot_consistency(self) -> List[str]:
        """验证剧情一致性"""
        issues = []

        # 检查是否有主角
        if not self.protagonists:
            issues.append("剧情缺少主角")

        # 检查时间线一致性
        if self.start_time and self.end_time:
            # 这里可以添加时间逻辑检查
            pass

        # 检查角色冲突
        protagonist_ids = [char.get("id") for char in self.protagonists]
        antagonist_ids = [char.get("id") for char in self.antagonists]

        overlap = set(protagonist_ids) & set(antagonist_ids)
        if overlap:
            issues.append(f"角色同时是主角和反派: {overlap}")

        # 检查必要元素
        if not self.conflict:
            issues.append("剧情缺少核心冲突")

        if not self.summary:
            issues.append("剧情缺少摘要")

        return issues

    def generate_outline_structure(self) -> Dict[str, Any]:
        """生成大纲结构"""
        return {
            "setup": {
                "description": self.setup,
                "characters": self.protagonists,
                "locations": [loc for loc in self.locations if loc.get("importance") == "high"]
            },
            "rising_action": {
                "description": self.rising_action,
                "events": [event for event in self.timeline_events if event.get("phase") == "rising"]
            },
            "climax": {
                "description": self.climax,
                "conflict": self.conflict
            },
            "falling_action": {
                "description": self.falling_action,
                "consequences": self.consequences
            },
            "resolution": {
                "description": self.resolution_detail,
                "character_changes": self.character_changes,
                "world_changes": self.world_changes
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["complexity_score"] = self.calculate_complexity_score()
        result["progress_percentage"] = self.get_progress_percentage()
        result["consistency_issues"] = self.validate_plot_consistency()
        result["outline_structure"] = self.generate_outline_structure()
        result["character_count"] = len(self.get_all_characters())
        result["tags"] = self.get_tags()
        return result
