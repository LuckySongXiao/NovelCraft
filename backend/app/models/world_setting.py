"""
世界设定数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict, Any, List

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class WorldSetting(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """世界设定模型"""

    __tablename__ = "world_settings"

    # 基本信息
    setting_type = Column(String(50), nullable=False, comment="设定类型")
    category = Column(String(100), comment="分类")

    # 地理信息
    geography = Column(JSON, comment="地理信息")
    climate = Column(JSON, comment="气候信息")
    resources = Column(JSON, comment="资源分布")

    # 历史信息
    history = Column(Text, comment="历史背景")
    timeline = Column(JSON, comment="历史时间线")
    important_events = Column(JSON, comment="重要历史事件")

    # 文化信息
    culture = Column(JSON, comment="文化设定")
    language = Column(JSON, comment="语言设定")
    religion = Column(JSON, comment="宗教信仰")
    customs = Column(JSON, comment="风俗习惯")

    # 自然法则
    natural_laws = Column(JSON, comment="自然法则")
    special_rules = Column(JSON, comment="特殊规则")
    magic_system = Column(JSON, comment="魔法体系")

    # 社会结构
    social_structure = Column(JSON, comment="社会结构")
    political_system = Column(JSON, comment="政治体系")
    economic_system = Column(JSON, comment="经济体系")

    # 新增体系字段
    currency_system = Column(JSON, comment="货币体系")
    commerce_system = Column(JSON, comment="商业体系")
    race_categories = Column(JSON, comment="种族类别")
    martial_arts_system = Column(JSON, comment="功法体系")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    parent_id = Column(Integer, ForeignKey("world_settings.id"), comment="父设定ID")

    # project = relationship("Project", back_populates="world_settings")
    children = relationship("WorldSetting", backref="parent", remote_side="WorldSetting.id")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.geography:
            self.geography = {}
        if not self.climate:
            self.climate = {}
        if not self.resources:
            self.resources = {}
        if not self.timeline:
            self.timeline = []
        if not self.important_events:
            self.important_events = []
        if not self.culture:
            self.culture = {}
        if not self.language:
            self.language = {}
        if not self.religion:
            self.religion = {}
        if not self.customs:
            self.customs = {}
        if not self.natural_laws:
            self.natural_laws = {}
        if not self.special_rules:
            self.special_rules = {}
        if not self.magic_system:
            self.magic_system = {}
        if not self.social_structure:
            self.social_structure = {}
        if not self.political_system:
            self.political_system = {}
        if not self.economic_system:
            self.economic_system = {}

        # 初始化新增体系字段
        if not self.currency_system:
            self.currency_system = {}
        if not self.commerce_system:
            self.commerce_system = {}
        if not self.race_categories:
            self.race_categories = {}
        if not self.martial_arts_system:
            self.martial_arts_system = {}

    def add_location(self, location_data: Dict[str, Any]):
        """添加地点"""
        if "locations" not in self.geography:
            self.geography["locations"] = []
        self.geography["locations"].append(location_data)

    def add_historical_event(self, event_data: Dict[str, Any]):
        """添加历史事件"""
        self.important_events.append(event_data)
        # 按时间排序
        self.important_events.sort(key=lambda x: x.get("time", 0))

    def add_cultural_element(self, element_type: str, element_data: Dict[str, Any]):
        """添加文化元素"""
        if element_type not in self.culture:
            self.culture[element_type] = []
        self.culture[element_type].append(element_data)

    def set_natural_law(self, law_name: str, law_data: Dict[str, Any]):
        """设置自然法则"""
        self.natural_laws[law_name] = law_data

    def set_magic_rule(self, rule_name: str, rule_data: Dict[str, Any]):
        """设置魔法规则"""
        if "rules" not in self.magic_system:
            self.magic_system["rules"] = {}
        self.magic_system["rules"][rule_name] = rule_data

    def get_location_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取地点"""
        locations = self.geography.get("locations", [])
        for location in locations:
            if location.get("name") == name:
                return location
        return None

    def get_events_by_period(self, start_time: int, end_time: int) -> List[Dict[str, Any]]:
        """获取指定时期的事件"""
        events = []
        for event in self.important_events:
            event_time = event.get("time", 0)
            if start_time <= event_time <= end_time:
                events.append(event)
        return events

    def validate_consistency(self) -> List[str]:
        """验证设定一致性"""
        issues = []

        # 检查地理与气候的一致性
        if self.geography and self.climate:
            # 这里可以添加具体的一致性检查逻辑
            pass

        # 检查历史事件的时间一致性
        for i, event in enumerate(self.important_events):
            if i > 0:
                prev_event = self.important_events[i-1]
                if event.get("time", 0) < prev_event.get("time", 0):
                    issues.append(f"历史事件时间顺序错误: {event.get('name', '未知事件')}")

        # 检查魔法体系与自然法则的一致性
        if self.magic_system and self.natural_laws:
            # 这里可以添加魔法与自然法则的冲突检查
            pass

        return issues

    def generate_summary(self) -> str:
        """生成设定摘要"""
        summary_parts = []

        if self.description:
            summary_parts.append(self.description)

        # 地理摘要
        if self.geography:
            locations = self.geography.get("locations", [])
            if locations:
                location_names = [loc.get("name", "") for loc in locations[:3]]
                summary_parts.append(f"主要地点: {', '.join(location_names)}")

        # 历史摘要
        if self.important_events:
            event_count = len(self.important_events)
            summary_parts.append(f"重要历史事件: {event_count}个")

        # 文化摘要
        if self.culture:
            culture_types = list(self.culture.keys())[:3]
            if culture_types:
                summary_parts.append(f"文化要素: {', '.join(culture_types)}")

        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result

    # 新增体系管理方法
    def add_currency(self, currency_data: Dict[str, Any]):
        """添加货币"""
        if "currencies" not in self.currency_system:
            self.currency_system["currencies"] = []
        self.currency_system["currencies"].append(currency_data)

    def add_race(self, race_data: Dict[str, Any]):
        """添加种族"""
        if "races" not in self.race_categories:
            self.race_categories["races"] = []
        self.race_categories["races"].append(race_data)

    def add_martial_art(self, martial_art_data: Dict[str, Any]):
        """添加功法"""
        if "techniques" not in self.martial_arts_system:
            self.martial_arts_system["techniques"] = []
        self.martial_arts_system["techniques"].append(martial_art_data)

    def add_commerce_rule(self, rule_name: str, rule_data: Dict[str, Any]):
        """添加商业规则"""
        if "rules" not in self.commerce_system:
            self.commerce_system["rules"] = {}
        self.commerce_system["rules"][rule_name] = rule_data

    def get_currency_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取货币"""
        currencies = self.currency_system.get("currencies", [])
        for currency in currencies:
            if currency.get("name") == name:
                return currency
        return None

    def get_race_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取种族"""
        races = self.race_categories.get("races", [])
        for race in races:
            if race.get("name") == name:
                return race
        return None

    def get_martial_art_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取功法"""
        techniques = self.martial_arts_system.get("techniques", [])
        for technique in techniques:
            if technique.get("name") == name:
                return technique
        return None
