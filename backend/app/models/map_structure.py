"""
地图结构数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class MapType(str, Enum):
    """地图类型枚举"""
    WORLD = "world"                 # 世界地图
    CONTINENT = "continent"         # 大陆
    REGION = "region"               # 区域
    PROVINCE = "province"           # 省份
    CITY = "city"                   # 城市
    TOWN = "town"                   # 城镇
    VILLAGE = "village"             # 村庄
    DUNGEON = "dungeon"             # 地下城
    BUILDING = "building"           # 建筑
    ROOM = "room"                   # 房间
    OTHER = "other"                 # 其他


class TerrainType(str, Enum):
    """地形类型枚举"""
    PLAINS = "plains"               # 平原
    FOREST = "forest"               # 森林
    MOUNTAIN = "mountain"           # 山脉
    DESERT = "desert"               # 沙漠
    SWAMP = "swamp"                 # 沼泽
    OCEAN = "ocean"                 # 海洋
    RIVER = "river"                 # 河流
    LAKE = "lake"                   # 湖泊
    TUNDRA = "tundra"               # 苔原
    VOLCANO = "volcano"             # 火山
    CANYON = "canyon"               # 峡谷
    CAVE = "cave"                   # 洞穴
    SKY = "sky"                     # 天空
    UNDERGROUND = "underground"     # 地下
    OTHER = "other"                 # 其他


class ClimateType(str, Enum):
    """气候类型枚举"""
    TROPICAL = "tropical"           # 热带
    TEMPERATE = "temperate"         # 温带
    ARCTIC = "arctic"               # 寒带
    ARID = "arid"                   # 干旱
    HUMID = "humid"                 # 湿润
    CONTINENTAL = "continental"     # 大陆性
    OCEANIC = "oceanic"             # 海洋性
    MONSOON = "monsoon"             # 季风
    MAGICAL = "magical"             # 魔法气候
    OTHER = "other"                 # 其他


class MapStructure(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """地图结构模型"""

    __tablename__ = "map_structures"

    # 基本信息
    map_type = Column(SQLEnum(MapType), default=MapType.REGION, comment="地图类型")
    terrain_type = Column(SQLEnum(TerrainType), default=TerrainType.PLAINS, comment="主要地形")
    climate_type = Column(SQLEnum(ClimateType), default=ClimateType.TEMPERATE, comment="气候类型")

    # 地理信息
    coordinates = Column(JSON, comment="坐标信息")
    area_size = Column(Float, comment="面积大小")
    elevation = Column(Float, comment="海拔高度")
    boundaries = Column(JSON, comment="边界信息")

    # 层级结构
    parent_map_id = Column(Integer, ForeignKey("map_structures.id"), comment="父级地图ID")
    level = Column(Integer, default=0, comment="层级深度")
    map_hierarchy = Column(JSON, comment="地图层级")

    # 地形特征
    terrain_features = Column(JSON, comment="地形特征")
    natural_landmarks = Column(JSON, comment="自然地标")
    water_bodies = Column(JSON, comment="水体")
    vegetation = Column(JSON, comment="植被")

    # 气候环境
    weather_patterns = Column(JSON, comment="天气模式")
    seasonal_changes = Column(JSON, comment="季节变化")
    natural_disasters = Column(JSON, comment="自然灾害")
    environmental_hazards = Column(JSON, comment="环境危险")

    # 人文地理
    settlements = Column(JSON, comment="定居点")
    transportation = Column(JSON, comment="交通网络")
    trade_routes = Column(JSON, comment="贸易路线")
    political_control = Column(JSON, comment="政治控制")

    # 资源分布
    natural_resources = Column(JSON, comment="自然资源")
    magical_resources = Column(JSON, comment="魔法资源")
    rare_materials = Column(JSON, comment="稀有材料")
    resource_nodes = Column(JSON, comment="资源节点")

    # 生物分布
    native_species = Column(JSON, comment="本土物种")
    monster_habitats = Column(JSON, comment="怪物栖息地")
    migration_routes = Column(JSON, comment="迁徙路线")
    ecosystem_balance = Column(JSON, comment="生态平衡")

    # 特殊区域
    magical_zones = Column(JSON, comment="魔法区域")
    forbidden_areas = Column(JSON, comment="禁区")
    sacred_sites = Column(JSON, comment="圣地")
    ruins_and_artifacts = Column(JSON, comment="遗迹文物")

    # 探索信息
    exploration_difficulty = Column(Integer, default=1, comment="探索难度")
    hidden_secrets = Column(JSON, comment="隐藏秘密")
    discovery_rewards = Column(JSON, comment="发现奖励")
    access_requirements = Column(JSON, comment="进入条件")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    # 自引用关系
    children = relationship("MapStructure", backref="parent", remote_side="MapStructure.id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.coordinates:
            self.coordinates = {}
        if not self.boundaries:
            self.boundaries = {}
        if not self.map_hierarchy:
            self.map_hierarchy = []
        if not self.terrain_features:
            self.terrain_features = []
        if not self.natural_landmarks:
            self.natural_landmarks = []
        if not self.water_bodies:
            self.water_bodies = []
        if not self.vegetation:
            self.vegetation = []
        if not self.weather_patterns:
            self.weather_patterns = []
        if not self.seasonal_changes:
            self.seasonal_changes = []
        if not self.natural_disasters:
            self.natural_disasters = []
        if not self.environmental_hazards:
            self.environmental_hazards = []
        if not self.settlements:
            self.settlements = []
        if not self.transportation:
            self.transportation = []
        if not self.trade_routes:
            self.trade_routes = []
        if not self.political_control:
            self.political_control = {}
        if not self.natural_resources:
            self.natural_resources = []
        if not self.magical_resources:
            self.magical_resources = []
        if not self.rare_materials:
            self.rare_materials = []
        if not self.resource_nodes:
            self.resource_nodes = []
        if not self.native_species:
            self.native_species = []
        if not self.monster_habitats:
            self.monster_habitats = []
        if not self.migration_routes:
            self.migration_routes = []
        if not self.ecosystem_balance:
            self.ecosystem_balance = {}
        if not self.magical_zones:
            self.magical_zones = []
        if not self.forbidden_areas:
            self.forbidden_areas = []
        if not self.sacred_sites:
            self.sacred_sites = []
        if not self.ruins_and_artifacts:
            self.ruins_and_artifacts = []
        if not self.hidden_secrets:
            self.hidden_secrets = []
        if not self.discovery_rewards:
            self.discovery_rewards = []
        if not self.access_requirements:
            self.access_requirements = []

    def add_terrain_feature(self, feature_data: Dict[str, Any]):
        """添加地形特征"""
        self.terrain_features.append(feature_data)

    def add_natural_landmark(self, landmark_data: Dict[str, Any]):
        """添加自然地标"""
        self.natural_landmarks.append(landmark_data)

    def add_settlement(self, settlement_data: Dict[str, Any]):
        """添加定居点"""
        self.settlements.append(settlement_data)

    def add_resource_node(self, resource_data: Dict[str, Any]):
        """添加资源节点"""
        self.resource_nodes.append(resource_data)

    def add_magical_zone(self, zone_data: Dict[str, Any]):
        """添加魔法区域"""
        self.magical_zones.append(zone_data)

    def add_child_map(self, child_map_data: Dict[str, Any]):
        """添加子地图"""
        child_map_data["parent_map_id"] = self.id
        child_map_data["level"] = self.level + 1
        return child_map_data

    def calculate_resource_density(self) -> float:
        """计算资源密度"""
        if not self.area_size or self.area_size == 0:
            return 0.0

        total_resources = (
            len(self.natural_resources) +
            len(self.magical_resources) +
            len(self.rare_materials) +
            len(self.resource_nodes)
        )

        return total_resources / self.area_size

    def calculate_danger_level(self) -> float:
        """计算危险等级"""
        danger = 0.0

        # 基础探索难度
        exploration_difficulty = self.exploration_difficulty or 1
        danger += exploration_difficulty * 10

        # 环境危险
        danger += len(self.environmental_hazards) * 5

        # 自然灾害
        danger += len(self.natural_disasters) * 3

        # 怪物栖息地
        danger += len(self.monster_habitats) * 4

        # 禁区
        danger += len(self.forbidden_areas) * 8

        return min(100.0, max(0.0, danger))

    def calculate_strategic_value(self) -> float:
        """计算战略价值"""
        value = 50.0  # 基础分数

        # 资源价值
        value += len(self.natural_resources) * 3
        value += len(self.magical_resources) * 5
        value += len(self.rare_materials) * 4

        # 交通价值
        value += len(self.transportation) * 2
        value += len(self.trade_routes) * 3

        # 定居点价值
        value += len(self.settlements) * 2

        # 特殊区域价值
        value += len(self.sacred_sites) * 4
        value += len(self.ruins_and_artifacts) * 3

        return min(100.0, max(0.0, value))

    def validate_consistency(self) -> List[str]:
        """验证地图结构一致性"""
        issues = []

        # 检查层级关系
        if self.parent_map_id and self.level == 0:
            issues.append("有父级地图但层级为0")

        # 检查地形与气候的一致性
        if self.terrain_type == TerrainType.DESERT and self.climate_type == ClimateType.HUMID:
            issues.append("沙漠地形与湿润气候不一致")

        # 检查面积大小的合理性
        if self.area_size and self.area_size < 0:
            issues.append("面积大小不能为负数")

        return issues

    def generate_summary(self) -> str:
        """生成地图摘要"""
        summary_parts = []

        if self.description:
            summary_parts.append(self.description)

        # 地图类型
        type_map = {
            MapType.WORLD: "世界地图",
            MapType.CONTINENT: "大陆",
            MapType.REGION: "区域",
            MapType.PROVINCE: "省份",
            MapType.CITY: "城市",
            MapType.TOWN: "城镇",
            MapType.VILLAGE: "村庄",
            MapType.DUNGEON: "地下城",
            MapType.BUILDING: "建筑",
            MapType.ROOM: "房间",
            MapType.OTHER: "其他"
        }
        summary_parts.append(f"类型: {type_map.get(self.map_type, '未知')}")

        # 主要地形
        terrain_map = {
            TerrainType.PLAINS: "平原",
            TerrainType.FOREST: "森林",
            TerrainType.MOUNTAIN: "山脉",
            TerrainType.DESERT: "沙漠",
            TerrainType.SWAMP: "沼泽",
            TerrainType.OCEAN: "海洋",
            TerrainType.RIVER: "河流",
            TerrainType.LAKE: "湖泊",
            TerrainType.TUNDRA: "苔原",
            TerrainType.VOLCANO: "火山",
            TerrainType.CANYON: "峡谷",
            TerrainType.CAVE: "洞穴",
            TerrainType.SKY: "天空",
            TerrainType.UNDERGROUND: "地下",
            TerrainType.OTHER: "其他"
        }
        summary_parts.append(f"地形: {terrain_map.get(self.terrain_type, '未知')}")

        # 面积
        if self.area_size:
            summary_parts.append(f"面积: {self.area_size:.1f}")

        # 危险等级
        danger = self.calculate_danger_level()
        summary_parts.append(f"危险等级: {danger:.1f}/100")

        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["resource_density"] = self.calculate_resource_density()
        result["danger_level"] = self.calculate_danger_level()
        result["strategic_value"] = self.calculate_strategic_value()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
