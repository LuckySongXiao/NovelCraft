"""
功法体系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class TechniqueType(str, Enum):
    """功法类型枚举"""
    INTERNAL = "internal"           # 内功
    EXTERNAL = "external"           # 外功
    MOVEMENT = "movement"           # 身法
    WEAPON = "weapon"               # 兵器
    MENTAL = "mental"               # 心法
    HEALING = "healing"             # 疗伤
    POISON = "poison"               # 毒功
    ILLUSION = "illusion"           # 幻术
    ELEMENTAL = "elemental"         # 元素
    FORBIDDEN = "forbidden"         # 禁术
    SECRET = "secret"               # 秘术
    OTHER = "other"                 # 其他


class TechniqueGrade(str, Enum):
    """功法品级枚举"""
    BASIC = "basic"                 # 基础级
    INTERMEDIATE = "intermediate"   # 中级
    ADVANCED = "advanced"           # 高级
    MASTER = "master"               # 宗师级
    GRANDMASTER = "grandmaster"     # 大宗师级
    LEGENDARY = "legendary"         # 传说级
    MYTHICAL = "mythical"           # 神话级
    DIVINE = "divine"               # 神级
    UNKNOWN = "unknown"             # 未知


class MartialArtsSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """功法体系模型"""

    __tablename__ = "martial_arts_systems"

    # 基本信息
    technique_type = Column(SQLEnum(TechniqueType), default=TechniqueType.INTERNAL, comment="功法类型")
    technique_grade = Column(SQLEnum(TechniqueGrade), default=TechniqueGrade.BASIC, comment="功法品级")
    
    # 功法属性
    power_source = Column(String(100), comment="力量来源")
    element_affinity = Column(JSON, comment="元素亲和")
    energy_type = Column(String(100), comment="能量类型")
    
    # 修炼要求
    prerequisites = Column(JSON, comment="修炼前提")
    required_level = Column(String(100), comment="所需境界")
    required_attributes = Column(JSON, comment="属性要求")
    
    # 功法效果
    primary_effects = Column(JSON, comment="主要效果")
    secondary_effects = Column(JSON, comment="次要效果")
    side_effects = Column(JSON, comment="副作用")
    
    # 修炼方法
    cultivation_method = Column(JSON, comment="修炼方法")
    training_stages = Column(JSON, comment="修炼阶段")
    mastery_levels = Column(JSON, comment="掌握程度")
    
    # 技能招式
    techniques = Column(JSON, comment="招式技能")
    combinations = Column(JSON, comment="连招组合")
    ultimate_moves = Column(JSON, comment="绝招")
    
    # 资源消耗
    energy_cost = Column(JSON, comment="能量消耗")
    material_requirements = Column(JSON, comment="材料需求")
    time_investment = Column(JSON, comment="时间投入")
    
    # 传承信息
    origin = Column(Text, comment="功法起源")
    creator = Column(String(200), comment="创始人")
    lineage = Column(JSON, comment="传承谱系")
    
    # 限制条件
    restrictions = Column(JSON, comment="修炼限制")
    forbidden_combinations = Column(JSON, comment="禁忌组合")
    compatibility = Column(JSON, comment="兼容性")
    
    # 威力评估
    offensive_power = Column(Float, default=0.0, comment="攻击威力")
    defensive_power = Column(Float, default=0.0, comment="防御能力")
    utility_value = Column(Float, default=0.0, comment="实用价值")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")
    parent_technique_id = Column(Integer, ForeignKey("martial_arts_systems.id"), comment="上级功法ID")

    children = relationship("MartialArtsSystem", backref="parent", remote_side="MartialArtsSystem.id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.element_affinity:
            self.element_affinity = []
        if not self.prerequisites:
            self.prerequisites = {}
        if not self.required_attributes:
            self.required_attributes = {}
        if not self.primary_effects:
            self.primary_effects = []
        if not self.secondary_effects:
            self.secondary_effects = []
        if not self.side_effects:
            self.side_effects = []
        if not self.cultivation_method:
            self.cultivation_method = {}
        if not self.training_stages:
            self.training_stages = []
        if not self.mastery_levels:
            self.mastery_levels = []
        if not self.techniques:
            self.techniques = []
        if not self.combinations:
            self.combinations = []
        if not self.ultimate_moves:
            self.ultimate_moves = []
        if not self.energy_cost:
            self.energy_cost = {}
        if not self.material_requirements:
            self.material_requirements = []
        if not self.time_investment:
            self.time_investment = {}
        if not self.lineage:
            self.lineage = []
        if not self.restrictions:
            self.restrictions = []
        if not self.forbidden_combinations:
            self.forbidden_combinations = []
        if not self.compatibility:
            self.compatibility = {}

    def add_technique(self, technique_data: Dict[str, Any]):
        """添加招式"""
        self.techniques.append(technique_data)

    def add_training_stage(self, stage_data: Dict[str, Any]):
        """添加修炼阶段"""
        self.training_stages.append(stage_data)

    def add_effect(self, effect_type: str, effect_data: Dict[str, Any]):
        """添加效果"""
        if effect_type == "primary":
            self.primary_effects.append(effect_data)
        elif effect_type == "secondary":
            self.secondary_effects.append(effect_data)
        elif effect_type == "side":
            self.side_effects.append(effect_data)

    def add_combination(self, combo_data: Dict[str, Any]):
        """添加连招组合"""
        self.combinations.append(combo_data)

    def add_ultimate_move(self, move_data: Dict[str, Any]):
        """添加绝招"""
        self.ultimate_moves.append(move_data)

    def add_lineage_member(self, member_data: Dict[str, Any]):
        """添加传承成员"""
        self.lineage.append(member_data)

    def get_technique_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取招式"""
        for technique in self.techniques:
            if technique.get("name") == name:
                return technique
        return None

    def get_stage_by_level(self, level: int) -> Dict[str, Any]:
        """根据等级获取修炼阶段"""
        for stage in self.training_stages:
            if stage.get("level") == level:
                return stage
        return None

    def calculate_total_power(self) -> float:
        """计算总体威力"""
        # 基础威力
        base_power = (self.offensive_power + self.defensive_power + self.utility_value) / 3
        
        # 品级加成
        grade_multiplier = {
            TechniqueGrade.BASIC: 1.0,
            TechniqueGrade.INTERMEDIATE: 1.2,
            TechniqueGrade.ADVANCED: 1.5,
            TechniqueGrade.MASTER: 2.0,
            TechniqueGrade.GRANDMASTER: 2.5,
            TechniqueGrade.LEGENDARY: 3.0,
            TechniqueGrade.MYTHICAL: 4.0,
            TechniqueGrade.DIVINE: 5.0,
            TechniqueGrade.UNKNOWN: 1.0
        }
        
        multiplier = grade_multiplier.get(self.technique_grade, 1.0)
        total_power = base_power * multiplier
        
        # 招式数量加成
        technique_bonus = len(self.techniques) * 0.1
        
        # 绝招加成
        ultimate_bonus = len(self.ultimate_moves) * 0.5
        
        return total_power + technique_bonus + ultimate_bonus

    def calculate_difficulty(self) -> float:
        """计算修炼难度"""
        difficulty = 50.0  # 基础难度
        
        # 品级影响
        grade_difficulty = {
            TechniqueGrade.BASIC: 0,
            TechniqueGrade.INTERMEDIATE: 10,
            TechniqueGrade.ADVANCED: 20,
            TechniqueGrade.MASTER: 30,
            TechniqueGrade.GRANDMASTER: 40,
            TechniqueGrade.LEGENDARY: 50,
            TechniqueGrade.MYTHICAL: 60,
            TechniqueGrade.DIVINE: 70,
            TechniqueGrade.UNKNOWN: 25
        }
        
        difficulty += grade_difficulty.get(self.technique_grade, 0)
        
        # 前提条件影响
        if self.prerequisites:
            difficulty += len(self.prerequisites) * 5
        
        # 限制条件影响
        difficulty += len(self.restrictions) * 3
        
        # 副作用影响
        difficulty += len(self.side_effects) * 2
        
        return min(100.0, max(0.0, difficulty))

    def validate_consistency(self) -> List[str]:
        """验证功法体系一致性"""
        issues = []
        
        # 检查威力与品级的一致性
        expected_power = {
            TechniqueGrade.BASIC: (0, 30),
            TechniqueGrade.INTERMEDIATE: (20, 50),
            TechniqueGrade.ADVANCED: (40, 70),
            TechniqueGrade.MASTER: (60, 85),
            TechniqueGrade.GRANDMASTER: (75, 95),
            TechniqueGrade.LEGENDARY: (85, 100),
            TechniqueGrade.MYTHICAL: (95, 100),
            TechniqueGrade.DIVINE: (100, 100)
        }
        
        if self.technique_grade in expected_power:
            min_power, max_power = expected_power[self.technique_grade]
            total_power = self.calculate_total_power()
            if total_power < min_power or total_power > max_power:
                issues.append(f"功法威力 {total_power:.1f} 与品级 {self.technique_grade} 不匹配")
        
        # 检查禁忌组合
        for forbidden in self.forbidden_combinations:
            technique_name = forbidden.get("technique")
            if technique_name and self.get_technique_by_name(technique_name):
                issues.append(f"包含禁忌组合: {technique_name}")
        
        return issues

    def generate_summary(self) -> str:
        """生成功法摘要"""
        summary_parts = []
        
        if self.description:
            summary_parts.append(self.description)
        
        # 功法类型
        type_map = {
            TechniqueType.INTERNAL: "内功",
            TechniqueType.EXTERNAL: "外功",
            TechniqueType.MOVEMENT: "身法",
            TechniqueType.WEAPON: "兵器",
            TechniqueType.MENTAL: "心法",
            TechniqueType.HEALING: "疗伤",
            TechniqueType.POISON: "毒功",
            TechniqueType.ILLUSION: "幻术",
            TechniqueType.ELEMENTAL: "元素",
            TechniqueType.FORBIDDEN: "禁术",
            TechniqueType.SECRET: "秘术",
            TechniqueType.OTHER: "其他"
        }
        summary_parts.append(f"类型: {type_map.get(self.technique_type, '未知')}")
        
        # 功法品级
        grade_map = {
            TechniqueGrade.BASIC: "基础级",
            TechniqueGrade.INTERMEDIATE: "中级",
            TechniqueGrade.ADVANCED: "高级",
            TechniqueGrade.MASTER: "宗师级",
            TechniqueGrade.GRANDMASTER: "大宗师级",
            TechniqueGrade.LEGENDARY: "传说级",
            TechniqueGrade.MYTHICAL: "神话级",
            TechniqueGrade.DIVINE: "神级",
            TechniqueGrade.UNKNOWN: "未知"
        }
        summary_parts.append(f"品级: {grade_map.get(self.technique_grade, '未知')}")
        
        # 招式数量
        summary_parts.append(f"招式: {len(self.techniques)}个")
        
        # 总体威力
        power = self.calculate_total_power()
        summary_parts.append(f"威力: {power:.1f}/100")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["total_power"] = self.calculate_total_power()
        result["difficulty"] = self.calculate_difficulty()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
