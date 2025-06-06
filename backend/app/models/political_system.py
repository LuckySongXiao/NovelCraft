"""
政治体系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class GovernmentType(str, Enum):
    """政府类型枚举"""
    MONARCHY = "monarchy"           # 君主制
    REPUBLIC = "republic"           # 共和制
    DEMOCRACY = "democracy"         # 民主制
    AUTOCRACY = "autocracy"         # 专制
    OLIGARCHY = "oligarchy"         # 寡头制
    THEOCRACY = "theocracy"         # 神权制
    FEDERATION = "federation"       # 联邦制
    CONFEDERATION = "confederation" # 邦联制
    EMPIRE = "empire"              # 帝制
    TRIBAL = "tribal"              # 部落制
    OTHER = "other"                # 其他


class PowerStructure(str, Enum):
    """权力结构枚举"""
    CENTRALIZED = "centralized"     # 中央集权
    DECENTRALIZED = "decentralized" # 分权制
    FEDERAL = "federal"             # 联邦制
    UNITARY = "unitary"            # 单一制
    MIXED = "mixed"                # 混合制


class PoliticalSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """政治体系模型"""

    __tablename__ = "political_systems"

    # 基本信息
    government_type = Column(SQLEnum(GovernmentType), default=GovernmentType.MONARCHY, comment="政府类型")
    power_structure = Column(SQLEnum(PowerStructure), default=PowerStructure.CENTRALIZED, comment="权力结构")
    
    # 政府组织
    government_structure = Column(JSON, comment="政府结构")
    leadership = Column(JSON, comment="领导层")
    institutions = Column(JSON, comment="政治机构")
    
    # 法律体系
    legal_system = Column(JSON, comment="法律体系")
    laws = Column(JSON, comment="法律条文")
    enforcement = Column(JSON, comment="执法机构")
    
    # 权力分配
    power_distribution = Column(JSON, comment="权力分配")
    checks_balances = Column(JSON, comment="制衡机制")
    succession_rules = Column(JSON, comment="继承规则")
    
    # 行政区划
    administrative_divisions = Column(JSON, comment="行政区划")
    local_governance = Column(JSON, comment="地方治理")
    
    # 政治文化
    political_culture = Column(JSON, comment="政治文化")
    ideology = Column(Text, comment="政治理念")
    traditions = Column(JSON, comment="政治传统")
    
    # 对外关系
    diplomacy = Column(JSON, comment="外交政策")
    alliances = Column(JSON, comment="政治联盟")
    treaties = Column(JSON, comment="条约协议")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.government_structure:
            self.government_structure = {}
        if not self.leadership:
            self.leadership = {}
        if not self.institutions:
            self.institutions = {}
        if not self.legal_system:
            self.legal_system = {}
        if not self.laws:
            self.laws = []
        if not self.enforcement:
            self.enforcement = {}
        if not self.power_distribution:
            self.power_distribution = {}
        if not self.checks_balances:
            self.checks_balances = {}
        if not self.succession_rules:
            self.succession_rules = {}
        if not self.administrative_divisions:
            self.administrative_divisions = {}
        if not self.local_governance:
            self.local_governance = {}
        if not self.political_culture:
            self.political_culture = {}
        if not self.traditions:
            self.traditions = []
        if not self.diplomacy:
            self.diplomacy = {}
        if not self.alliances:
            self.alliances = []
        if not self.treaties:
            self.treaties = []

    def add_institution(self, institution_data: Dict[str, Any]):
        """添加政治机构"""
        if "institutions" not in self.institutions:
            self.institutions["institutions"] = []
        self.institutions["institutions"].append(institution_data)

    def add_law(self, law_data: Dict[str, Any]):
        """添加法律"""
        self.laws.append(law_data)

    def add_administrative_division(self, division_data: Dict[str, Any]):
        """添加行政区划"""
        if "divisions" not in self.administrative_divisions:
            self.administrative_divisions["divisions"] = []
        self.administrative_divisions["divisions"].append(division_data)

    def add_alliance(self, alliance_data: Dict[str, Any]):
        """添加政治联盟"""
        self.alliances.append(alliance_data)

    def add_treaty(self, treaty_data: Dict[str, Any]):
        """添加条约"""
        self.treaties.append(treaty_data)

    def get_institution_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取政治机构"""
        institutions = self.institutions.get("institutions", [])
        for institution in institutions:
            if institution.get("name") == name:
                return institution
        return None

    def get_law_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取法律"""
        for law in self.laws:
            if law.get("name") == name:
                return law
        return None

    def calculate_stability_score(self) -> float:
        """计算政治稳定性评分"""
        score = 50.0  # 基础分数
        
        # 权力结构稳定性
        if self.power_structure == PowerStructure.CENTRALIZED:
            score += 10
        elif self.power_structure == PowerStructure.FEDERAL:
            score += 5
        
        # 制衡机制
        if self.checks_balances:
            score += len(self.checks_balances) * 2
        
        # 法律体系完善度
        if self.legal_system:
            score += len(self.legal_system) * 3
        
        # 政治传统
        if self.traditions:
            score += len(self.traditions) * 2
        
        return min(100.0, max(0.0, score))

    def validate_consistency(self) -> List[str]:
        """验证政治体系一致性"""
        issues = []
        
        # 检查政府类型与权力结构的一致性
        if self.government_type == GovernmentType.DEMOCRACY and self.power_structure == PowerStructure.CENTRALIZED:
            issues.append("民主制与中央集权制存在矛盾")
        
        # 检查继承规则与政府类型的一致性
        if self.government_type == GovernmentType.REPUBLIC and self.succession_rules:
            if "hereditary" in str(self.succession_rules):
                issues.append("共和制不应有世袭继承规则")
        
        return issues

    def generate_summary(self) -> str:
        """生成政治体系摘要"""
        summary_parts = []
        
        if self.description:
            summary_parts.append(self.description)
        
        # 政府类型
        gov_type_map = {
            GovernmentType.MONARCHY: "君主制",
            GovernmentType.REPUBLIC: "共和制",
            GovernmentType.DEMOCRACY: "民主制",
            GovernmentType.AUTOCRACY: "专制",
            GovernmentType.OLIGARCHY: "寡头制",
            GovernmentType.THEOCRACY: "神权制",
            GovernmentType.FEDERATION: "联邦制",
            GovernmentType.CONFEDERATION: "邦联制",
            GovernmentType.EMPIRE: "帝制",
            GovernmentType.TRIBAL: "部落制",
            GovernmentType.OTHER: "其他"
        }
        summary_parts.append(f"政府类型: {gov_type_map.get(self.government_type, '未知')}")
        
        # 权力结构
        power_map = {
            PowerStructure.CENTRALIZED: "中央集权",
            PowerStructure.DECENTRALIZED: "分权制",
            PowerStructure.FEDERAL: "联邦制",
            PowerStructure.UNITARY: "单一制",
            PowerStructure.MIXED: "混合制"
        }
        summary_parts.append(f"权力结构: {power_map.get(self.power_structure, '未知')}")
        
        # 稳定性评分
        stability = self.calculate_stability_score()
        summary_parts.append(f"稳定性: {stability:.1f}/100")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["stability_score"] = self.calculate_stability_score()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
