"""
势力组织数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class FactionType(str, Enum):
    """势力类型枚举"""
    SECT = "sect"               # 宗门
    FAMILY = "family"           # 家族
    EMPIRE = "empire"           # 帝国
    KINGDOM = "kingdom"         # 王国
    GUILD = "guild"             # 公会
    ORGANIZATION = "organization" # 组织
    ALLIANCE = "alliance"       # 联盟
    MERCENARY = "mercenary"     # 雇佣兵团
    CULT = "cult"               # 邪教
    ACADEMY = "academy"         # 学院
    OTHER = "other"             # 其他


class FactionStatus(str, Enum):
    """势力状态枚举"""
    ACTIVE = "active"           # 活跃
    DECLINING = "declining"     # 衰落
    RISING = "rising"           # 崛起
    DESTROYED = "destroyed"     # 覆灭
    DORMANT = "dormant"         # 蛰伏
    UNKNOWN = "unknown"         # 未知


class Faction(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """势力组织模型"""

    __tablename__ = "factions"

    # 基本信息
    full_name = Column(String(300), comment="全称")
    short_name = Column(String(100), comment="简称")
    faction_type = Column(SQLEnum(FactionType), default=FactionType.ORGANIZATION, comment="势力类型")
    status = Column(SQLEnum(FactionStatus), default=FactionStatus.ACTIVE, comment="势力状态")

    # 基础属性
    founded_date = Column(String(100), comment="成立时间")
    founder = Column(String(200), comment="创始人")
    current_leader = Column(String(200), comment="当前领导者")
    headquarters = Column(String(300), comment="总部位置")

    # 组织结构
    hierarchy = Column(JSON, comment="组织架构")
    positions = Column(JSON, comment="职位体系")
    members = Column(JSON, comment="成员信息")
    member_count = Column(Integer, default=0, comment="成员数量")

    # 实力评估
    power_level = Column(Float, default=0, comment="整体实力")
    influence_level = Column(Float, default=0, comment="影响力")
    territory = Column(JSON, comment="势力范围")
    resources = Column(JSON, comment="拥有资源")

    # 理念文化
    ideology = Column(Text, comment="理念宗旨")
    culture = Column(JSON, comment="组织文化")
    traditions = Column(JSON, comment="传统习俗")
    rules = Column(JSON, comment="组织规则")

    # 历史发展
    history = Column(Text, comment="发展历史")
    major_events = Column(JSON, comment="重大事件")
    achievements = Column(JSON, comment="主要成就")
    failures = Column(JSON, comment="重大失败")

    # 对外关系
    allies = Column(JSON, comment="盟友势力")
    enemies = Column(JSON, comment="敌对势力")
    neutral_relations = Column(JSON, comment="中立关系")

    # 经济状况
    wealth_level = Column(Float, default=0, comment="财富水平")
    income_sources = Column(JSON, comment="收入来源")
    expenses = Column(JSON, comment="主要支出")

    # 军事力量
    military_strength = Column(JSON, comment="军事实力")
    special_forces = Column(JSON, comment="特殊部队")
    weapons = Column(JSON, comment="武器装备")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    parent_faction_id = Column(Integer, ForeignKey("factions.id"), comment="上级势力ID")

    children = relationship("Faction", backref="parent", remote_side="Faction.id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.hierarchy:
            self.hierarchy = {}
        if not self.positions:
            self.positions = []
        if not self.members:
            self.members = []
        if not self.territory:
            self.territory = {}
        if not self.resources:
            self.resources = {}
        if not self.culture:
            self.culture = {}
        if not self.traditions:
            self.traditions = []
        if not self.rules:
            self.rules = []
        if not self.major_events:
            self.major_events = []
        if not self.achievements:
            self.achievements = []
        if not self.failures:
            self.failures = []
        if not self.allies:
            self.allies = []
        if not self.enemies:
            self.enemies = []
        if not self.neutral_relations:
            self.neutral_relations = []
        if not self.income_sources:
            self.income_sources = []
        if not self.expenses:
            self.expenses = []
        if not self.military_strength:
            self.military_strength = {}
        if not self.special_forces:
            self.special_forces = []
        if not self.weapons:
            self.weapons = []

    def get_display_name(self) -> str:
        """获取显示名称"""
        if self.short_name:
            return self.short_name
        elif self.full_name:
            return self.full_name
        else:
            return self.name

    def add_member(self, member_data: Dict[str, Any]):
        """添加成员"""
        self.members.append(member_data)
        self.member_count = len(self.members)

    def remove_member(self, member_id: int):
        """移除成员"""
        self.members = [m for m in self.members if m.get("id") != member_id]
        self.member_count = len(self.members)

    def add_position(self, position_data: Dict[str, Any]):
        """添加职位"""
        self.positions.append(position_data)

    def add_major_event(self, event_data: Dict[str, Any]):
        """添加重大事件"""
        self.major_events.append(event_data)
        # 按时间排序
        self.major_events.sort(key=lambda x: x.get("date", ""))

    def set_relationship(self, target_faction: str, relationship_type: str, description: str = ""):
        """设置与其他势力的关系"""
        relationship_data = {
            "faction": target_faction,
            "type": relationship_type,
            "description": description
        }

        if relationship_type == "ally":
            if target_faction not in [ally.get("faction") for ally in self.allies]:
                self.allies.append(relationship_data)
        elif relationship_type == "enemy":
            if target_faction not in [enemy.get("faction") for enemy in self.enemies]:
                self.enemies.append(relationship_data)
        else:
            if target_faction not in [neutral.get("faction") for neutral in self.neutral_relations]:
                self.neutral_relations.append(relationship_data)

    def calculate_total_power(self) -> float:
        """计算总体实力"""
        # 基础实力
        base_power = self.power_level

        # 成员实力加成
        member_power = self.member_count * 10

        # 资源加成
        resource_power = len(self.resources) * 5

        # 领土加成
        territory_power = len(self.territory.get("regions", [])) * 20

        # 财富加成
        wealth_power = self.wealth_level * 0.1

        # 影响力加成
        influence_power = self.influence_level * 0.5

        total = base_power + member_power + resource_power + territory_power + wealth_power + influence_power
        return total

    def get_relationship_summary(self) -> Dict[str, int]:
        """获取关系摘要"""
        return {
            "allies": len(self.allies),
            "enemies": len(self.enemies),
            "neutral": len(self.neutral_relations)
        }

    def get_power_ranking(self, all_factions: List['Faction']) -> int:
        """获取实力排名"""
        faction_powers = [(faction.id, faction.calculate_total_power()) for faction in all_factions]
        faction_powers.sort(key=lambda x: x[1], reverse=True)

        for rank, (faction_id, power) in enumerate(faction_powers, 1):
            if faction_id == self.id:
                return rank
        return len(all_factions)

    def get_member_by_position(self, position: str) -> List[Dict[str, Any]]:
        """根据职位获取成员"""
        return [member for member in self.members if member.get("position") == position]

    def get_leader_info(self) -> Dict[str, Any]:
        """获取领导者信息"""
        leaders = self.get_member_by_position("leader") or self.get_member_by_position("宗主") or self.get_member_by_position("族长")
        if leaders:
            return leaders[0]
        return {"name": self.current_leader, "position": "领导者"}

    def calculate_influence_score(self) -> float:
        """计算影响力评分"""
        score = 0

        # 基于势力类型
        type_scores = {
            FactionType.EMPIRE: 100,
            FactionType.KINGDOM: 80,
            FactionType.SECT: 60,
            FactionType.FAMILY: 40,
            FactionType.GUILD: 30,
            FactionType.ORGANIZATION: 25,
            FactionType.ALLIANCE: 70,
            FactionType.ACADEMY: 50,
            FactionType.MERCENARY: 20,
            FactionType.CULT: 15,
            FactionType.OTHER: 10
        }
        score += type_scores.get(self.faction_type, 10)

        # 基于成员数量
        score += min(self.member_count, 1000) * 0.1

        # 基于盟友数量
        score += len(self.allies) * 5

        # 基于领土范围
        score += len(self.territory.get("regions", [])) * 10

        # 基于历史成就
        score += len(self.achievements) * 3

        return score

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["display_name"] = self.get_display_name()
        result["total_power"] = self.calculate_total_power()
        result["relationship_summary"] = self.get_relationship_summary()
        result["influence_score"] = self.calculate_influence_score()
        result["leader_info"] = self.get_leader_info()
        result["tags"] = self.get_tags()
        return result
