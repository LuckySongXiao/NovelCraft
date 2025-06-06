"""
时间线数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin


class EventType(str, Enum):
    """事件类型枚举"""
    HISTORICAL = "historical"       # 历史事件
    PLOT = "plot"                  # 剧情事件
    CHARACTER = "character"        # 角色事件
    WORLD = "world"               # 世界事件
    POLITICAL = "political"       # 政治事件
    NATURAL = "natural"           # 自然事件
    CULTURAL = "cultural"         # 文化事件
    ECONOMIC = "economic"         # 经济事件
    MILITARY = "military"         # 军事事件
    PERSONAL = "personal"         # 个人事件


class EventImportance(str, Enum):
    """事件重要性枚举"""
    CRITICAL = "critical"         # 关键
    HIGH = "high"                # 高
    MEDIUM = "medium"            # 中
    LOW = "low"                  # 低
    TRIVIAL = "trivial"          # 微不足道


class Timeline(ProjectBaseModel, TaggedMixin):
    """时间线模型"""

    __tablename__ = "timelines"

    # 基本信息
    timeline_type = Column(String(50), comment="时间线类型")
    scope = Column(String(100), comment="作用范围")

    # 时间信息
    start_time = Column(String(100), comment="开始时间")
    end_time = Column(String(100), comment="结束时间")
    time_unit = Column(String(20), default="year", comment="时间单位")
    time_format = Column(String(50), comment="时间格式")

    # 事件信息
    events = Column(JSON, comment="事件列表")
    milestones = Column(JSON, comment="里程碑事件")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    related_characters = Column(JSON, comment="相关角色")
    related_factions = Column(JSON, comment="相关势力")
    related_plots = Column(JSON, comment="相关剧情")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.events:
            self.events = []
        if not self.milestones:
            self.milestones = []
        if not self.related_characters:
            self.related_characters = []
        if not self.related_factions:
            self.related_factions = []
        if not self.related_plots:
            self.related_plots = []

    def add_event(self, event_data: Dict[str, Any]):
        """添加事件"""
        # 确保事件有必要字段
        if "time" not in event_data:
            raise ValueError("事件必须包含时间信息")

        if "name" not in event_data:
            raise ValueError("事件必须包含名称")

        # 设置默认值
        event_data.setdefault("type", EventType.HISTORICAL.value)
        event_data.setdefault("importance", EventImportance.MEDIUM.value)
        event_data.setdefault("description", "")
        event_data.setdefault("participants", [])
        event_data.setdefault("consequences", [])
        event_data.setdefault("id", len(self.events) + 1)

        self.events.append(event_data)
        self._sort_events()

    def add_milestone(self, milestone_data: Dict[str, Any]):
        """添加里程碑事件"""
        milestone_data.setdefault("id", len(self.milestones) + 1)
        self.milestones.append(milestone_data)
        self._sort_milestones()

    def _sort_events(self):
        """按时间排序事件"""
        self.events.sort(key=lambda x: self._parse_time(x.get("time", "")))

    def _sort_milestones(self):
        """按时间排序里程碑"""
        self.milestones.sort(key=lambda x: self._parse_time(x.get("time", "")))

    def _parse_time(self, time_str: str) -> float:
        """解析时间字符串为数值（用于排序）"""
        if not time_str:
            return 0

        try:
            # 简单的时间解析，可以根据需要扩展
            if "年" in time_str:
                return float(time_str.replace("年", ""))
            elif "月" in time_str:
                parts = time_str.split("年")
                if len(parts) == 2:
                    year = float(parts[0])
                    month = float(parts[1].replace("月", "")) / 12
                    return year + month
            else:
                # 尝试直接转换为数字
                return float(time_str)
        except (ValueError, AttributeError):
            return 0

    def get_events_by_time_range(self, start_time: str, end_time: str) -> List[Dict[str, Any]]:
        """获取指定时间范围内的事件"""
        start_num = self._parse_time(start_time)
        end_num = self._parse_time(end_time)

        filtered_events = []
        for event in self.events:
            event_time = self._parse_time(event.get("time", ""))
            if start_num <= event_time <= end_num:
                filtered_events.append(event)

        return filtered_events

    def get_events_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """根据类型获取事件"""
        return [event for event in self.events if event.get("type") == event_type]

    def get_events_by_importance(self, importance: str) -> List[Dict[str, Any]]:
        """根据重要性获取事件"""
        return [event for event in self.events if event.get("importance") == importance]

    def get_events_by_character(self, character_id: int) -> List[Dict[str, Any]]:
        """获取与指定角色相关的事件"""
        character_events = []
        for event in self.events:
            participants = event.get("participants", [])
            if character_id in participants:
                character_events.append(event)
        return character_events

    def get_events_by_faction(self, faction_id: int) -> List[Dict[str, Any]]:
        """获取与指定势力相关的事件"""
        faction_events = []
        for event in self.events:
            participants = event.get("participants", [])
            if faction_id in participants:
                faction_events.append(event)
        return faction_events

    def update_event(self, event_id: int, update_data: Dict[str, Any]):
        """更新事件"""
        for i, event in enumerate(self.events):
            if event.get("id") == event_id:
                event.update(update_data)
                self._sort_events()
                return True
        return False

    def remove_event(self, event_id: int):
        """删除事件"""
        self.events = [event for event in self.events if event.get("id") != event_id]

    def get_timeline_summary(self) -> Dict[str, Any]:
        """获取时间线摘要"""
        if not self.events:
            return {
                "total_events": 0,
                "time_span": "无",
                "major_events": 0,
                "event_types": {}
            }

        # 统计事件类型
        event_types = {}
        major_events = 0

        for event in self.events:
            event_type = event.get("type", "unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1

            if event.get("importance") in ["critical", "high"]:
                major_events += 1

        # 计算时间跨度
        if len(self.events) >= 2:
            first_time = self._parse_time(self.events[0].get("time", ""))
            last_time = self._parse_time(self.events[-1].get("time", ""))
            time_span = f"{last_time - first_time}{self.time_unit}"
        else:
            time_span = "单一时间点"

        return {
            "total_events": len(self.events),
            "time_span": time_span,
            "major_events": major_events,
            "event_types": event_types,
            "milestones": len(self.milestones)
        }

    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """检测时间冲突"""
        conflicts = []

        # 检查同一时间的多个重大事件
        time_events = {}
        for event in self.events:
            time_key = event.get("time", "")
            if time_key not in time_events:
                time_events[time_key] = []
            time_events[time_key].append(event)

        for time_key, events in time_events.items():
            if len(events) > 1:
                major_events = [e for e in events if e.get("importance") in ["critical", "high"]]
                if len(major_events) > 1:
                    conflicts.append({
                        "type": "multiple_major_events",
                        "time": time_key,
                        "events": [e.get("name") for e in major_events],
                        "description": f"同一时间发生多个重大事件"
                    })

        # 检查角色参与冲突
        for i, event1 in enumerate(self.events):
            for j, event2 in enumerate(self.events[i+1:], i+1):
                # 检查时间相近的事件中是否有相同角色参与
                time1 = self._parse_time(event1.get("time", ""))
                time2 = self._parse_time(event2.get("time", ""))

                if abs(time1 - time2) < 0.1:  # 时间很接近
                    participants1 = set(event1.get("participants", []))
                    participants2 = set(event2.get("participants", []))
                    overlap = participants1 & participants2

                    if overlap:
                        conflicts.append({
                            "type": "character_conflict",
                            "time": event1.get("time"),
                            "events": [event1.get("name"), event2.get("name")],
                            "characters": list(overlap),
                            "description": "角色在相近时间参与多个事件"
                        })

        return conflicts

    def generate_timeline_visualization_data(self) -> Dict[str, Any]:
        """生成时间线可视化数据"""
        return {
            "timeline_info": {
                "name": self.name,
                "type": self.timeline_type,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "time_unit": self.time_unit
            },
            "events": [
                {
                    "id": event.get("id"),
                    "name": event.get("name"),
                    "time": event.get("time"),
                    "type": event.get("type"),
                    "importance": event.get("importance"),
                    "description": event.get("description", "")[:100] + "..." if len(event.get("description", "")) > 100 else event.get("description", "")
                }
                for event in self.events
            ],
            "milestones": self.milestones,
            "summary": self.get_timeline_summary(),
            "conflicts": self.detect_conflicts()
        }

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.get_timeline_summary()
        result["conflicts"] = self.detect_conflicts()
        result["visualization_data"] = self.generate_timeline_visualization_data()
        result["tags"] = self.get_tags()
        return result
