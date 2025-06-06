"""
种族分布数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class PopulationDensity(str, Enum):
    """人口密度枚举"""
    SPARSE = "sparse"               # 稀疏
    LOW = "low"                     # 低密度
    MODERATE = "moderate"           # 中等密度
    HIGH = "high"                   # 高密度
    DENSE = "dense"                 # 密集
    OVERCROWDED = "overcrowded"     # 过度拥挤
    UNKNOWN = "unknown"             # 未知


class SettlementType(str, Enum):
    """定居类型枚举"""
    NOMADIC = "nomadic"             # 游牧
    SEMI_NOMADIC = "semi_nomadic"   # 半游牧
    SETTLED = "settled"             # 定居
    URBAN = "urban"                 # 城市
    TRIBAL = "tribal"               # 部落
    ISOLATED = "isolated"           # 孤立
    MIXED = "mixed"                 # 混合
    OTHER = "other"                 # 其他


class DominanceLevel(str, Enum):
    """统治程度枚举"""
    DOMINANT = "dominant"           # 统治
    MAJORITY = "majority"           # 多数
    SIGNIFICANT = "significant"     # 重要
    MINORITY = "minority"           # 少数
    RARE = "rare"                   # 稀少
    EXTINCT = "extinct"             # 灭绝
    UNKNOWN = "unknown"             # 未知


class RaceDistribution(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """种族分布模型"""

    __tablename__ = "race_distributions"

    # 基本信息
    race_name = Column(String(200), comment="种族名称")
    population_density = Column(SQLEnum(PopulationDensity), default=PopulationDensity.MODERATE, comment="人口密度")
    settlement_type = Column(SQLEnum(SettlementType), default=SettlementType.SETTLED, comment="定居类型")
    dominance_level = Column(SQLEnum(DominanceLevel), default=DominanceLevel.MINORITY, comment="统治程度")
    
    # 人口统计
    total_population = Column(Integer, comment="总人口")
    population_growth_rate = Column(Float, comment="人口增长率")
    age_distribution = Column(JSON, comment="年龄分布")
    gender_ratio = Column(JSON, comment="性别比例")
    
    # 地理分布
    primary_territories = Column(JSON, comment="主要领土")
    secondary_regions = Column(JSON, comment="次要区域")
    migration_routes = Column(JSON, comment="迁徙路线")
    seasonal_movements = Column(JSON, comment="季节性迁移")
    
    # 定居模式
    settlement_patterns = Column(JSON, comment="定居模式")
    major_cities = Column(JSON, comment="主要城市")
    tribal_areas = Column(JSON, comment="部落区域")
    sacred_lands = Column(JSON, comment="圣地")
    
    # 环境适应
    preferred_climate = Column(JSON, comment="偏好气候")
    terrain_adaptation = Column(JSON, comment="地形适应")
    resource_dependencies = Column(JSON, comment="资源依赖")
    environmental_threats = Column(JSON, comment="环境威胁")
    
    # 社会结构
    social_organization = Column(JSON, comment="社会组织")
    leadership_structure = Column(JSON, comment="领导结构")
    cultural_centers = Column(JSON, comment="文化中心")
    religious_sites = Column(JSON, comment="宗教场所")
    
    # 种族关系
    allied_races = Column(JSON, comment="友好种族")
    hostile_races = Column(JSON, comment="敌对种族")
    neutral_races = Column(JSON, comment="中立种族")
    mixed_communities = Column(JSON, comment="混合社区")
    
    # 经济活动
    primary_occupations = Column(JSON, comment="主要职业")
    trade_specialties = Column(JSON, comment="贸易特长")
    economic_centers = Column(JSON, comment="经济中心")
    resource_control = Column(JSON, comment="资源控制")
    
    # 历史变迁
    historical_migrations = Column(JSON, comment="历史迁移")
    territorial_changes = Column(JSON, comment="领土变化")
    population_events = Column(JSON, comment="人口事件")
    cultural_evolution = Column(JSON, comment="文化演变")
    
    # 现状分析
    current_trends = Column(JSON, comment="当前趋势")
    challenges_faced = Column(JSON, comment="面临挑战")
    future_projections = Column(JSON, comment="未来预测")
    adaptation_strategies = Column(JSON, comment="适应策略")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")
    race_system_id = Column(Integer, ForeignKey("race_systems.id"), comment="种族体系ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.age_distribution:
            self.age_distribution = {}
        if not self.gender_ratio:
            self.gender_ratio = {}
        if not self.primary_territories:
            self.primary_territories = []
        if not self.secondary_regions:
            self.secondary_regions = []
        if not self.migration_routes:
            self.migration_routes = []
        if not self.seasonal_movements:
            self.seasonal_movements = []
        if not self.settlement_patterns:
            self.settlement_patterns = []
        if not self.major_cities:
            self.major_cities = []
        if not self.tribal_areas:
            self.tribal_areas = []
        if not self.sacred_lands:
            self.sacred_lands = []
        if not self.preferred_climate:
            self.preferred_climate = {}
        if not self.terrain_adaptation:
            self.terrain_adaptation = []
        if not self.resource_dependencies:
            self.resource_dependencies = []
        if not self.environmental_threats:
            self.environmental_threats = []
        if not self.social_organization:
            self.social_organization = {}
        if not self.leadership_structure:
            self.leadership_structure = {}
        if not self.cultural_centers:
            self.cultural_centers = []
        if not self.religious_sites:
            self.religious_sites = []
        if not self.allied_races:
            self.allied_races = []
        if not self.hostile_races:
            self.hostile_races = []
        if not self.neutral_races:
            self.neutral_races = []
        if not self.mixed_communities:
            self.mixed_communities = []
        if not self.primary_occupations:
            self.primary_occupations = []
        if not self.trade_specialties:
            self.trade_specialties = []
        if not self.economic_centers:
            self.economic_centers = []
        if not self.resource_control:
            self.resource_control = []
        if not self.historical_migrations:
            self.historical_migrations = []
        if not self.territorial_changes:
            self.territorial_changes = []
        if not self.population_events:
            self.population_events = []
        if not self.cultural_evolution:
            self.cultural_evolution = []
        if not self.current_trends:
            self.current_trends = []
        if not self.challenges_faced:
            self.challenges_faced = []
        if not self.future_projections:
            self.future_projections = []
        if not self.adaptation_strategies:
            self.adaptation_strategies = []

    def add_primary_territory(self, territory_data: Dict[str, Any]):
        """添加主要领土"""
        self.primary_territories.append(territory_data)

    def add_major_city(self, city_data: Dict[str, Any]):
        """添加主要城市"""
        self.major_cities.append(city_data)

    def add_migration_route(self, route_data: Dict[str, Any]):
        """添加迁徙路线"""
        self.migration_routes.append(route_data)

    def set_race_relationship(self, race_name: str, relationship_type: str):
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

    def calculate_territorial_coverage(self) -> float:
        """计算领土覆盖度"""
        coverage = 0.0
        
        # 主要领土权重更高
        coverage += len(self.primary_territories) * 10
        
        # 次要区域
        coverage += len(self.secondary_regions) * 5
        
        # 主要城市
        coverage += len(self.major_cities) * 3
        
        # 部落区域
        coverage += len(self.tribal_areas) * 2
        
        return min(100.0, max(0.0, coverage))

    def calculate_influence_level(self) -> float:
        """计算影响力等级"""
        influence = 50.0  # 基础分数
        
        # 统治程度影响
        dominance_bonus = {
            DominanceLevel.DOMINANT: 30,
            DominanceLevel.MAJORITY: 20,
            DominanceLevel.SIGNIFICANT: 10,
            DominanceLevel.MINORITY: 0,
            DominanceLevel.RARE: -10,
            DominanceLevel.EXTINCT: -50,
            DominanceLevel.UNKNOWN: 0
        }
        influence += dominance_bonus.get(self.dominance_level, 0)
        
        # 人口密度影响
        density_bonus = {
            PopulationDensity.SPARSE: -10,
            PopulationDensity.LOW: -5,
            PopulationDensity.MODERATE: 0,
            PopulationDensity.HIGH: 10,
            PopulationDensity.DENSE: 15,
            PopulationDensity.OVERCROWDED: 5,  # 过度拥挤可能带来问题
            PopulationDensity.UNKNOWN: 0
        }
        influence += density_bonus.get(self.population_density, 0)
        
        # 经济中心数量
        influence += len(self.economic_centers) * 3
        
        # 文化中心数量
        influence += len(self.cultural_centers) * 2
        
        return min(100.0, max(0.0, influence))

    def calculate_stability_index(self) -> float:
        """计算稳定性指数"""
        stability = 50.0  # 基础分数
        
        # 人口增长率影响
        if self.population_growth_rate:
            if 0 <= self.population_growth_rate <= 3:
                stability += 10  # 健康增长
            elif self.population_growth_rate > 5:
                stability -= 5   # 过快增长可能带来问题
            elif self.population_growth_rate < -2:
                stability -= 15  # 人口下降
        
        # 环境威胁影响
        stability -= len(self.environmental_threats) * 3
        
        # 面临挑战影响
        stability -= len(self.challenges_faced) * 2
        
        # 适应策略加成
        stability += len(self.adaptation_strategies) * 4
        
        # 友好种族关系加成
        stability += len(self.allied_races) * 2
        
        # 敌对种族关系影响
        stability -= len(self.hostile_races) * 3
        
        return min(100.0, max(0.0, stability))

    def validate_consistency(self) -> List[str]:
        """验证种族分布一致性"""
        issues = []
        
        # 检查人口数据
        if self.total_population and self.total_population < 0:
            issues.append("总人口不能为负数")
        
        # 检查人口增长率
        if self.population_growth_rate and abs(self.population_growth_rate) > 20:
            issues.append("人口增长率过于极端")
        
        # 检查定居类型与人口密度的一致性
        if self.settlement_type == SettlementType.NOMADIC and self.population_density == PopulationDensity.DENSE:
            issues.append("游牧民族不应有密集的人口分布")
        
        # 检查统治程度与领土的一致性
        if self.dominance_level == DominanceLevel.DOMINANT and len(self.primary_territories) == 0:
            issues.append("统治种族应该有主要领土")
        
        return issues

    def generate_summary(self) -> str:
        """生成种族分布摘要"""
        summary_parts = []
        
        if self.race_name:
            summary_parts.append(self.race_name)
        
        # 统治程度
        dominance_map = {
            DominanceLevel.DOMINANT: "统治",
            DominanceLevel.MAJORITY: "多数",
            DominanceLevel.SIGNIFICANT: "重要",
            DominanceLevel.MINORITY: "少数",
            DominanceLevel.RARE: "稀少",
            DominanceLevel.EXTINCT: "灭绝",
            DominanceLevel.UNKNOWN: "未知"
        }
        summary_parts.append(f"地位: {dominance_map.get(self.dominance_level, '未知')}")
        
        # 人口密度
        density_map = {
            PopulationDensity.SPARSE: "稀疏",
            PopulationDensity.LOW: "低密度",
            PopulationDensity.MODERATE: "中等密度",
            PopulationDensity.HIGH: "高密度",
            PopulationDensity.DENSE: "密集",
            PopulationDensity.OVERCROWDED: "过度拥挤",
            PopulationDensity.UNKNOWN: "未知"
        }
        summary_parts.append(f"密度: {density_map.get(self.population_density, '未知')}")
        
        # 总人口
        if self.total_population:
            summary_parts.append(f"人口: {self.total_population:,}")
        
        # 影响力等级
        influence = self.calculate_influence_level()
        summary_parts.append(f"影响力: {influence:.1f}/100")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["territorial_coverage"] = self.calculate_territorial_coverage()
        result["influence_level"] = self.calculate_influence_level()
        result["stability_index"] = self.calculate_stability_index()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
