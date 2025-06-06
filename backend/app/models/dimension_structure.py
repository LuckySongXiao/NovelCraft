"""
维度结构数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class DimensionType(str, Enum):
    """维度类型枚举"""
    MATERIAL = "material"           # 物质位面
    ELEMENTAL = "elemental"         # 元素位面
    SPIRITUAL = "spiritual"         # 精神位面
    SHADOW = "shadow"               # 阴影位面
    ASTRAL = "astral"               # 星界
    ETHEREAL = "ethereal"           # 以太位面
    DREAM = "dream"                 # 梦境位面
    VOID = "void"                   # 虚空
    HEAVEN = "heaven"               # 天界
    HELL = "hell"                   # 地狱
    POCKET = "pocket"               # 口袋维度
    MIRROR = "mirror"               # 镜像维度
    TIME = "time"                   # 时间维度
    PARALLEL = "parallel"           # 平行维度
    OTHER = "other"                 # 其他


class DimensionStability(str, Enum):
    """维度稳定性枚举"""
    STABLE = "stable"               # 稳定
    UNSTABLE = "unstable"           # 不稳定
    COLLAPSING = "collapsing"       # 崩塌中
    FORMING = "forming"             # 形成中
    CHAOTIC = "chaotic"             # 混沌
    DORMANT = "dormant"             # 休眠
    ACTIVE = "active"               # 活跃
    UNKNOWN = "unknown"             # 未知


class AccessLevel(str, Enum):
    """访问等级枚举"""
    PUBLIC = "public"               # 公开
    RESTRICTED = "restricted"       # 限制
    FORBIDDEN = "forbidden"         # 禁止
    HIDDEN = "hidden"               # 隐藏
    LEGENDARY = "legendary"         # 传说
    DIVINE = "divine"               # 神级
    UNKNOWN = "unknown"             # 未知


class DimensionStructure(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """维度结构模型"""

    __tablename__ = "dimension_structures"

    # 基本信息
    dimension_type = Column(SQLEnum(DimensionType), default=DimensionType.MATERIAL, comment="维度类型")
    stability = Column(SQLEnum(DimensionStability), default=DimensionStability.STABLE, comment="稳定性")
    access_level = Column(SQLEnum(AccessLevel), default=AccessLevel.PUBLIC, comment="访问等级")

    # 维度属性
    dimensional_laws = Column(JSON, comment="维度法则")
    physical_properties = Column(JSON, comment="物理属性")
    magical_properties = Column(JSON, comment="魔法属性")
    time_flow = Column(Float, default=1.0, comment="时间流速")

    # 空间结构
    spatial_dimensions = Column(Integer, default=3, comment="空间维数")
    size_scale = Column(String(50), comment="尺度大小")
    geometry_type = Column(String(50), comment="几何类型")
    boundaries = Column(JSON, comment="边界信息")

    # 环境特征
    atmosphere = Column(JSON, comment="大气环境")
    gravity = Column(Float, default=1.0, comment="重力系数")
    temperature = Column(JSON, comment="温度范围")
    energy_levels = Column(JSON, comment="能量水平")

    # 居民与生物
    native_beings = Column(JSON, comment="原生生物")
    visitor_species = Column(JSON, comment="访客种族")
    population_density = Column(Float, default=0.0, comment="人口密度")
    civilization_level = Column(Integer, default=0, comment="文明等级")

    # 资源与材料
    unique_resources = Column(JSON, comment="独特资源")
    dimensional_materials = Column(JSON, comment="维度材料")
    energy_sources = Column(JSON, comment="能量来源")
    rare_phenomena = Column(JSON, comment="稀有现象")

    # 连接与传送
    portals = Column(JSON, comment="传送门")
    rift_points = Column(JSON, comment="裂隙点")
    dimensional_anchors = Column(JSON, comment="维度锚点")
    travel_methods = Column(JSON, comment="旅行方式")

    # 危险与威胁
    environmental_hazards = Column(JSON, comment="环境危险")
    hostile_entities = Column(JSON, comment="敌对实体")
    dimensional_storms = Column(JSON, comment="维度风暴")
    corruption_zones = Column(JSON, comment="腐化区域")

    # 历史与传说
    creation_myth = Column(Text, comment="创世神话")
    historical_events = Column(JSON, comment="历史事件")
    famous_locations = Column(JSON, comment="著名地点")
    legendary_artifacts = Column(JSON, comment="传奇文物")

    # 探索信息
    exploration_difficulty = Column(Integer, default=1, comment="探索难度")
    discovery_rewards = Column(JSON, comment="发现奖励")
    hidden_secrets = Column(JSON, comment="隐藏秘密")
    research_value = Column(Float, default=0.0, comment="研究价值")

    # 维度关系
    parent_dimension_id = Column(Integer, ForeignKey("dimension_structures.id"), comment="父维度ID")
    connected_dimensions = Column(JSON, comment="连接维度")
    dimensional_hierarchy = Column(JSON, comment="维度层级")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    # 自引用关系
    children = relationship("DimensionStructure", backref="parent", remote_side="DimensionStructure.id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.dimensional_laws:
            self.dimensional_laws = {}
        if not self.physical_properties:
            self.physical_properties = {}
        if not self.magical_properties:
            self.magical_properties = {}
        if not self.boundaries:
            self.boundaries = {}
        if not self.atmosphere:
            self.atmosphere = {}
        if not self.temperature:
            self.temperature = {}
        if not self.energy_levels:
            self.energy_levels = {}
        if not self.native_beings:
            self.native_beings = []
        if not self.visitor_species:
            self.visitor_species = []
        if not self.unique_resources:
            self.unique_resources = []
        if not self.dimensional_materials:
            self.dimensional_materials = []
        if not self.energy_sources:
            self.energy_sources = []
        if not self.rare_phenomena:
            self.rare_phenomena = []
        if not self.portals:
            self.portals = []
        if not self.rift_points:
            self.rift_points = []
        if not self.dimensional_anchors:
            self.dimensional_anchors = []
        if not self.travel_methods:
            self.travel_methods = []
        if not self.environmental_hazards:
            self.environmental_hazards = []
        if not self.hostile_entities:
            self.hostile_entities = []
        if not self.dimensional_storms:
            self.dimensional_storms = []
        if not self.corruption_zones:
            self.corruption_zones = []
        if not self.historical_events:
            self.historical_events = []
        if not self.famous_locations:
            self.famous_locations = []
        if not self.legendary_artifacts:
            self.legendary_artifacts = []
        if not self.discovery_rewards:
            self.discovery_rewards = []
        if not self.hidden_secrets:
            self.hidden_secrets = []
        if not self.connected_dimensions:
            self.connected_dimensions = []
        if not self.dimensional_hierarchy:
            self.dimensional_hierarchy = []

    def add_native_being(self, being_data: Dict[str, Any]):
        """添加原生生物"""
        self.native_beings.append(being_data)

    def add_portal(self, portal_data: Dict[str, Any]):
        """添加传送门"""
        self.portals.append(portal_data)

    def add_unique_resource(self, resource_data: Dict[str, Any]):
        """添加独特资源"""
        self.unique_resources.append(resource_data)

    def add_environmental_hazard(self, hazard_data: Dict[str, Any]):
        """添加环境危险"""
        self.environmental_hazards.append(hazard_data)

    def add_connected_dimension(self, dimension_id: int, connection_type: str):
        """添加连接维度"""
        connection = {
            "dimension_id": dimension_id,
            "connection_type": connection_type,
            "stability": "stable"
        }
        self.connected_dimensions.append(connection)

    def calculate_danger_level(self) -> float:
        """计算危险等级"""
        danger = 0.0

        # 基础探索难度
        exploration_difficulty = self.exploration_difficulty or 1
        danger += exploration_difficulty * 10

        # 稳定性影响
        stability_danger = {
            DimensionStability.STABLE: 0,
            DimensionStability.UNSTABLE: 20,
            DimensionStability.COLLAPSING: 40,
            DimensionStability.FORMING: 15,
            DimensionStability.CHAOTIC: 35,
            DimensionStability.DORMANT: 5,
            DimensionStability.ACTIVE: 10,
            DimensionStability.UNKNOWN: 25
        }
        danger += stability_danger.get(self.stability, 0)

        # 环境危险
        danger += len(self.environmental_hazards) * 3

        # 敌对实体
        danger += len(self.hostile_entities) * 4

        # 维度风暴
        danger += len(self.dimensional_storms) * 5

        # 腐化区域
        danger += len(self.corruption_zones) * 6

        return min(100.0, max(0.0, danger))

    def calculate_research_potential(self) -> float:
        """计算研究潜力"""
        potential = self.research_value or 0.0

        # 独特资源加成
        potential += len(self.unique_resources) * 5

        # 维度材料加成
        potential += len(self.dimensional_materials) * 4

        # 稀有现象加成
        potential += len(self.rare_phenomena) * 6

        # 传奇文物加成
        potential += len(self.legendary_artifacts) * 8

        # 维度类型加成
        type_bonus = {
            DimensionType.MATERIAL: 0,
            DimensionType.ELEMENTAL: 10,
            DimensionType.SPIRITUAL: 15,
            DimensionType.SHADOW: 12,
            DimensionType.ASTRAL: 18,
            DimensionType.ETHEREAL: 16,
            DimensionType.DREAM: 20,
            DimensionType.VOID: 25,
            DimensionType.HEAVEN: 22,
            DimensionType.HELL: 20,
            DimensionType.POCKET: 8,
            DimensionType.MIRROR: 14,
            DimensionType.TIME: 30,
            DimensionType.PARALLEL: 25,
            DimensionType.OTHER: 10
        }
        potential += type_bonus.get(self.dimension_type, 0)

        return min(100.0, max(0.0, potential))

    def calculate_accessibility(self) -> float:
        """计算可达性"""
        accessibility = 50.0  # 基础分数

        # 访问等级影响
        access_modifier = {
            AccessLevel.PUBLIC: 30,
            AccessLevel.RESTRICTED: 10,
            AccessLevel.FORBIDDEN: -20,
            AccessLevel.HIDDEN: -10,
            AccessLevel.LEGENDARY: -15,
            AccessLevel.DIVINE: -25,
            AccessLevel.UNKNOWN: 0
        }
        accessibility += access_modifier.get(self.access_level, 0)

        # 传送门数量
        accessibility += len(self.portals) * 5

        # 旅行方式
        accessibility += len(self.travel_methods) * 3

        # 稳定性影响
        if self.stability == DimensionStability.STABLE:
            accessibility += 15
        elif self.stability == DimensionStability.UNSTABLE:
            accessibility -= 10

        return min(100.0, max(0.0, accessibility))

    def validate_consistency(self) -> List[str]:
        """验证维度结构一致性"""
        issues = []

        # 检查时间流速
        if self.time_flow <= 0:
            issues.append("时间流速必须大于0")

        # 检查空间维数
        if self.spatial_dimensions < 1:
            issues.append("空间维数必须至少为1")

        # 检查重力系数
        if self.gravity < 0:
            issues.append("重力系数不能为负数")

        # 检查维度类型与属性的一致性
        if self.dimension_type == DimensionType.VOID and self.population_density > 0:
            issues.append("虚空维度不应有人口")

        return issues

    def generate_summary(self) -> str:
        """生成维度摘要"""
        summary_parts = []

        if self.description:
            summary_parts.append(self.description)

        # 维度类型
        type_map = {
            DimensionType.MATERIAL: "物质位面",
            DimensionType.ELEMENTAL: "元素位面",
            DimensionType.SPIRITUAL: "精神位面",
            DimensionType.SHADOW: "阴影位面",
            DimensionType.ASTRAL: "星界",
            DimensionType.ETHEREAL: "以太位面",
            DimensionType.DREAM: "梦境位面",
            DimensionType.VOID: "虚空",
            DimensionType.HEAVEN: "天界",
            DimensionType.HELL: "地狱",
            DimensionType.POCKET: "口袋维度",
            DimensionType.MIRROR: "镜像维度",
            DimensionType.TIME: "时间维度",
            DimensionType.PARALLEL: "平行维度",
            DimensionType.OTHER: "其他"
        }
        summary_parts.append(f"类型: {type_map.get(self.dimension_type, '未知')}")

        # 稳定性
        stability_map = {
            DimensionStability.STABLE: "稳定",
            DimensionStability.UNSTABLE: "不稳定",
            DimensionStability.COLLAPSING: "崩塌中",
            DimensionStability.FORMING: "形成中",
            DimensionStability.CHAOTIC: "混沌",
            DimensionStability.DORMANT: "休眠",
            DimensionStability.ACTIVE: "活跃",
            DimensionStability.UNKNOWN: "未知"
        }
        summary_parts.append(f"稳定性: {stability_map.get(self.stability, '未知')}")

        # 时间流速
        if self.time_flow != 1.0:
            summary_parts.append(f"时间流速: {self.time_flow}x")

        # 危险等级
        danger = self.calculate_danger_level()
        summary_parts.append(f"危险等级: {danger:.1f}/100")

        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["danger_level"] = self.calculate_danger_level()
        result["research_potential"] = self.calculate_research_potential()
        result["accessibility"] = self.calculate_accessibility()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
