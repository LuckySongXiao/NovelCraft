"""
灵宝体系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class TreasureType(str, Enum):
    """灵宝类型枚举"""
    WEAPON = "weapon"               # 法器武器
    ARMOR = "armor"                 # 护身法宝
    ACCESSORY = "accessory"         # 饰品法宝
    PILL = "pill"                   # 丹药
    FORMATION = "formation"         # 阵法
    TALISMAN = "talisman"           # 符箓
    CAULDRON = "cauldron"           # 鼎炉
    SCROLL = "scroll"               # 功法秘籍
    SPIRIT_STONE = "spirit_stone"   # 灵石
    HERB = "herb"                   # 灵草
    BEAST_CORE = "beast_core"       # 妖兽内丹
    ARTIFACT = "artifact"           # 上古神器
    OTHER = "other"                 # 其他


class TreasureGrade(str, Enum):
    """灵宝品级枚举"""
    MORTAL = "mortal"               # 凡品
    SPIRITUAL = "spiritual"         # 灵品
    TREASURE = "treasure"           # 宝品
    KING = "king"                   # 王品
    EMPEROR = "emperor"             # 皇品
    SAINT = "saint"                 # 圣品
    DIVINE = "divine"               # 神品
    IMMORTAL = "immortal"           # 仙品
    CHAOS = "chaos"                 # 混沌
    UNKNOWN = "unknown"             # 未知


class SpiritualLevel(str, Enum):
    """灵性等级枚举"""
    NONE = "none"                   # 无灵性
    WEAK = "weak"                   # 微弱
    LOW = "low"                     # 低等
    MEDIUM = "medium"               # 中等
    HIGH = "high"                   # 高等
    PEAK = "peak"                   # 巅峰
    TRANSCENDENT = "transcendent"   # 超凡
    UNKNOWN = "unknown"             # 未知


class SpiritualTreasureSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """灵宝体系模型"""

    __tablename__ = "spiritual_treasure_systems"

    # 基本信息
    treasure_type = Column(SQLEnum(TreasureType), default=TreasureType.WEAPON, comment="灵宝类型")
    treasure_grade = Column(SQLEnum(TreasureGrade), default=TreasureGrade.MORTAL, comment="灵宝品级")
    spiritual_level = Column(SQLEnum(SpiritualLevel), default=SpiritualLevel.NONE, comment="灵性等级")
    
    # 灵宝属性
    spiritual_power = Column(Float, default=0.0, comment="灵力值")
    elemental_affinity = Column(JSON, comment="元素亲和")
    special_abilities = Column(JSON, comment="特殊能力")
    restrictions = Column(JSON, comment="使用限制")
    
    # 炼制信息
    refining_materials = Column(JSON, comment="炼制材料")
    refining_method = Column(Text, comment="炼制方法")
    refining_difficulty = Column(Integer, default=1, comment="炼制难度")
    success_rate = Column(Float, default=100.0, comment="成功率")
    
    # 成长系统
    growth_potential = Column(Float, default=0.0, comment="成长潜力")
    evolution_paths = Column(JSON, comment="进化路径")
    upgrade_materials = Column(JSON, comment="升级材料")
    max_level = Column(Integer, default=1, comment="最大等级")
    
    # 器灵系统
    spirit_consciousness = Column(Boolean, default=False, comment="是否有器灵")
    spirit_personality = Column(JSON, comment="器灵性格")
    spirit_abilities = Column(JSON, comment="器灵能力")
    spirit_communication = Column(Text, comment="沟通方式")
    
    # 使用效果
    primary_effects = Column(JSON, comment="主要效果")
    secondary_effects = Column(JSON, comment="次要效果")
    side_effects = Column(JSON, comment="副作用")
    duration = Column(String(100), comment="持续时间")
    
    # 获取方式
    acquisition_methods = Column(JSON, comment="获取方式")
    drop_locations = Column(JSON, comment="掉落地点")
    quest_rewards = Column(JSON, comment="任务奖励")
    crafting_recipes = Column(JSON, comment="制作配方")
    
    # 历史传承
    origin_story = Column(Text, comment="来历故事")
    previous_owners = Column(JSON, comment="历任主人")
    legendary_deeds = Column(JSON, comment="传奇事迹")
    cultural_significance = Column(Text, comment="文化意义")
    
    # 市场价值
    market_value = Column(Float, comment="市场价值")
    rarity_factor = Column(Float, default=1.0, comment="稀有度系数")
    trade_restrictions = Column(JSON, comment="交易限制")
    auction_records = Column(JSON, comment="拍卖记录")
    
    # 保存与维护
    storage_requirements = Column(JSON, comment="保存要求")
    maintenance_needs = Column(JSON, comment="维护需求")
    degradation_rate = Column(Float, default=0.0, comment="损耗率")
    repair_methods = Column(JSON, comment="修复方法")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")
    parent_treasure_id = Column(Integer, ForeignKey("spiritual_treasure_systems.id"), comment="父级灵宝ID")

    # 自引用关系
    children = relationship("SpiritualTreasureSystem", backref="parent", remote_side="SpiritualTreasureSystem.id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.elemental_affinity:
            self.elemental_affinity = []
        if not self.special_abilities:
            self.special_abilities = []
        if not self.restrictions:
            self.restrictions = []
        if not self.refining_materials:
            self.refining_materials = []
        if not self.evolution_paths:
            self.evolution_paths = []
        if not self.upgrade_materials:
            self.upgrade_materials = []
        if not self.spirit_personality:
            self.spirit_personality = {}
        if not self.spirit_abilities:
            self.spirit_abilities = []
        if not self.primary_effects:
            self.primary_effects = []
        if not self.secondary_effects:
            self.secondary_effects = []
        if not self.side_effects:
            self.side_effects = []
        if not self.acquisition_methods:
            self.acquisition_methods = []
        if not self.drop_locations:
            self.drop_locations = []
        if not self.quest_rewards:
            self.quest_rewards = []
        if not self.crafting_recipes:
            self.crafting_recipes = []
        if not self.previous_owners:
            self.previous_owners = []
        if not self.legendary_deeds:
            self.legendary_deeds = []
        if not self.trade_restrictions:
            self.trade_restrictions = []
        if not self.auction_records:
            self.auction_records = []
        if not self.storage_requirements:
            self.storage_requirements = []
        if not self.maintenance_needs:
            self.maintenance_needs = []
        if not self.repair_methods:
            self.repair_methods = []

    def add_special_ability(self, ability_data: Dict[str, Any]):
        """添加特殊能力"""
        self.special_abilities.append(ability_data)

    def add_refining_material(self, material_data: Dict[str, Any]):
        """添加炼制材料"""
        self.refining_materials.append(material_data)

    def add_evolution_path(self, path_data: Dict[str, Any]):
        """添加进化路径"""
        self.evolution_paths.append(path_data)

    def add_spirit_ability(self, ability_data: Dict[str, Any]):
        """添加器灵能力"""
        self.spirit_abilities.append(ability_data)

    def add_legendary_deed(self, deed_data: Dict[str, Any]):
        """添加传奇事迹"""
        self.legendary_deeds.append(deed_data)

    def awaken_spirit(self, spirit_data: Dict[str, Any]):
        """觉醒器灵"""
        self.spirit_consciousness = True
        self.spirit_personality.update(spirit_data)

    def upgrade_treasure(self, new_grade: TreasureGrade) -> bool:
        """升级灵宝"""
        grade_order = [
            TreasureGrade.MORTAL,
            TreasureGrade.SPIRITUAL,
            TreasureGrade.TREASURE,
            TreasureGrade.KING,
            TreasureGrade.EMPEROR,
            TreasureGrade.SAINT,
            TreasureGrade.DIVINE,
            TreasureGrade.IMMORTAL,
            TreasureGrade.CHAOS
        ]
        
        current_index = grade_order.index(self.treasure_grade) if self.treasure_grade in grade_order else 0
        new_index = grade_order.index(new_grade) if new_grade in grade_order else 0
        
        if new_index > current_index:
            self.treasure_grade = new_grade
            return True
        return False

    def calculate_total_power(self) -> float:
        """计算总体威力"""
        power = self.spiritual_power
        
        # 品级加成
        grade_multiplier = {
            TreasureGrade.MORTAL: 1.0,
            TreasureGrade.SPIRITUAL: 1.5,
            TreasureGrade.TREASURE: 2.0,
            TreasureGrade.KING: 3.0,
            TreasureGrade.EMPEROR: 4.5,
            TreasureGrade.SAINT: 6.0,
            TreasureGrade.DIVINE: 8.0,
            TreasureGrade.IMMORTAL: 12.0,
            TreasureGrade.CHAOS: 20.0,
            TreasureGrade.UNKNOWN: 1.0
        }
        power *= grade_multiplier.get(self.treasure_grade, 1.0)
        
        # 灵性等级加成
        spiritual_bonus = {
            SpiritualLevel.NONE: 0,
            SpiritualLevel.WEAK: 0.1,
            SpiritualLevel.LOW: 0.2,
            SpiritualLevel.MEDIUM: 0.4,
            SpiritualLevel.HIGH: 0.7,
            SpiritualLevel.PEAK: 1.0,
            SpiritualLevel.TRANSCENDENT: 1.5,
            SpiritualLevel.UNKNOWN: 0
        }
        power *= (1 + spiritual_bonus.get(self.spiritual_level, 0))
        
        # 特殊能力加成
        power += len(self.special_abilities) * 10
        
        # 器灵加成
        if self.spirit_consciousness:
            power *= 1.3
            power += len(self.spirit_abilities) * 5
        
        return power

    def calculate_rarity_score(self) -> float:
        """计算稀有度评分"""
        rarity = 50.0  # 基础分数
        
        # 品级影响
        grade_rarity = {
            TreasureGrade.MORTAL: 0,
            TreasureGrade.SPIRITUAL: 10,
            TreasureGrade.TREASURE: 20,
            TreasureGrade.KING: 35,
            TreasureGrade.EMPEROR: 50,
            TreasureGrade.SAINT: 65,
            TreasureGrade.DIVINE: 80,
            TreasureGrade.IMMORTAL: 90,
            TreasureGrade.CHAOS: 95,
            TreasureGrade.UNKNOWN: 25
        }
        rarity += grade_rarity.get(self.treasure_grade, 0)
        
        # 稀有度系数
        rarity *= self.rarity_factor
        
        # 器灵加成
        if self.spirit_consciousness:
            rarity += 15
        
        # 成长潜力加成
        rarity += self.growth_potential * 0.1
        
        return min(100.0, max(0.0, rarity))

    def calculate_market_worth(self) -> float:
        """计算市场价值"""
        worth = self.market_value or 0.0
        
        # 威力影响
        total_power = self.calculate_total_power()
        worth += total_power * 100
        
        # 稀有度影响
        rarity = self.calculate_rarity_score()
        worth *= (1 + rarity / 100)
        
        # 历史价值
        worth += len(self.legendary_deeds) * 1000
        worth += len(self.previous_owners) * 500
        
        return worth

    def validate_consistency(self) -> List[str]:
        """验证灵宝体系一致性"""
        issues = []
        
        # 检查灵力值
        if self.spiritual_power < 0:
            issues.append("灵力值不能为负数")
        
        # 检查成功率
        if self.success_rate < 0 or self.success_rate > 100:
            issues.append("成功率必须在0-100之间")
        
        # 检查器灵与灵性等级的一致性
        if self.spirit_consciousness and self.spiritual_level == SpiritualLevel.NONE:
            issues.append("有器灵的灵宝不应该没有灵性")
        
        # 检查品级与威力的合理性
        if self.treasure_grade == TreasureGrade.CHAOS and self.spiritual_power < 1000:
            issues.append("混沌级灵宝的灵力值过低")
        
        return issues

    def generate_summary(self) -> str:
        """生成灵宝摘要"""
        summary_parts = []
        
        if self.description:
            summary_parts.append(self.description)
        
        # 灵宝类型
        type_map = {
            TreasureType.WEAPON: "法器武器",
            TreasureType.ARMOR: "护身法宝",
            TreasureType.ACCESSORY: "饰品法宝",
            TreasureType.PILL: "丹药",
            TreasureType.FORMATION: "阵法",
            TreasureType.TALISMAN: "符箓",
            TreasureType.CAULDRON: "鼎炉",
            TreasureType.SCROLL: "功法秘籍",
            TreasureType.SPIRIT_STONE: "灵石",
            TreasureType.HERB: "灵草",
            TreasureType.BEAST_CORE: "妖兽内丹",
            TreasureType.ARTIFACT: "上古神器",
            TreasureType.OTHER: "其他"
        }
        summary_parts.append(f"类型: {type_map.get(self.treasure_type, '未知')}")
        
        # 灵宝品级
        grade_map = {
            TreasureGrade.MORTAL: "凡品",
            TreasureGrade.SPIRITUAL: "灵品",
            TreasureGrade.TREASURE: "宝品",
            TreasureGrade.KING: "王品",
            TreasureGrade.EMPEROR: "皇品",
            TreasureGrade.SAINT: "圣品",
            TreasureGrade.DIVINE: "神品",
            TreasureGrade.IMMORTAL: "仙品",
            TreasureGrade.CHAOS: "混沌",
            TreasureGrade.UNKNOWN: "未知"
        }
        summary_parts.append(f"品级: {grade_map.get(self.treasure_grade, '未知')}")
        
        # 器灵状态
        if self.spirit_consciousness:
            summary_parts.append("有器灵")
        
        # 总体威力
        power = self.calculate_total_power()
        summary_parts.append(f"威力: {power:.1f}")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["total_power"] = self.calculate_total_power()
        result["rarity_score"] = self.calculate_rarity_score()
        result["market_worth"] = self.calculate_market_worth()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
