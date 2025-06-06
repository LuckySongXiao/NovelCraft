"""
装备体系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class EquipmentType(str, Enum):
    """装备类型枚举"""
    WEAPON = "weapon"               # 武器
    ARMOR = "armor"                 # 防具
    ACCESSORY = "accessory"         # 饰品
    CONSUMABLE = "consumable"       # 消耗品
    MATERIAL = "material"           # 材料
    TOOL = "tool"                   # 工具
    MOUNT = "mount"                 # 坐骑
    ARTIFACT = "artifact"           # 神器
    TALISMAN = "talisman"           # 法宝
    PILL = "pill"                   # 丹药
    SCROLL = "scroll"               # 卷轴
    OTHER = "other"                 # 其他


class EquipmentGrade(str, Enum):
    """装备品级枚举"""
    COMMON = "common"               # 普通
    UNCOMMON = "uncommon"           # 优秀
    RARE = "rare"                   # 稀有
    EPIC = "epic"                   # 史诗
    LEGENDARY = "legendary"         # 传说
    MYTHICAL = "mythical"           # 神话
    DIVINE = "divine"               # 神级
    TRANSCENDENT = "transcendent"   # 超越
    UNKNOWN = "unknown"             # 未知


class EquipmentSlot(str, Enum):
    """装备槽位枚举"""
    MAIN_HAND = "main_hand"         # 主手
    OFF_HAND = "off_hand"           # 副手
    TWO_HAND = "two_hand"           # 双手
    HEAD = "head"                   # 头部
    CHEST = "chest"                 # 胸部
    LEGS = "legs"                   # 腿部
    FEET = "feet"                   # 脚部
    HANDS = "hands"                 # 手部
    NECK = "neck"                   # 颈部
    RING = "ring"                   # 戒指
    BELT = "belt"                   # 腰带
    CLOAK = "cloak"                 # 斗篷
    NONE = "none"                   # 无槽位


class EquipmentSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """装备体系模型"""

    __tablename__ = "equipment_systems"

    # 基本信息
    equipment_type = Column(SQLEnum(EquipmentType), default=EquipmentType.WEAPON, comment="装备类型")
    equipment_grade = Column(SQLEnum(EquipmentGrade), default=EquipmentGrade.COMMON, comment="装备品级")
    equipment_slot = Column(SQLEnum(EquipmentSlot), default=EquipmentSlot.NONE, comment="装备槽位")

    # 装备属性
    base_attributes = Column(JSON, comment="基础属性")
    bonus_attributes = Column(JSON, comment="加成属性")
    special_effects = Column(JSON, comment="特殊效果")

    # 基础战斗属性
    offensive_power = Column(Float, default=0.0, comment="攻击力")
    defensive_power = Column(Float, default=0.0, comment="防御力")

    # 使用要求
    level_requirement = Column(Integer, default=1, comment="等级要求")
    class_requirement = Column(JSON, comment="职业要求")
    attribute_requirement = Column(JSON, comment="属性要求")

    # 装备数据
    durability = Column(Integer, default=100, comment="耐久度")
    max_durability = Column(Integer, default=100, comment="最大耐久度")
    weight = Column(Float, default=0.0, comment="重量")
    value = Column(Integer, default=0, comment="价值")

    # 强化系统
    enhancement_level = Column(Integer, default=0, comment="强化等级")
    max_enhancement = Column(Integer, default=10, comment="最大强化等级")
    enhancement_materials = Column(JSON, comment="强化材料")

    # 套装系统
    set_name = Column(String(200), comment="套装名称")
    set_pieces = Column(JSON, comment="套装部件")
    set_bonuses = Column(JSON, comment="套装效果")

    # 制作信息
    crafting_recipe = Column(JSON, comment="制作配方")
    crafting_materials = Column(JSON, comment="制作材料")
    crafting_skill = Column(String(100), comment="制作技能")
    crafting_level = Column(Integer, default=1, comment="制作等级")

    # 获取方式
    drop_sources = Column(JSON, comment="掉落来源")
    quest_rewards = Column(JSON, comment="任务奖励")
    shop_availability = Column(JSON, comment="商店购买")

    # 装备历史
    creation_story = Column(Text, comment="装备来历")
    previous_owners = Column(JSON, comment="历任主人")
    legendary_deeds = Column(JSON, comment="传奇事迹")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.base_attributes:
            self.base_attributes = {}
        if not self.bonus_attributes:
            self.bonus_attributes = {}
        if not self.special_effects:
            self.special_effects = []
        if not self.class_requirement:
            self.class_requirement = []
        if not self.attribute_requirement:
            self.attribute_requirement = {}
        if not self.enhancement_materials:
            self.enhancement_materials = []
        if not self.set_pieces:
            self.set_pieces = []
        if not self.set_bonuses:
            self.set_bonuses = []
        if not self.crafting_recipe:
            self.crafting_recipe = {}
        if not self.crafting_materials:
            self.crafting_materials = []
        if not self.drop_sources:
            self.drop_sources = []
        if not self.quest_rewards:
            self.quest_rewards = []
        if not self.shop_availability:
            self.shop_availability = []
        if not self.previous_owners:
            self.previous_owners = []
        if not self.legendary_deeds:
            self.legendary_deeds = []

    def add_special_effect(self, effect_data: Dict[str, Any]):
        """添加特殊效果"""
        self.special_effects.append(effect_data)

    def add_special_ability(self, ability_data: Dict[str, Any]):
        """添加特殊能力（兼容性方法）"""
        self.add_special_effect(ability_data)

    def add_enhancement_material(self, material_data: Dict[str, Any]):
        """添加强化材料"""
        self.enhancement_materials.append(material_data)

    def add_set_piece(self, piece_data: Dict[str, Any]):
        """添加套装部件"""
        self.set_pieces.append(piece_data)

    def add_set_bonus(self, bonus_data: Dict[str, Any]):
        """添加套装效果"""
        self.set_bonuses.append(bonus_data)

    def add_drop_source(self, source_data: Dict[str, Any]):
        """添加掉落来源"""
        self.drop_sources.append(source_data)

    def enhance_equipment(self, target_level: int) -> bool:
        """强化装备"""
        if target_level <= self.max_enhancement and target_level > self.enhancement_level:
            self.enhancement_level = target_level
            return True
        return False

    def repair_equipment(self, repair_amount: int = None):
        """修理装备"""
        if repair_amount is None:
            self.durability = self.max_durability
        else:
            self.durability = min(self.max_durability, self.durability + repair_amount)

    def calculate_total_attributes(self) -> Dict[str, Any]:
        """计算总属性"""
        total_attrs = self.base_attributes.copy()

        # 加成属性
        for attr, value in self.bonus_attributes.items():
            if attr in total_attrs:
                total_attrs[attr] += value
            else:
                total_attrs[attr] = value

        # 强化加成
        enhancement_multiplier = 1 + (self.enhancement_level * 0.1)
        for attr in total_attrs:
            if isinstance(total_attrs[attr], (int, float)):
                total_attrs[attr] = int(total_attrs[attr] * enhancement_multiplier)

        return total_attrs

    def calculate_equipment_score(self) -> float:
        """计算装备评分"""
        score = 50.0  # 基础分数

        # 品级加成
        grade_bonus = {
            EquipmentGrade.COMMON: 0,
            EquipmentGrade.UNCOMMON: 10,
            EquipmentGrade.RARE: 20,
            EquipmentGrade.EPIC: 30,
            EquipmentGrade.LEGENDARY: 40,
            EquipmentGrade.MYTHICAL: 50,
            EquipmentGrade.DIVINE: 60,
            EquipmentGrade.TRANSCENDENT: 70,
            EquipmentGrade.UNKNOWN: 0
        }
        score += grade_bonus.get(self.equipment_grade, 0)

        # 强化等级加成
        enhancement_level = self.enhancement_level or 0
        score += enhancement_level * 2

        # 特殊效果加成
        score += len(self.special_effects) * 3

        # 套装加成
        if self.set_name:
            score += 10

        # 战斗属性加成
        if self.offensive_power is not None and self.offensive_power > 0:
            score += min(self.offensive_power / 10, 20)  # 攻击力加成，最多20分
        if self.defensive_power is not None and self.defensive_power > 0:
            score += min(self.defensive_power / 10, 20)  # 防御力加成，最多20分

        return min(100.0, max(0.0, score))

    def validate_consistency(self) -> List[str]:
        """验证装备一致性"""
        issues = []

        # 检查耐久度
        if self.durability > self.max_durability:
            issues.append("当前耐久度超过最大耐久度")

        # 检查强化等级
        if self.enhancement_level > self.max_enhancement:
            issues.append("强化等级超过最大限制")

        # 检查装备槽位与类型的一致性
        weapon_slots = [EquipmentSlot.MAIN_HAND, EquipmentSlot.OFF_HAND, EquipmentSlot.TWO_HAND]
        if self.equipment_type == EquipmentType.WEAPON and self.equipment_slot not in weapon_slots:
            issues.append("武器类型与装备槽位不匹配")

        return issues

    def generate_summary(self) -> str:
        """生成装备摘要"""
        summary_parts = []

        if self.description:
            summary_parts.append(self.description)

        # 装备类型
        type_map = {
            EquipmentType.WEAPON: "武器",
            EquipmentType.ARMOR: "防具",
            EquipmentType.ACCESSORY: "饰品",
            EquipmentType.CONSUMABLE: "消耗品",
            EquipmentType.MATERIAL: "材料",
            EquipmentType.TOOL: "工具",
            EquipmentType.MOUNT: "坐骑",
            EquipmentType.ARTIFACT: "神器",
            EquipmentType.TALISMAN: "法宝",
            EquipmentType.PILL: "丹药",
            EquipmentType.SCROLL: "卷轴",
            EquipmentType.OTHER: "其他"
        }
        summary_parts.append(f"类型: {type_map.get(self.equipment_type, '未知')}")

        # 装备品级
        grade_map = {
            EquipmentGrade.COMMON: "普通",
            EquipmentGrade.UNCOMMON: "优秀",
            EquipmentGrade.RARE: "稀有",
            EquipmentGrade.EPIC: "史诗",
            EquipmentGrade.LEGENDARY: "传说",
            EquipmentGrade.MYTHICAL: "神话",
            EquipmentGrade.DIVINE: "神级",
            EquipmentGrade.TRANSCENDENT: "超越",
            EquipmentGrade.UNKNOWN: "未知"
        }
        summary_parts.append(f"品级: {grade_map.get(self.equipment_grade, '未知')}")

        # 强化等级
        if self.enhancement_level > 0:
            summary_parts.append(f"强化: +{self.enhancement_level}")

        # 装备评分
        score = self.calculate_equipment_score()
        summary_parts.append(f"评分: {score:.1f}/100")

        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["total_attributes"] = self.calculate_total_attributes()
        result["equipment_score"] = self.calculate_equipment_score()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
