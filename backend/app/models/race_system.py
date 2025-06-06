"""
种族类别数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class RaceType(str, Enum):
    """种族类型枚举"""
    HUMANOID = "humanoid"           # 类人种族
    BEAST = "beast"                 # 兽族
    ELEMENTAL = "elemental"         # 元素族
    UNDEAD = "undead"               # 不死族
    DEMON = "demon"                 # 魔族
    ANGEL = "angel"                 # 天使族
    DRAGON = "dragon"               # 龙族
    SPIRIT = "spirit"               # 精灵族
    CONSTRUCT = "construct"         # 构造体
    PLANT = "plant"                 # 植物族
    AQUATIC = "aquatic"             # 水族
    AERIAL = "aerial"               # 飞行族
    OTHER = "other"                 # 其他


class LifespanCategory(str, Enum):
    """寿命类别枚举"""
    SHORT = "short"                 # 短寿 (0-100年)
    MEDIUM = "medium"               # 中等 (100-500年)
    LONG = "long"                   # 长寿 (500-2000年)
    VERY_LONG = "very_long"         # 极长寿 (2000年以上)
    IMMORTAL = "immortal"           # 不朽
    UNKNOWN = "unknown"             # 未知


class RaceSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """种族类别模型"""

    __tablename__ = "race_systems"

    # 基本信息
    race_type = Column(SQLEnum(RaceType), default=RaceType.HUMANOID, comment="种族类型")
    lifespan_category = Column(SQLEnum(LifespanCategory), default=LifespanCategory.MEDIUM, comment="寿命类别")
    
    # 生理特征
    physical_traits = Column(JSON, comment="生理特征")
    appearance = Column(JSON, comment="外貌特征")
    size_category = Column(String(50), comment="体型分类")
    
    # 能力属性
    racial_abilities = Column(JSON, comment="种族能力")
    attribute_modifiers = Column(JSON, comment="属性修正")
    special_talents = Column(JSON, comment="特殊天赋")
    
    # 文化特征
    culture = Column(JSON, comment="文化特征")
    language = Column(JSON, comment="语言体系")
    traditions = Column(JSON, comment="传统习俗")
    religion = Column(JSON, comment="宗教信仰")
    
    # 社会结构
    social_structure = Column(JSON, comment="社会结构")
    government = Column(JSON, comment="政治体制")
    hierarchy = Column(JSON, comment="等级制度")
    
    # 生存环境
    habitat = Column(JSON, comment="栖息地")
    climate_preference = Column(JSON, comment="气候偏好")
    territorial_behavior = Column(JSON, comment="领域行为")
    
    # 种族关系
    allied_races = Column(JSON, comment="友好种族")
    hostile_races = Column(JSON, comment="敌对种族")
    neutral_races = Column(JSON, comment="中立种族")
    
    # 历史发展
    origin_story = Column(Text, comment="起源故事")
    historical_events = Column(JSON, comment="历史事件")
    migration_patterns = Column(JSON, comment="迁徙模式")
    
    # 繁衍特征
    reproduction = Column(JSON, comment="繁衍方式")
    growth_stages = Column(JSON, comment="成长阶段")
    population_data = Column(JSON, comment="人口数据")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.physical_traits:
            self.physical_traits = {}
        if not self.appearance:
            self.appearance = {}
        if not self.racial_abilities:
            self.racial_abilities = []
        if not self.attribute_modifiers:
            self.attribute_modifiers = {}
        if not self.special_talents:
            self.special_talents = []
        if not self.culture:
            self.culture = {}
        if not self.language:
            self.language = {}
        if not self.traditions:
            self.traditions = []
        if not self.religion:
            self.religion = {}
        if not self.social_structure:
            self.social_structure = {}
        if not self.government:
            self.government = {}
        if not self.hierarchy:
            self.hierarchy = {}
        if not self.habitat:
            self.habitat = {}
        if not self.climate_preference:
            self.climate_preference = {}
        if not self.territorial_behavior:
            self.territorial_behavior = {}
        if not self.allied_races:
            self.allied_races = []
        if not self.hostile_races:
            self.hostile_races = []
        if not self.neutral_races:
            self.neutral_races = []
        if not self.historical_events:
            self.historical_events = []
        if not self.migration_patterns:
            self.migration_patterns = []
        if not self.reproduction:
            self.reproduction = {}
        if not self.growth_stages:
            self.growth_stages = []
        if not self.population_data:
            self.population_data = {}

    def add_racial_ability(self, ability_data: Dict[str, Any]):
        """添加种族能力"""
        self.racial_abilities.append(ability_data)

    def add_special_talent(self, talent_data: Dict[str, Any]):
        """添加特殊天赋"""
        self.special_talents.append(talent_data)

    def add_tradition(self, tradition_data: Dict[str, Any]):
        """添加传统习俗"""
        self.traditions.append(tradition_data)

    def add_historical_event(self, event_data: Dict[str, Any]):
        """添加历史事件"""
        self.historical_events.append(event_data)
        # 按时间排序
        self.historical_events.sort(key=lambda x: x.get("time", 0))

    def set_relationship(self, race_name: str, relationship_type: str):
        """设置种族关系"""
        # 先从其他关系列表中移除
        self.allied_races = [r for r in self.allied_races if r != race_name]
        self.hostile_races = [r for r in self.hostile_races if r != race_name]
        self.neutral_races = [r for r in self.neutral_races if r != race_name]
        
        # 添加到对应关系列表
        if relationship_type == "allied":
            self.allied_races.append(race_name)
        elif relationship_type == "hostile":
            self.hostile_races.append(race_name)
        elif relationship_type == "neutral":
            self.neutral_races.append(race_name)

    def get_ability_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取种族能力"""
        for ability in self.racial_abilities:
            if ability.get("name") == name:
                return ability
        return None

    def get_talent_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取特殊天赋"""
        for talent in self.special_talents:
            if talent.get("name") == name:
                return talent
        return None

    def calculate_power_level(self) -> float:
        """计算种族实力等级"""
        score = 50.0  # 基础分数
        
        # 种族能力加成
        score += len(self.racial_abilities) * 5
        
        # 特殊天赋加成
        score += len(self.special_talents) * 3
        
        # 寿命加成
        lifespan_bonus = {
            LifespanCategory.SHORT: 0,
            LifespanCategory.MEDIUM: 5,
            LifespanCategory.LONG: 10,
            LifespanCategory.VERY_LONG: 15,
            LifespanCategory.IMMORTAL: 20,
            LifespanCategory.UNKNOWN: 0
        }
        score += lifespan_bonus.get(self.lifespan_category, 0)
        
        # 属性修正加成
        if self.attribute_modifiers:
            total_modifiers = sum(abs(v) for v in self.attribute_modifiers.values() if isinstance(v, (int, float)))
            score += total_modifiers * 2
        
        return min(100.0, max(0.0, score))

    def calculate_civilization_level(self) -> float:
        """计算文明等级"""
        score = 30.0  # 基础分数
        
        # 社会结构复杂度
        if self.social_structure:
            score += len(self.social_structure) * 5
        
        # 政治体制
        if self.government:
            score += len(self.government) * 4
        
        # 文化发展
        if self.culture:
            score += len(self.culture) * 3
        
        # 语言体系
        if self.language:
            score += len(self.language) * 3
        
        # 传统习俗
        score += len(self.traditions) * 2
        
        # 历史深度
        score += len(self.historical_events) * 2
        
        return min(100.0, max(0.0, score))

    def validate_consistency(self) -> List[str]:
        """验证种族设定一致性"""
        issues = []
        
        # 检查寿命与种族类型的一致性
        if self.race_type == RaceType.UNDEAD and self.lifespan_category != LifespanCategory.IMMORTAL:
            issues.append("不死族应该是不朽的")
        
        # 检查栖息地与气候偏好的一致性
        if self.habitat and self.climate_preference:
            habitat_climate = self.habitat.get("climate")
            preferred_climate = self.climate_preference.get("preferred")
            if habitat_climate and preferred_climate and habitat_climate != preferred_climate:
                issues.append("栖息地气候与气候偏好不一致")
        
        # 检查种族关系的对称性
        all_relations = self.allied_races + self.hostile_races + self.neutral_races
        if len(all_relations) != len(set(all_relations)):
            issues.append("种族关系列表中存在重复")
        
        return issues

    def generate_summary(self) -> str:
        """生成种族摘要"""
        summary_parts = []
        
        if self.description:
            summary_parts.append(self.description)
        
        # 种族类型
        type_map = {
            RaceType.HUMANOID: "类人种族",
            RaceType.BEAST: "兽族",
            RaceType.ELEMENTAL: "元素族",
            RaceType.UNDEAD: "不死族",
            RaceType.DEMON: "魔族",
            RaceType.ANGEL: "天使族",
            RaceType.DRAGON: "龙族",
            RaceType.SPIRIT: "精灵族",
            RaceType.CONSTRUCT: "构造体",
            RaceType.PLANT: "植物族",
            RaceType.AQUATIC: "水族",
            RaceType.AERIAL: "飞行族",
            RaceType.OTHER: "其他"
        }
        summary_parts.append(f"种族类型: {type_map.get(self.race_type, '未知')}")
        
        # 寿命类别
        lifespan_map = {
            LifespanCategory.SHORT: "短寿",
            LifespanCategory.MEDIUM: "中等寿命",
            LifespanCategory.LONG: "长寿",
            LifespanCategory.VERY_LONG: "极长寿",
            LifespanCategory.IMMORTAL: "不朽",
            LifespanCategory.UNKNOWN: "未知"
        }
        summary_parts.append(f"寿命: {lifespan_map.get(self.lifespan_category, '未知')}")
        
        # 能力数量
        summary_parts.append(f"种族能力: {len(self.racial_abilities)}个")
        
        # 实力等级
        power = self.calculate_power_level()
        summary_parts.append(f"实力等级: {power:.1f}/100")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["power_level"] = self.calculate_power_level()
        result["civilization_level"] = self.calculate_civilization_level()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
