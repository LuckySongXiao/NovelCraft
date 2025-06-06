"""
秘境分布数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class RealmType(str, Enum):
    """秘境类型枚举"""
    DUNGEON = "dungeon"             # 地下城
    RUINS = "ruins"                 # 遗迹
    TEMPLE = "temple"               # 神殿
    TOMB = "tomb"                   # 陵墓
    CAVE = "cave"                   # 洞穴
    FOREST = "forest"               # 秘境森林
    ISLAND = "island"               # 神秘岛屿
    DIMENSION = "dimension"         # 异次元
    TOWER = "tower"                 # 高塔
    LABYRINTH = "labyrinth"         # 迷宫
    SANCTUARY = "sanctuary"         # 圣域
    TRIAL = "trial"                 # 试炼场
    OTHER = "other"                 # 其他


class DangerLevel(str, Enum):
    """危险等级枚举"""
    SAFE = "safe"                   # 安全
    LOW = "low"                     # 低危
    MODERATE = "moderate"           # 中危
    HIGH = "high"                   # 高危
    EXTREME = "extreme"             # 极危
    LETHAL = "lethal"               # 致命
    UNKNOWN = "unknown"             # 未知


class AccessType(str, Enum):
    """进入方式枚举"""
    OPEN = "open"                   # 开放
    CONDITIONAL = "conditional"     # 条件
    TIMED = "timed"                 # 定时
    TRIGGERED = "triggered"         # 触发
    HIDDEN = "hidden"               # 隐藏
    SEALED = "sealed"               # 封印
    DESTROYED = "destroyed"         # 已毁
    UNKNOWN = "unknown"             # 未知


class SecretRealmDistribution(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """秘境分布模型"""

    __tablename__ = "secret_realm_distributions"

    # 基本信息
    realm_type = Column(SQLEnum(RealmType), default=RealmType.DUNGEON, comment="秘境类型")
    danger_level = Column(SQLEnum(DangerLevel), default=DangerLevel.MODERATE, comment="危险等级")
    access_type = Column(SQLEnum(AccessType), default=AccessType.OPEN, comment="进入方式")
    
    # 位置信息
    location_coordinates = Column(JSON, comment="位置坐标")
    geographic_region = Column(String(200), comment="地理区域")
    terrain_type = Column(String(100), comment="地形类型")
    hidden_level = Column(Integer, default=1, comment="隐藏程度")
    
    # 结构信息
    size_scale = Column(String(50), comment="规模大小")
    internal_structure = Column(JSON, comment="内部结构")
    floor_levels = Column(Integer, default=1, comment="层数")
    room_count = Column(Integer, comment="房间数量")
    
    # 进入条件
    entry_requirements = Column(JSON, comment="进入条件")
    access_restrictions = Column(JSON, comment="访问限制")
    opening_schedule = Column(JSON, comment="开放时间")
    activation_methods = Column(JSON, comment="激活方法")
    
    # 环境特征
    environmental_conditions = Column(JSON, comment="环境条件")
    magical_properties = Column(JSON, comment="魔法属性")
    atmospheric_effects = Column(JSON, comment="大气效应")
    special_phenomena = Column(JSON, comment="特殊现象")
    
    # 居住生物
    guardian_creatures = Column(JSON, comment="守护生物")
    hostile_entities = Column(JSON, comment="敌对实体")
    neutral_inhabitants = Column(JSON, comment="中性居民")
    boss_encounters = Column(JSON, comment="首领遭遇")
    
    # 奖励资源
    treasure_types = Column(JSON, comment="宝藏类型")
    rare_materials = Column(JSON, comment="稀有材料")
    magical_artifacts = Column(JSON, comment="魔法文物")
    knowledge_rewards = Column(JSON, comment="知识奖励")
    
    # 陷阱机关
    trap_systems = Column(JSON, comment="陷阱系统")
    puzzle_mechanisms = Column(JSON, comment="谜题机关")
    security_measures = Column(JSON, comment="安全措施")
    defensive_systems = Column(JSON, comment="防御系统")
    
    # 历史背景
    creation_origin = Column(Text, comment="创建起源")
    historical_purpose = Column(Text, comment="历史用途")
    previous_explorers = Column(JSON, comment="先前探索者")
    significant_events = Column(JSON, comment="重要事件")
    
    # 探索信息
    exploration_status = Column(String(100), comment="探索状态")
    completion_rate = Column(Float, default=0.0, comment="完成度")
    discovery_rewards = Column(JSON, comment="发现奖励")
    exploration_records = Column(JSON, comment="探索记录")
    
    # 影响范围
    influence_radius = Column(Float, comment="影响半径")
    environmental_impact = Column(JSON, comment="环境影响")
    local_legends = Column(JSON, comment="当地传说")
    cultural_significance = Column(Text, comment="文化意义")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")
    map_structure_id = Column(Integer, ForeignKey("map_structures.id"), comment="地图结构ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.location_coordinates:
            self.location_coordinates = {}
        if not self.internal_structure:
            self.internal_structure = {}
        if not self.entry_requirements:
            self.entry_requirements = []
        if not self.access_restrictions:
            self.access_restrictions = []
        if not self.opening_schedule:
            self.opening_schedule = {}
        if not self.activation_methods:
            self.activation_methods = []
        if not self.environmental_conditions:
            self.environmental_conditions = {}
        if not self.magical_properties:
            self.magical_properties = []
        if not self.atmospheric_effects:
            self.atmospheric_effects = []
        if not self.special_phenomena:
            self.special_phenomena = []
        if not self.guardian_creatures:
            self.guardian_creatures = []
        if not self.hostile_entities:
            self.hostile_entities = []
        if not self.neutral_inhabitants:
            self.neutral_inhabitants = []
        if not self.boss_encounters:
            self.boss_encounters = []
        if not self.treasure_types:
            self.treasure_types = []
        if not self.rare_materials:
            self.rare_materials = []
        if not self.magical_artifacts:
            self.magical_artifacts = []
        if not self.knowledge_rewards:
            self.knowledge_rewards = []
        if not self.trap_systems:
            self.trap_systems = []
        if not self.puzzle_mechanisms:
            self.puzzle_mechanisms = []
        if not self.security_measures:
            self.security_measures = []
        if not self.defensive_systems:
            self.defensive_systems = []
        if not self.previous_explorers:
            self.previous_explorers = []
        if not self.significant_events:
            self.significant_events = []
        if not self.discovery_rewards:
            self.discovery_rewards = []
        if not self.exploration_records:
            self.exploration_records = []
        if not self.environmental_impact:
            self.environmental_impact = {}
        if not self.local_legends:
            self.local_legends = []

    def add_guardian_creature(self, creature_data: Dict[str, Any]):
        """添加守护生物"""
        self.guardian_creatures.append(creature_data)

    def add_treasure(self, treasure_data: Dict[str, Any]):
        """添加宝藏"""
        self.treasure_types.append(treasure_data)

    def add_trap_system(self, trap_data: Dict[str, Any]):
        """添加陷阱系统"""
        self.trap_systems.append(trap_data)

    def add_exploration_record(self, record_data: Dict[str, Any]):
        """添加探索记录"""
        self.exploration_records.append(record_data)

    def update_completion_rate(self, new_rate: float):
        """更新完成度"""
        self.completion_rate = max(0.0, min(100.0, new_rate))

    def calculate_difficulty_score(self) -> float:
        """计算难度评分"""
        difficulty = 0.0
        
        # 危险等级基础分数
        danger_scores = {
            DangerLevel.SAFE: 10,
            DangerLevel.LOW: 25,
            DangerLevel.MODERATE: 40,
            DangerLevel.HIGH: 60,
            DangerLevel.EXTREME: 80,
            DangerLevel.LETHAL: 95,
            DangerLevel.UNKNOWN: 50
        }
        difficulty += danger_scores.get(self.danger_level, 50)
        
        # 守护生物数量
        difficulty += len(self.guardian_creatures) * 3
        
        # 敌对实体数量
        difficulty += len(self.hostile_entities) * 2
        
        # 首领遭遇数量
        difficulty += len(self.boss_encounters) * 5
        
        # 陷阱系统复杂度
        difficulty += len(self.trap_systems) * 2
        
        # 谜题机关复杂度
        difficulty += len(self.puzzle_mechanisms) * 1.5
        
        # 进入条件限制
        difficulty += len(self.entry_requirements) * 1
        
        return min(100.0, max(0.0, difficulty))

    def calculate_reward_value(self) -> float:
        """计算奖励价值"""
        value = 0.0
        
        # 宝藏类型价值
        value += len(self.treasure_types) * 5
        
        # 稀有材料价值
        value += len(self.rare_materials) * 4
        
        # 魔法文物价值
        value += len(self.magical_artifacts) * 8
        
        # 知识奖励价值
        value += len(self.knowledge_rewards) * 6
        
        # 发现奖励价值
        value += len(self.discovery_rewards) * 3
        
        # 规模加成
        if self.floor_levels:
            value += self.floor_levels * 2
        
        if self.room_count:
            value += self.room_count * 0.5
        
        return min(100.0, max(0.0, value))

    def calculate_accessibility(self) -> float:
        """计算可达性"""
        accessibility = 50.0  # 基础分数
        
        # 进入方式影响
        access_modifiers = {
            AccessType.OPEN: 20,
            AccessType.CONDITIONAL: 0,
            AccessType.TIMED: -5,
            AccessType.TRIGGERED: -10,
            AccessType.HIDDEN: -15,
            AccessType.SEALED: -30,
            AccessType.DESTROYED: -50,
            AccessType.UNKNOWN: -5
        }
        accessibility += access_modifiers.get(self.access_type, 0)
        
        # 隐藏程度影响
        accessibility -= self.hidden_level * 3
        
        # 进入条件限制
        accessibility -= len(self.entry_requirements) * 2
        
        # 访问限制
        accessibility -= len(self.access_restrictions) * 3
        
        return min(100.0, max(0.0, accessibility))

    def validate_consistency(self) -> List[str]:
        """验证秘境分布一致性"""
        issues = []
        
        # 检查完成度范围
        if self.completion_rate < 0 or self.completion_rate > 100:
            issues.append("完成度必须在0-100之间")
        
        # 检查层数与房间数的合理性
        if self.floor_levels and self.room_count:
            if self.room_count < self.floor_levels:
                issues.append("房间数量不应少于层数")
        
        # 检查进入方式与访问限制的一致性
        if self.access_type == AccessType.OPEN and len(self.access_restrictions) > 0:
            issues.append("开放式秘境不应有访问限制")
        
        # 检查危险等级与守护生物的一致性
        if self.danger_level == DangerLevel.SAFE and len(self.hostile_entities) > 0:
            issues.append("安全等级的秘境不应有敌对实体")
        
        return issues

    def generate_summary(self) -> str:
        """生成秘境分布摘要"""
        summary_parts = []
        
        if self.description:
            summary_parts.append(self.description)
        
        # 秘境类型
        type_map = {
            RealmType.DUNGEON: "地下城",
            RealmType.RUINS: "遗迹",
            RealmType.TEMPLE: "神殿",
            RealmType.TOMB: "陵墓",
            RealmType.CAVE: "洞穴",
            RealmType.FOREST: "秘境森林",
            RealmType.ISLAND: "神秘岛屿",
            RealmType.DIMENSION: "异次元",
            RealmType.TOWER: "高塔",
            RealmType.LABYRINTH: "迷宫",
            RealmType.SANCTUARY: "圣域",
            RealmType.TRIAL: "试炼场",
            RealmType.OTHER: "其他"
        }
        summary_parts.append(f"类型: {type_map.get(self.realm_type, '未知')}")
        
        # 危险等级
        danger_map = {
            DangerLevel.SAFE: "安全",
            DangerLevel.LOW: "低危",
            DangerLevel.MODERATE: "中危",
            DangerLevel.HIGH: "高危",
            DangerLevel.EXTREME: "极危",
            DangerLevel.LETHAL: "致命",
            DangerLevel.UNKNOWN: "未知"
        }
        summary_parts.append(f"危险: {danger_map.get(self.danger_level, '未知')}")
        
        # 层数
        if self.floor_levels:
            summary_parts.append(f"层数: {self.floor_levels}")
        
        # 完成度
        summary_parts.append(f"完成度: {self.completion_rate:.1f}%")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["difficulty_score"] = self.calculate_difficulty_score()
        result["reward_value"] = self.calculate_reward_value()
        result["accessibility"] = self.calculate_accessibility()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
