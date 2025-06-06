"""
资源分布数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class ResourceType(str, Enum):
    """资源类型枚举"""
    MINERAL = "mineral"             # 矿物
    PLANT = "plant"                 # 植物
    ANIMAL = "animal"               # 动物
    MAGICAL = "magical"             # 魔法
    ENERGY = "energy"               # 能量
    WATER = "water"                 # 水源
    FOOD = "food"                   # 食物
    MATERIAL = "material"           # 材料
    ARTIFACT = "artifact"           # 文物
    KNOWLEDGE = "knowledge"         # 知识
    SPIRITUAL = "spiritual"         # 精神
    OTHER = "other"                 # 其他


class ResourceRarity(str, Enum):
    """资源稀有度枚举"""
    ABUNDANT = "abundant"           # 丰富
    COMMON = "common"               # 常见
    UNCOMMON = "uncommon"           # 不常见
    RARE = "rare"                   # 稀有
    VERY_RARE = "very_rare"         # 极稀有
    LEGENDARY = "legendary"         # 传说
    UNIQUE = "unique"               # 唯一
    UNKNOWN = "unknown"             # 未知


class ResourceDistribution(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """资源分布模型"""

    __tablename__ = "resource_distributions"

    # 基本信息
    resource_type = Column(SQLEnum(ResourceType), default=ResourceType.MINERAL, comment="资源类型")
    resource_rarity = Column(SQLEnum(ResourceRarity), default=ResourceRarity.COMMON, comment="资源稀有度")
    resource_name = Column(String(200), comment="资源名称")
    
    # 分布信息
    distribution_pattern = Column(String(100), comment="分布模式")
    concentration_areas = Column(JSON, comment="集中区域")
    scattered_locations = Column(JSON, comment="散布地点")
    geographic_regions = Column(JSON, comment="地理区域")
    
    # 数量信息
    total_reserves = Column(Float, comment="总储量")
    annual_yield = Column(Float, comment="年产量")
    regeneration_rate = Column(Float, comment="再生率")
    
    # 开采信息
    extraction_methods = Column(JSON, comment="开采方法")
    required_tools = Column(JSON, comment="所需工具")
    extraction_risks = Column(JSON, comment="开采风险")
    
    # 经济价值
    market_value = Column(Float, comment="市场价值")
    trade_routes = Column(JSON, comment="贸易路线")
    controlling_factions = Column(JSON, comment="控制势力")
    
    # 环境影响
    environmental_impact = Column(JSON, comment="环境影响")
    conservation_efforts = Column(JSON, comment="保护措施")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.concentration_areas:
            self.concentration_areas = []
        if not self.scattered_locations:
            self.scattered_locations = []
        if not self.geographic_regions:
            self.geographic_regions = []
        if not self.extraction_methods:
            self.extraction_methods = []
        if not self.required_tools:
            self.required_tools = []
        if not self.extraction_risks:
            self.extraction_risks = []
        if not self.trade_routes:
            self.trade_routes = []
        if not self.controlling_factions:
            self.controlling_factions = []
        if not self.environmental_impact:
            self.environmental_impact = {}
        if not self.conservation_efforts:
            self.conservation_efforts = []

    def add_concentration_area(self, area_data: Dict[str, Any]):
        """添加集中区域"""
        self.concentration_areas.append(area_data)

    def calculate_economic_value(self) -> float:
        """计算经济价值"""
        value = self.market_value or 0.0
        
        # 稀有度加成
        rarity_multiplier = {
            ResourceRarity.ABUNDANT: 0.5,
            ResourceRarity.COMMON: 1.0,
            ResourceRarity.UNCOMMON: 1.5,
            ResourceRarity.RARE: 2.5,
            ResourceRarity.VERY_RARE: 4.0,
            ResourceRarity.LEGENDARY: 6.0,
            ResourceRarity.UNIQUE: 10.0,
            ResourceRarity.UNKNOWN: 1.0
        }
        value *= rarity_multiplier.get(self.resource_rarity, 1.0)
        
        return value

    def generate_summary(self) -> str:
        """生成资源分布摘要"""
        summary_parts = []
        
        if self.resource_name:
            summary_parts.append(self.resource_name)
        
        # 资源类型
        type_map = {
            ResourceType.MINERAL: "矿物",
            ResourceType.PLANT: "植物",
            ResourceType.ANIMAL: "动物",
            ResourceType.MAGICAL: "魔法",
            ResourceType.ENERGY: "能量",
            ResourceType.WATER: "水源",
            ResourceType.FOOD: "食物",
            ResourceType.MATERIAL: "材料",
            ResourceType.ARTIFACT: "文物",
            ResourceType.KNOWLEDGE: "知识",
            ResourceType.SPIRITUAL: "精神",
            ResourceType.OTHER: "其他"
        }
        summary_parts.append(f"类型: {type_map.get(self.resource_type, '未知')}")
        
        # 稀有度
        rarity_map = {
            ResourceRarity.ABUNDANT: "丰富",
            ResourceRarity.COMMON: "常见",
            ResourceRarity.UNCOMMON: "不常见",
            ResourceRarity.RARE: "稀有",
            ResourceRarity.VERY_RARE: "极稀有",
            ResourceRarity.LEGENDARY: "传说",
            ResourceRarity.UNIQUE: "唯一",
            ResourceRarity.UNKNOWN: "未知"
        }
        summary_parts.append(f"稀有度: {rarity_map.get(self.resource_rarity, '未知')}")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["economic_value"] = self.calculate_economic_value()
        result["tags"] = self.get_tags()
        return result
