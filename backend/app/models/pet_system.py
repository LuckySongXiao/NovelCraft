"""
宠物体系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class PetType(str, Enum):
    """宠物类型枚举"""
    BEAST = "beast"                 # 野兽
    SPIRIT = "spirit"               # 精灵
    DRAGON = "dragon"               # 龙族
    ELEMENTAL = "elemental"         # 元素
    UNDEAD = "undead"               # 不死
    CONSTRUCT = "construct"         # 构造体
    PLANT = "plant"                 # 植物
    AQUATIC = "aquatic"             # 水生
    AERIAL = "aerial"               # 飞行
    MYTHICAL = "mythical"           # 神话
    DEMON = "demon"                 # 魔族
    CELESTIAL = "celestial"         # 天界
    OTHER = "other"                 # 其他


class PetRarity(str, Enum):
    """宠物稀有度枚举"""
    COMMON = "common"               # 普通
    UNCOMMON = "uncommon"           # 优秀
    RARE = "rare"                   # 稀有
    EPIC = "epic"                   # 史诗
    LEGENDARY = "legendary"         # 传说
    MYTHICAL = "mythical"           # 神话
    DIVINE = "divine"               # 神级
    UNIQUE = "unique"               # 唯一
    UNKNOWN = "unknown"             # 未知


class PetRole(str, Enum):
    """宠物角色枚举"""
    COMBAT = "combat"               # 战斗
    MOUNT = "mount"                 # 坐骑
    COMPANION = "companion"         # 伙伴
    WORKER = "worker"               # 工作
    GUARDIAN = "guardian"           # 守护
    SCOUT = "scout"                 # 侦察
    HEALER = "healer"               # 治疗
    SUPPORT = "support"             # 辅助
    TRANSPORT = "transport"         # 运输
    DECORATION = "decoration"       # 装饰
    OTHER = "other"                 # 其他


class PetSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """宠物体系模型"""

    __tablename__ = "pet_systems"

    # 基本信息
    pet_type = Column(SQLEnum(PetType), default=PetType.BEAST, comment="宠物类型")
    pet_rarity = Column(SQLEnum(PetRarity), default=PetRarity.COMMON, comment="宠物稀有度")
    pet_role = Column(SQLEnum(PetRole), default=PetRole.COMPANION, comment="宠物角色")
    
    # 生物特征
    species = Column(String(100), comment="物种")
    size_category = Column(String(50), comment="体型分类")
    lifespan = Column(Integer, comment="寿命")
    habitat = Column(JSON, comment="栖息地")
    
    # 基础属性
    base_attributes = Column(JSON, comment="基础属性")
    growth_rates = Column(JSON, comment="成长率")
    max_level = Column(Integer, default=100, comment="最大等级")
    current_level = Column(Integer, default=1, comment="当前等级")
    
    # 技能系统
    innate_skills = Column(JSON, comment="天赋技能")
    learnable_skills = Column(JSON, comment="可学技能")
    skill_slots = Column(Integer, default=4, comment="技能槽位")
    
    # 进化系统
    evolution_chain = Column(JSON, comment="进化链")
    evolution_requirements = Column(JSON, comment="进化条件")
    evolution_materials = Column(JSON, comment="进化材料")
    
    # 培养系统
    feeding_preferences = Column(JSON, comment="喂食偏好")
    training_methods = Column(JSON, comment="训练方法")
    bonding_activities = Column(JSON, comment="亲密度活动")
    
    # 繁殖系统
    breeding_compatibility = Column(JSON, comment="繁殖兼容性")
    breeding_requirements = Column(JSON, comment="繁殖条件")
    offspring_traits = Column(JSON, comment="后代特征")
    
    # 战斗能力
    combat_abilities = Column(JSON, comment="战斗能力")
    special_attacks = Column(JSON, comment="特殊攻击")
    defensive_skills = Column(JSON, comment="防御技能")
    
    # 实用功能
    utility_functions = Column(JSON, comment="实用功能")
    mount_capabilities = Column(JSON, comment="坐骑能力")
    work_skills = Column(JSON, comment="工作技能")
    
    # 获取方式
    capture_methods = Column(JSON, comment="捕获方法")
    spawn_locations = Column(JSON, comment="出现地点")
    quest_rewards = Column(JSON, comment="任务奖励")
    
    # 宠物历史
    origin_story = Column(Text, comment="起源故事")
    famous_specimens = Column(JSON, comment="著名个体")
    cultural_significance = Column(Text, comment="文化意义")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.habitat:
            self.habitat = {}
        if not self.base_attributes:
            self.base_attributes = {}
        if not self.growth_rates:
            self.growth_rates = {}
        if not self.innate_skills:
            self.innate_skills = []
        if not self.learnable_skills:
            self.learnable_skills = []
        if not self.evolution_chain:
            self.evolution_chain = []
        if not self.evolution_requirements:
            self.evolution_requirements = {}
        if not self.evolution_materials:
            self.evolution_materials = []
        if not self.feeding_preferences:
            self.feeding_preferences = []
        if not self.training_methods:
            self.training_methods = []
        if not self.bonding_activities:
            self.bonding_activities = []
        if not self.breeding_compatibility:
            self.breeding_compatibility = []
        if not self.breeding_requirements:
            self.breeding_requirements = {}
        if not self.offspring_traits:
            self.offspring_traits = []
        if not self.combat_abilities:
            self.combat_abilities = []
        if not self.special_attacks:
            self.special_attacks = []
        if not self.defensive_skills:
            self.defensive_skills = []
        if not self.utility_functions:
            self.utility_functions = []
        if not self.mount_capabilities:
            self.mount_capabilities = {}
        if not self.work_skills:
            self.work_skills = []
        if not self.capture_methods:
            self.capture_methods = []
        if not self.spawn_locations:
            self.spawn_locations = []
        if not self.quest_rewards:
            self.quest_rewards = []
        if not self.famous_specimens:
            self.famous_specimens = []

    def add_innate_skill(self, skill_data: Dict[str, Any]):
        """添加天赋技能"""
        self.innate_skills.append(skill_data)

    def add_learnable_skill(self, skill_data: Dict[str, Any]):
        """添加可学技能"""
        self.learnable_skills.append(skill_data)

    def add_evolution_stage(self, stage_data: Dict[str, Any]):
        """添加进化阶段"""
        self.evolution_chain.append(stage_data)

    def add_combat_ability(self, ability_data: Dict[str, Any]):
        """添加战斗能力"""
        self.combat_abilities.append(ability_data)

    def add_spawn_location(self, location_data: Dict[str, Any]):
        """添加出现地点"""
        self.spawn_locations.append(location_data)

    def level_up(self, target_level: int = None):
        """升级宠物"""
        if target_level is None:
            target_level = self.current_level + 1
        
        if target_level <= self.max_level:
            self.current_level = target_level
            return True
        return False

    def calculate_current_attributes(self) -> Dict[str, Any]:
        """计算当前属性"""
        current_attrs = {}
        
        for attr, base_value in self.base_attributes.items():
            growth_rate = self.growth_rates.get(attr, 1.0)
            current_value = base_value + (self.current_level - 1) * growth_rate
            current_attrs[attr] = int(current_value)
        
        return current_attrs

    def calculate_combat_power(self) -> float:
        """计算战斗力"""
        power = 0.0
        
        # 基础属性贡献
        current_attrs = self.calculate_current_attributes()
        for attr, value in current_attrs.items():
            if attr in ["attack", "defense", "speed", "hp"]:
                power += value * 0.1
        
        # 等级贡献
        power += self.current_level * 2
        
        # 技能贡献
        power += len(self.innate_skills) * 5
        power += len(self.combat_abilities) * 3
        
        # 稀有度加成
        rarity_bonus = {
            PetRarity.COMMON: 1.0,
            PetRarity.UNCOMMON: 1.2,
            PetRarity.RARE: 1.5,
            PetRarity.EPIC: 2.0,
            PetRarity.LEGENDARY: 2.5,
            PetRarity.MYTHICAL: 3.0,
            PetRarity.DIVINE: 4.0,
            PetRarity.UNIQUE: 5.0,
            PetRarity.UNKNOWN: 1.0
        }
        
        power *= rarity_bonus.get(self.pet_rarity, 1.0)
        
        return power

    def calculate_utility_value(self) -> float:
        """计算实用价值"""
        value = 50.0  # 基础分数
        
        # 实用功能加成
        value += len(self.utility_functions) * 5
        
        # 工作技能加成
        value += len(self.work_skills) * 3
        
        # 坐骑能力加成
        if self.mount_capabilities:
            value += len(self.mount_capabilities) * 4
        
        # 角色类型加成
        role_bonus = {
            PetRole.COMBAT: 0,
            PetRole.MOUNT: 15,
            PetRole.COMPANION: 10,
            PetRole.WORKER: 20,
            PetRole.GUARDIAN: 10,
            PetRole.SCOUT: 12,
            PetRole.HEALER: 18,
            PetRole.SUPPORT: 15,
            PetRole.TRANSPORT: 15,
            PetRole.DECORATION: 5,
            PetRole.OTHER: 0
        }
        value += role_bonus.get(self.pet_role, 0)
        
        return min(100.0, max(0.0, value))

    def validate_consistency(self) -> List[str]:
        """验证宠物设定一致性"""
        issues = []
        
        # 检查等级范围
        if self.current_level > self.max_level:
            issues.append("当前等级超过最大等级")
        
        # 检查技能槽位
        active_skills = len(self.innate_skills)
        if active_skills > self.skill_slots:
            issues.append(f"技能数量({active_skills})超过技能槽位({self.skill_slots})")
        
        # 检查宠物类型与角色的一致性
        if self.pet_type == PetType.UNDEAD and self.pet_role == PetRole.HEALER:
            issues.append("不死类型宠物不适合担任治疗角色")
        
        return issues

    def generate_summary(self) -> str:
        """生成宠物摘要"""
        summary_parts = []
        
        if self.description:
            summary_parts.append(self.description)
        
        # 宠物类型
        type_map = {
            PetType.BEAST: "野兽",
            PetType.SPIRIT: "精灵",
            PetType.DRAGON: "龙族",
            PetType.ELEMENTAL: "元素",
            PetType.UNDEAD: "不死",
            PetType.CONSTRUCT: "构造体",
            PetType.PLANT: "植物",
            PetType.AQUATIC: "水生",
            PetType.AERIAL: "飞行",
            PetType.MYTHICAL: "神话",
            PetType.DEMON: "魔族",
            PetType.CELESTIAL: "天界",
            PetType.OTHER: "其他"
        }
        summary_parts.append(f"类型: {type_map.get(self.pet_type, '未知')}")
        
        # 稀有度
        rarity_map = {
            PetRarity.COMMON: "普通",
            PetRarity.UNCOMMON: "优秀",
            PetRarity.RARE: "稀有",
            PetRarity.EPIC: "史诗",
            PetRarity.LEGENDARY: "传说",
            PetRarity.MYTHICAL: "神话",
            PetRarity.DIVINE: "神级",
            PetRarity.UNIQUE: "唯一",
            PetRarity.UNKNOWN: "未知"
        }
        summary_parts.append(f"稀有度: {rarity_map.get(self.pet_rarity, '未知')}")
        
        # 等级
        summary_parts.append(f"等级: {self.current_level}/{self.max_level}")
        
        # 战斗力
        combat_power = self.calculate_combat_power()
        summary_parts.append(f"战斗力: {combat_power:.1f}")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["current_attributes"] = self.calculate_current_attributes()
        result["combat_power"] = self.calculate_combat_power()
        result["utility_value"] = self.calculate_utility_value()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
