"""
人物数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum
from datetime import datetime

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class CharacterType(str, Enum):
    """人物类型枚举"""
    PROTAGONIST = "protagonist"      # 主角
    DEUTERAGONIST = "deuteragonist" # 重要配角
    SUPPORTING = "supporting"        # 配角
    ANTAGONIST = "antagonist"        # 反派
    VILLAIN = "villain"             # 大反派
    NPC = "npc"                     # NPC
    BACKGROUND = "background"        # 背景人物


class Gender(str, Enum):
    """性别枚举"""
    MALE = "male"           # 男性
    FEMALE = "female"       # 女性
    OTHER = "other"         # 其他
    UNKNOWN = "unknown"     # 未知


class CharacterStatus(str, Enum):
    """人物状态枚举"""
    ALIVE = "alive"         # 存活
    DEAD = "dead"           # 死亡
    MISSING = "missing"     # 失踪
    UNKNOWN = "unknown"     # 未知


class Character(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """人物模型"""

    __tablename__ = "characters"

    # 基本信息
    full_name = Column(String(200), comment="全名")
    nickname = Column(String(100), comment="昵称")
    title = Column(String(200), comment="称号")
    character_type = Column(SQLEnum(CharacterType), default=CharacterType.SUPPORTING, comment="人物类型")

    # 个人属性
    gender = Column(SQLEnum(Gender), default=Gender.UNKNOWN, comment="性别")
    age = Column(Integer, comment="年龄")
    birth_date = Column(String(100), comment="出生日期")
    birth_place = Column(String(200), comment="出生地")
    race = Column(String(100), comment="种族")
    bloodline = Column(String(200), comment="血脉")

    # 外貌描述
    appearance = Column(JSON, comment="外貌描述")
    height = Column(Float, comment="身高(cm)")
    weight = Column(Float, comment="体重(kg)")
    distinctive_features = Column(Text, comment="特征描述")

    # 性格特点
    personality = Column(JSON, comment="性格特点")
    values = Column(JSON, comment="价值观")
    beliefs = Column(JSON, comment="信仰")
    fears = Column(JSON, comment="恐惧")
    desires = Column(JSON, comment="欲望")

    # 能力属性
    abilities = Column(JSON, comment="能力属性")
    skills = Column(JSON, comment="技能")
    talents = Column(JSON, comment="天赋")
    cultivation_level = Column(String(100), comment="修炼等级")
    power_level = Column(Float, default=0, comment="实力等级")

    # 背景故事
    background = Column(Text, comment="背景故事")
    family = Column(JSON, comment="家庭关系")
    education = Column(JSON, comment="教育经历")
    experiences = Column(JSON, comment="重要经历")

    # 社会关系
    affiliations = Column(JSON, comment="所属组织")
    positions = Column(JSON, comment="职位")
    reputation = Column(JSON, comment="声望")

    # 状态信息
    status = Column(SQLEnum(CharacterStatus), default=CharacterStatus.ALIVE, comment="生存状态")
    current_location = Column(String(200), comment="当前位置")
    goals = Column(JSON, comment="目标")
    motivations = Column(JSON, comment="动机")

    # 成长轨迹
    growth_events = Column(JSON, comment="成长事件")
    character_arc = Column(JSON, comment="人物弧线")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.appearance:
            self.appearance = {}
        if not self.personality:
            self.personality = {}
        if not self.values:
            self.values = []
        if not self.beliefs:
            self.beliefs = []
        if not self.fears:
            self.fears = []
        if not self.desires:
            self.desires = []
        if not self.abilities:
            self.abilities = {}
        if not self.skills:
            self.skills = {}
        if not self.talents:
            self.talents = []
        if not self.family:
            self.family = {}
        if not self.education:
            self.education = []
        if not self.experiences:
            self.experiences = []
        if not self.affiliations:
            self.affiliations = []
        if not self.positions:
            self.positions = []
        if not self.reputation:
            self.reputation = {}
        if not self.goals:
            self.goals = []
        if not self.motivations:
            self.motivations = []
        if not self.growth_events:
            self.growth_events = []
        if not self.character_arc:
            self.character_arc = {}

    def get_display_name(self) -> str:
        """获取显示名称"""
        if self.nickname:
            return self.nickname
        elif self.full_name:
            return self.full_name
        else:
            return self.name

    def add_growth_event(self, event_data: Dict[str, Any]):
        """添加成长事件"""
        event_data["timestamp"] = datetime.now().isoformat()
        self.growth_events.append(event_data)
        # 按时间排序
        self.growth_events.sort(key=lambda x: x.get("timestamp", ""))

    def update_power_level(self, cultivation_system_data: Dict[str, Any] = None):
        """更新实力等级"""
        if cultivation_system_data:
            # 根据修炼体系计算实力
            character_data = {
                "cultivation_level": self.cultivation_level,
                "talents": self.talents,
                "techniques": self.skills.get("techniques", []),
                "bloodline": self.bloodline
            }
            # 这里需要调用修炼体系的计算方法
            # self.power_level = cultivation_system.calculate_power_level(character_data)
        else:
            # 简单计算
            base_power = self._calculate_base_power()
            talent_bonus = len(self.talents) * 10
            skill_bonus = len(self.skills) * 5
            self.power_level = base_power + talent_bonus + skill_bonus

    def _calculate_base_power(self) -> float:
        """计算基础实力"""
        # 根据年龄、修炼等级等计算基础实力
        age_factor = min(self.age or 20, 100) / 100 * 50
        level_factor = self._get_cultivation_level_power()
        return age_factor + level_factor

    def _get_cultivation_level_power(self) -> float:
        """根据修炼等级获取实力"""
        # 这里可以根据具体的修炼体系来计算
        # 暂时使用简单的映射
        level_map = {
            "凡人": 0,
            "练气": 10,
            "筑基": 30,
            "金丹": 60,
            "元婴": 100,
            "化神": 150,
            "炼虚": 200,
            "合体": 300,
            "大乘": 500,
            "渡劫": 800,
            "仙人": 1000
        }
        return level_map.get(self.cultivation_level, 0)

    def add_relationship(self, target_character_id: int, relationship_type: str, description: str = ""):
        """添加人物关系（需要在关系表中创建记录）"""
        # 这个方法需要在服务层实现
        pass

    def get_personality_summary(self) -> str:
        """获取性格摘要"""
        traits = []
        if self.personality:
            for category, values in self.personality.items():
                if isinstance(values, list):
                    traits.extend(values[:2])  # 取前两个特征
                elif isinstance(values, str):
                    traits.append(values)
        return ", ".join(traits[:5])  # 最多显示5个特征

    def get_ability_summary(self) -> str:
        """获取能力摘要"""
        abilities = []
        if self.cultivation_level:
            abilities.append(f"修为: {self.cultivation_level}")
        if self.talents:
            abilities.append(f"天赋: {len(self.talents)}项")
        if self.skills:
            skill_count = sum(len(v) if isinstance(v, list) else 1 for v in self.skills.values())
            abilities.append(f"技能: {skill_count}项")
        return " | ".join(abilities)

    def calculate_importance_score(self) -> float:
        """计算人物重要性评分"""
        score = 0

        # 基于人物类型
        type_scores = {
            CharacterType.PROTAGONIST: 100,
            CharacterType.DEUTERAGONIST: 80,
            CharacterType.ANTAGONIST: 70,
            CharacterType.VILLAIN: 90,
            CharacterType.SUPPORTING: 40,
            CharacterType.NPC: 20,
            CharacterType.BACKGROUND: 10
        }
        score += type_scores.get(self.character_type, 20)

        # 基于关系数量（需要从关系表查询）
        # score += relationship_count * 5

        # 基于成长事件数量
        score += len(self.growth_events) * 2

        # 基于实力等级
        score += self.power_level * 0.1

        return score

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["display_name"] = self.get_display_name()
        result["personality_summary"] = self.get_personality_summary()
        result["ability_summary"] = self.get_ability_summary()
        result["importance_score"] = self.calculate_importance_score()
        result["tags"] = self.get_tags()
        return result
