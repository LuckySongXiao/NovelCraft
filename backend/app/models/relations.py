"""
关系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum
from datetime import datetime

from .base import BaseModel


class RelationType(str, Enum):
    """关系类型枚举"""
    # 人物关系
    FAMILY = "family"               # 家庭关系
    FRIEND = "friend"              # 朋友
    ENEMY = "enemy"                # 敌人
    LOVER = "lover"                # 恋人
    MENTOR = "mentor"              # 师父
    STUDENT = "student"            # 学生
    COLLEAGUE = "colleague"        # 同事
    RIVAL = "rival"                # 对手
    ALLY = "ally"                  # 盟友
    SUBORDINATE = "subordinate"    # 下属
    SUPERIOR = "superior"          # 上级

    # 势力关系
    ALLIANCE = "alliance"          # 联盟
    HOSTILITY = "hostility"        # 敌对
    NEUTRAL = "neutral"            # 中立
    VASSAL = "vassal"              # 附庸
    OVERLORD = "overlord"          # 宗主
    TRADE = "trade"                # 贸易
    COMPETITION = "competition"    # 竞争


class RelationStatus(str, Enum):
    """关系状态枚举"""
    ACTIVE = "active"              # 活跃
    INACTIVE = "inactive"          # 不活跃
    BROKEN = "broken"              # 破裂
    DEVELOPING = "developing"      # 发展中
    STABLE = "stable"              # 稳定
    DETERIORATING = "deteriorating" # 恶化中


class CharacterRelation(BaseModel):
    """人物关系模型"""

    __tablename__ = "character_relations"

    # 关系双方
    character_a_id = Column(Integer, ForeignKey("characters.id"), comment="角色A的ID")
    character_b_id = Column(Integer, ForeignKey("characters.id"), comment="角色B的ID")

    # 关系属性
    relation_type = Column(String(50), comment="关系类型")
    relation_subtype = Column(String(100), comment="关系子类型")
    status = Column(String(20), default=RelationStatus.ACTIVE.value, comment="关系状态")

    # 关系强度和方向
    strength = Column(Float, default=0.5, comment="关系强度(0-1)")
    is_mutual = Column(Boolean, default=True, comment="是否相互关系")
    direction = Column(String(20), default="bidirectional", comment="关系方向")

    # 时间信息
    start_time = Column(String(100), comment="关系开始时间")
    end_time = Column(String(100), comment="关系结束时间")

    # 详细信息
    description = Column(Text, comment="关系描述")
    origin_story = Column(Text, comment="关系起源")
    key_events = Column(JSON, comment="关键事件")

    # 影响因素
    trust_level = Column(Float, default=0.5, comment="信任度(0-1)")
    intimacy_level = Column(Float, default=0.5, comment="亲密度(0-1)")
    conflict_level = Column(Float, default=0.0, comment="冲突度(0-1)")

    # 关联信息
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    related_plots = Column(JSON, comment="相关剧情")
    related_events = Column(JSON, comment="相关事件")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.key_events:
            self.key_events = []
        if not self.related_plots:
            self.related_plots = []
        if not self.related_events:
            self.related_events = []

    def add_key_event(self, event_data: Dict[str, Any]):
        """添加关键事件"""
        event_data.setdefault("timestamp", datetime.now().isoformat())
        self.key_events.append(event_data)
        # 按时间排序
        self.key_events.sort(key=lambda x: x.get("timestamp", ""))

    def update_strength(self, change: float, reason: str = ""):
        """更新关系强度"""
        old_strength = self.strength
        self.strength = max(0, min(1, self.strength + change))

        # 记录变化
        self.add_key_event({
            "type": "strength_change",
            "old_value": old_strength,
            "new_value": self.strength,
            "change": change,
            "reason": reason
        })

    def update_trust(self, change: float, reason: str = ""):
        """更新信任度"""
        old_trust = self.trust_level
        self.trust_level = max(0, min(1, self.trust_level + change))

        self.add_key_event({
            "type": "trust_change",
            "old_value": old_trust,
            "new_value": self.trust_level,
            "change": change,
            "reason": reason
        })

    def calculate_relationship_score(self) -> float:
        """计算关系综合评分"""
        # 基础评分基于关系强度
        base_score = self.strength * 50

        # 信任度加成
        trust_bonus = self.trust_level * 20

        # 亲密度加成
        intimacy_bonus = self.intimacy_level * 20

        # 冲突度减分
        conflict_penalty = self.conflict_level * 30

        # 关系类型调整
        type_multiplier = self._get_type_multiplier()

        total_score = (base_score + trust_bonus + intimacy_bonus - conflict_penalty) * type_multiplier
        return max(0, min(100, total_score))

    def _get_type_multiplier(self) -> float:
        """获取关系类型的评分倍数"""
        positive_relations = ["family", "friend", "lover", "mentor", "ally"]
        negative_relations = ["enemy", "rival"]

        if self.relation_type in positive_relations:
            return 1.2
        elif self.relation_type in negative_relations:
            return 0.8
        else:
            return 1.0

    def get_relationship_summary(self) -> str:
        """获取关系摘要"""
        summary_parts = []

        # 关系类型
        summary_parts.append(self.relation_type)

        # 关系强度
        if self.strength >= 0.8:
            summary_parts.append("强")
        elif self.strength >= 0.5:
            summary_parts.append("中")
        else:
            summary_parts.append("弱")

        # 状态
        if self.status != RelationStatus.ACTIVE.value:
            summary_parts.append(self.status)

        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["relationship_summary"] = self.get_relationship_summary()
        result["relationship_score"] = self.calculate_relationship_score()
        return result


class FactionRelation(BaseModel):
    """势力关系模型"""

    __tablename__ = "faction_relations"

    # 关系双方
    faction_a_id = Column(Integer, ForeignKey("factions.id"), comment="势力A的ID")
    faction_b_id = Column(Integer, ForeignKey("factions.id"), comment="势力B的ID")

    # 关系属性
    relation_type = Column(String(50), comment="关系类型")
    relation_subtype = Column(String(100), comment="关系子类型")
    status = Column(String(20), default=RelationStatus.ACTIVE.value, comment="关系状态")

    # 关系强度
    strength = Column(Float, default=0.5, comment="关系强度(0-1)")
    influence_level = Column(Float, default=0.5, comment="影响力水平")

    # 时间信息
    start_time = Column(String(100), comment="关系开始时间")
    end_time = Column(String(100), comment="关系结束时间")

    # 详细信息
    description = Column(Text, comment="关系描述")
    formal_agreement = Column(Text, comment="正式协议")
    key_events = Column(JSON, comment="关键事件")

    # 具体关系指标
    military_cooperation = Column(Float, default=0.0, comment="军事合作度")
    economic_cooperation = Column(Float, default=0.0, comment="经济合作度")
    political_alignment = Column(Float, default=0.0, comment="政治一致性")
    cultural_exchange = Column(Float, default=0.0, comment="文化交流度")

    # 关联信息
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    related_plots = Column(JSON, comment="相关剧情")
    related_events = Column(JSON, comment="相关事件")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.key_events:
            self.key_events = []
        if not self.related_plots:
            self.related_plots = []
        if not self.related_events:
            self.related_events = []

    def calculate_overall_cooperation(self) -> float:
        """计算总体合作度"""
        cooperation_factors = [
            self.military_cooperation,
            self.economic_cooperation,
            self.political_alignment,
            self.cultural_exchange
        ]
        return sum(cooperation_factors) / len(cooperation_factors)

    def update_cooperation(self, cooperation_type: str, change: float, reason: str = ""):
        """更新合作度"""
        old_value = getattr(self, cooperation_type, 0)
        new_value = max(0, min(1, old_value + change))
        setattr(self, cooperation_type, new_value)

        self.key_events.append({
            "type": f"{cooperation_type}_change",
            "old_value": old_value,
            "new_value": new_value,
            "change": change,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["overall_cooperation"] = self.calculate_overall_cooperation()
        return result


class EventAssociation(BaseModel):
    """事件关联模型"""

    __tablename__ = "event_associations"

    # 事件信息
    event_id = Column(Integer, comment="事件ID")
    event_type = Column(String(50), comment="事件类型")

    # 关联实体
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True, comment="关联角色ID")
    faction_id = Column(Integer, ForeignKey("factions.id"), nullable=True, comment="关联势力ID")
    plot_id = Column(Integer, ForeignKey("plots.id"), nullable=True, comment="关联剧情ID")
    location_name = Column(String(200), comment="关联地点")

    # 关联属性
    role = Column(String(100), comment="在事件中的角色")
    importance = Column(String(20), default="medium", comment="重要性")
    impact_level = Column(Float, default=0.5, comment="影响程度")

    # 详细信息
    description = Column(Text, comment="关联描述")
    consequences = Column(JSON, comment="后果影响")

    # 关联信息
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.consequences:
            self.consequences = []

    def add_consequence(self, consequence_data: Dict[str, Any]):
        """添加后果"""
        self.consequences.append(consequence_data)

    def get_association_summary(self) -> str:
        """获取关联摘要"""
        summary_parts = []

        if self.character_id:
            summary_parts.append(f"角色{self.character_id}")
        if self.faction_id:
            summary_parts.append(f"势力{self.faction_id}")
        if self.plot_id:
            summary_parts.append(f"剧情{self.plot_id}")
        if self.location_name:
            summary_parts.append(f"地点{self.location_name}")

        summary_parts.append(f"角色:{self.role}")
        summary_parts.append(f"重要性:{self.importance}")

        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["association_summary"] = self.get_association_summary()
        return result
