"""
修炼体系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class PowerType(str, Enum):
    """能力类型枚举"""
    PHYSICAL = "physical"        # 体修
    SPIRITUAL = "spiritual"      # 神修
    ELEMENTAL = "elemental"      # 元素
    MENTAL = "mental"           # 精神
    BLOODLINE = "bloodline"     # 血脉
    TECHNIQUE = "technique"     # 技法
    ARTIFACT = "artifact"       # 法宝
    OTHER = "other"             # 其他


class CultivationSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """修炼体系模型"""

    __tablename__ = "cultivation_systems"

    # 基本信息
    system_type = Column(String(50), nullable=False, comment="体系类型")
    power_source = Column(String(100), comment="力量来源")

    # 等级体系
    levels = Column(JSON, comment="等级划分")
    level_requirements = Column(JSON, comment="等级要求")
    breakthrough_conditions = Column(JSON, comment="突破条件")

    # 能力分类
    abilities = Column(JSON, comment="能力分类")
    skills = Column(JSON, comment="技能体系")
    techniques = Column(JSON, comment="功法技巧")

    # 修炼资源
    resources = Column(JSON, comment="修炼资源")
    materials = Column(JSON, comment="修炼材料")
    environments = Column(JSON, comment="修炼环境")

    # 特殊规则
    rules = Column(JSON, comment="修炼规则")
    restrictions = Column(JSON, comment="限制条件")
    side_effects = Column(JSON, comment="副作用")

    # 天赋血脉
    talents = Column(JSON, comment="天赋体系")
    bloodlines = Column(JSON, comment="血脉体系")
    constitutions = Column(JSON, comment="特殊体质")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    parent_id = Column(Integer, ForeignKey("cultivation_systems.id"), comment="父体系ID")

    children = relationship("CultivationSystem", backref="parent", remote_side="CultivationSystem.id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.levels:
            self.levels = []
        if not self.level_requirements:
            self.level_requirements = {}
        if not self.breakthrough_conditions:
            self.breakthrough_conditions = {}
        if not self.abilities:
            self.abilities = {}
        if not self.skills:
            self.skills = {}
        if not self.techniques:
            self.techniques = {}
        if not self.resources:
            self.resources = {}
        if not self.materials:
            self.materials = {}
        if not self.environments:
            self.environments = {}
        if not self.rules:
            self.rules = {}
        if not self.restrictions:
            self.restrictions = {}
        if not self.side_effects:
            self.side_effects = {}
        if not self.talents:
            self.talents = {}
        if not self.bloodlines:
            self.bloodlines = {}
        if not self.constitutions:
            self.constitutions = {}

    def add_level(self, level_data: Dict[str, Any]):
        """添加等级"""
        self.levels.append(level_data)
        # 按等级排序
        self.levels.sort(key=lambda x: x.get("order", 0))

    def set_level_requirement(self, level_name: str, requirements: Dict[str, Any]):
        """设置等级要求"""
        self.level_requirements[level_name] = requirements

    def add_ability(self, ability_type: str, ability_data: Dict[str, Any]):
        """添加能力"""
        if ability_type not in self.abilities:
            self.abilities[ability_type] = []
        self.abilities[ability_type].append(ability_data)

    def add_technique(self, technique_data: Dict[str, Any]):
        """添加功法"""
        technique_type = technique_data.get("type", "general")
        if technique_type not in self.techniques:
            self.techniques[technique_type] = []
        self.techniques[technique_type].append(technique_data)

    def add_resource(self, resource_type: str, resource_data: Dict[str, Any]):
        """添加修炼资源"""
        if resource_type not in self.resources:
            self.resources[resource_type] = []
        self.resources[resource_type].append(resource_data)

    def set_rule(self, rule_name: str, rule_data: Dict[str, Any]):
        """设置修炼规则"""
        self.rules[rule_name] = rule_data

    def add_talent(self, talent_data: Dict[str, Any]):
        """添加天赋"""
        talent_type = talent_data.get("type", "general")
        if talent_type not in self.talents:
            self.talents[talent_type] = []
        self.talents[talent_type].append(talent_data)

    def add_bloodline(self, bloodline_data: Dict[str, Any]):
        """添加血脉"""
        bloodline_type = bloodline_data.get("type", "general")
        if bloodline_type not in self.bloodlines:
            self.bloodlines[bloodline_type] = []
        self.bloodlines[bloodline_type].append(bloodline_data)

    def get_level_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取等级"""
        for level in self.levels:
            if level.get("name") == name:
                return level
        return None

    def get_level_by_order(self, order: int) -> Dict[str, Any]:
        """根据顺序获取等级"""
        for level in self.levels:
            if level.get("order") == order:
                return level
        return None

    def get_abilities_by_type(self, ability_type: str) -> List[Dict[str, Any]]:
        """根据类型获取能力"""
        return self.abilities.get(ability_type, [])

    def get_techniques_by_level(self, level_name: str) -> List[Dict[str, Any]]:
        """根据等级获取可用功法"""
        available_techniques = []
        for technique_type, techniques in self.techniques.items():
            for technique in techniques:
                required_level = technique.get("required_level", "")
                if self._is_level_sufficient(level_name, required_level):
                    available_techniques.append(technique)
        return available_techniques

    def _is_level_sufficient(self, current_level: str, required_level: str) -> bool:
        """检查等级是否满足要求"""
        current_order = self._get_level_order(current_level)
        required_order = self._get_level_order(required_level)
        return current_order >= required_order

    def _get_level_order(self, level_name: str) -> int:
        """获取等级顺序"""
        level = self.get_level_by_name(level_name)
        return level.get("order", 0) if level else 0

    def calculate_power_level(self, character_data: Dict[str, Any]) -> float:
        """计算角色实力等级"""
        base_level = character_data.get("cultivation_level", "")
        level_order = self._get_level_order(base_level)

        # 基础实力
        base_power = level_order * 100

        # 天赋加成
        talents = character_data.get("talents", [])
        talent_bonus = sum(self._get_talent_bonus(talent) for talent in talents)

        # 功法加成
        techniques = character_data.get("techniques", [])
        technique_bonus = sum(self._get_technique_bonus(technique) for technique in techniques)

        # 血脉加成
        bloodline = character_data.get("bloodline", "")
        bloodline_bonus = self._get_bloodline_bonus(bloodline)

        total_power = base_power + talent_bonus + technique_bonus + bloodline_bonus
        return total_power

    def _get_talent_bonus(self, talent_name: str) -> float:
        """获取天赋加成"""
        for talent_type, talents in self.talents.items():
            for talent in talents:
                if talent.get("name") == talent_name:
                    return talent.get("power_bonus", 0)
        return 0

    def _get_technique_bonus(self, technique_name: str) -> float:
        """获取功法加成"""
        for technique_type, techniques in self.techniques.items():
            for technique in techniques:
                if technique.get("name") == technique_name:
                    return technique.get("power_bonus", 0)
        return 0

    def _get_bloodline_bonus(self, bloodline_name: str) -> float:
        """获取血脉加成"""
        for bloodline_type, bloodlines in self.bloodlines.items():
            for bloodline in bloodlines:
                if bloodline.get("name") == bloodline_name:
                    return bloodline.get("power_bonus", 0)
        return 0

    def validate_system_consistency(self) -> List[str]:
        """验证体系一致性"""
        issues = []

        # 检查等级顺序
        orders = [level.get("order", 0) for level in self.levels]
        if len(orders) != len(set(orders)):
            issues.append("等级顺序存在重复")

        # 检查功法等级要求
        for technique_type, techniques in self.techniques.items():
            for technique in techniques:
                required_level = technique.get("required_level", "")
                if required_level and not self.get_level_by_name(required_level):
                    issues.append(f"功法 {technique.get('name', '未知')} 要求的等级 {required_level} 不存在")

        return issues

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["level_count"] = len(self.levels)
        result["ability_count"] = sum(len(abilities) for abilities in self.abilities.values())
        result["technique_count"] = sum(len(techniques) for techniques in self.techniques.values())
        result["consistency_issues"] = self.validate_system_consistency()
        result["tags"] = self.get_tags()
        return result
