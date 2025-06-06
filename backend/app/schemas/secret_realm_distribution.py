"""
秘境分布相关的 Pydantic 模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..models.secret_realm_distribution import RealmType, DangerLevel, AccessType


class SecretRealmDistributionBase(BaseModel):
    """秘境分布基础模式"""
    name: str = Field(..., description="秘境名称")
    description: Optional[str] = Field(None, description="秘境描述")
    realm_type: RealmType = Field(RealmType.DUNGEON, description="秘境类型")
    danger_level: DangerLevel = Field(DangerLevel.MODERATE, description="危险等级")
    access_type: AccessType = Field(AccessType.OPEN, description="进入方式")
    
    # 位置信息
    location_coordinates: Optional[Dict[str, Any]] = Field(None, description="位置坐标")
    geographic_region: Optional[str] = Field(None, description="地理区域")
    terrain_type: Optional[str] = Field(None, description="地形类型")
    hidden_level: int = Field(1, description="隐藏程度")
    
    # 结构信息
    size_scale: Optional[str] = Field(None, description="规模大小")
    internal_structure: Optional[Dict[str, Any]] = Field(None, description="内部结构")
    floor_levels: int = Field(1, description="层数")
    room_count: Optional[int] = Field(None, description="房间数量")
    
    # 进入条件
    entry_requirements: Optional[List[Dict[str, Any]]] = Field(None, description="进入条件")
    access_restrictions: Optional[List[Dict[str, Any]]] = Field(None, description="访问限制")
    opening_schedule: Optional[Dict[str, Any]] = Field(None, description="开放时间")
    activation_methods: Optional[List[Dict[str, Any]]] = Field(None, description="激活方法")
    
    # 环境特征
    environmental_conditions: Optional[Dict[str, Any]] = Field(None, description="环境条件")
    magical_properties: Optional[List[Dict[str, Any]]] = Field(None, description="魔法属性")
    atmospheric_effects: Optional[List[Dict[str, Any]]] = Field(None, description="大气效应")
    special_phenomena: Optional[List[Dict[str, Any]]] = Field(None, description="特殊现象")
    
    # 居住生物
    guardian_creatures: Optional[List[Dict[str, Any]]] = Field(None, description="守护生物")
    hostile_entities: Optional[List[Dict[str, Any]]] = Field(None, description="敌对实体")
    neutral_inhabitants: Optional[List[Dict[str, Any]]] = Field(None, description="中性居民")
    boss_encounters: Optional[List[Dict[str, Any]]] = Field(None, description="首领遭遇")
    
    # 奖励资源
    treasure_types: Optional[List[Dict[str, Any]]] = Field(None, description="宝藏类型")
    rare_materials: Optional[List[Dict[str, Any]]] = Field(None, description="稀有材料")
    magical_artifacts: Optional[List[Dict[str, Any]]] = Field(None, description="魔法文物")
    knowledge_rewards: Optional[List[Dict[str, Any]]] = Field(None, description="知识奖励")
    
    # 陷阱机关
    trap_systems: Optional[List[Dict[str, Any]]] = Field(None, description="陷阱系统")
    puzzle_mechanisms: Optional[List[Dict[str, Any]]] = Field(None, description="谜题机关")
    security_measures: Optional[List[Dict[str, Any]]] = Field(None, description="安全措施")
    defensive_systems: Optional[List[Dict[str, Any]]] = Field(None, description="防御系统")


class SecretRealmDistributionCreate(SecretRealmDistributionBase):
    """创建秘境分布模式"""
    project_id: int = Field(..., description="项目ID")
    
    # 探索信息
    discovery_date: Optional[str] = Field(None, description="发现日期")
    discovery_method: Optional[str] = Field(None, description="发现方式")
    discoverer_info: Optional[Dict[str, Any]] = Field(None, description="发现者信息")
    exploration_status: str = Field("未探索", description="探索状态")
    completion_rate: float = Field(0.0, description="完成度")
    
    # 历史记录
    historical_events: Optional[List[Dict[str, Any]]] = Field(None, description="历史事件")
    previous_explorers: Optional[List[Dict[str, Any]]] = Field(None, description="之前的探索者")
    discovery_rewards: Optional[List[Dict[str, Any]]] = Field(None, description="发现奖励")
    exploration_records: Optional[List[Dict[str, Any]]] = Field(None, description="探索记录")
    
    # 影响评估
    environmental_impact: Optional[Dict[str, Any]] = Field(None, description="环境影响")
    local_legends: Optional[List[Dict[str, Any]]] = Field(None, description="当地传说")
    
    # 标签和版本
    tags: Optional[List[str]] = Field(None, description="标签")
    version: str = Field("1.0", description="版本")
    notes: Optional[str] = Field(None, description="备注")


class SecretRealmDistributionUpdate(BaseModel):
    """更新秘境分布模式"""
    name: Optional[str] = Field(None, description="秘境名称")
    description: Optional[str] = Field(None, description="秘境描述")
    realm_type: Optional[RealmType] = Field(None, description="秘境类型")
    danger_level: Optional[DangerLevel] = Field(None, description="危险等级")
    access_type: Optional[AccessType] = Field(None, description="进入方式")
    
    # 位置信息
    location_coordinates: Optional[Dict[str, Any]] = Field(None, description="位置坐标")
    geographic_region: Optional[str] = Field(None, description="地理区域")
    terrain_type: Optional[str] = Field(None, description="地形类型")
    hidden_level: Optional[int] = Field(None, description="隐藏程度")
    
    # 结构信息
    size_scale: Optional[str] = Field(None, description="规模大小")
    internal_structure: Optional[Dict[str, Any]] = Field(None, description="内部结构")
    floor_levels: Optional[int] = Field(None, description="层数")
    room_count: Optional[int] = Field(None, description="房间数量")
    
    # 探索信息
    exploration_status: Optional[str] = Field(None, description="探索状态")
    completion_rate: Optional[float] = Field(None, description="完成度")
    
    # 标签和版本
    tags: Optional[List[str]] = Field(None, description="标签")
    notes: Optional[str] = Field(None, description="备注")


class SecretRealmDistributionResponse(SecretRealmDistributionBase):
    """秘境分布响应模式"""
    id: int = Field(..., description="ID")
    project_id: int = Field(..., description="项目ID")
    
    # 探索信息
    discovery_date: Optional[str] = Field(None, description="发现日期")
    discovery_method: Optional[str] = Field(None, description="发现方式")
    discoverer_info: Optional[Dict[str, Any]] = Field(None, description="发现者信息")
    exploration_status: str = Field("未探索", description="探索状态")
    completion_rate: float = Field(0.0, description="完成度")
    
    # 历史记录
    historical_events: Optional[List[Dict[str, Any]]] = Field(None, description="历史事件")
    previous_explorers: Optional[List[Dict[str, Any]]] = Field(None, description="之前的探索者")
    discovery_rewards: Optional[List[Dict[str, Any]]] = Field(None, description="发现奖励")
    exploration_records: Optional[List[Dict[str, Any]]] = Field(None, description="探索记录")
    
    # 影响评估
    environmental_impact: Optional[Dict[str, Any]] = Field(None, description="环境影响")
    local_legends: Optional[List[Dict[str, Any]]] = Field(None, description="当地传说")
    
    # 标签和版本
    tags: Optional[List[str]] = Field(None, description="标签")
    version: str = Field("1.0", description="版本")
    notes: Optional[str] = Field(None, description="备注")
    
    # 时间戳
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class SecretRealmDistributionSummary(BaseModel):
    """秘境分布摘要模式"""
    id: int = Field(..., description="ID")
    name: str = Field(..., description="秘境名称")
    realm_type: RealmType = Field(..., description="秘境类型")
    danger_level: DangerLevel = Field(..., description="危险等级")
    geographic_region: Optional[str] = Field(None, description="地理区域")
    exploration_status: str = Field(..., description="探索状态")
    completion_rate: float = Field(..., description="完成度")
    difficulty_score: Optional[float] = Field(None, description="难度评分")
    
    class Config:
        from_attributes = True


class TreasureData(BaseModel):
    """宝藏数据模式"""
    name: str = Field(..., description="宝藏名称")
    type: str = Field(..., description="宝藏类型")
    rarity: str = Field(..., description="稀有度")
    description: Optional[str] = Field(None, description="描述")
    value: Optional[float] = Field(None, description="价值")


class GuardianCreatureData(BaseModel):
    """守护生物数据模式"""
    name: str = Field(..., description="生物名称")
    type: str = Field(..., description="生物类型")
    level: int = Field(..., description="等级")
    abilities: Optional[List[str]] = Field(None, description="能力")
    description: Optional[str] = Field(None, description="描述")


class TrapSystemData(BaseModel):
    """陷阱系统数据模式"""
    name: str = Field(..., description="陷阱名称")
    type: str = Field(..., description="陷阱类型")
    trigger_condition: str = Field(..., description="触发条件")
    effect: str = Field(..., description="效果")
    difficulty: int = Field(..., description="难度等级")
    description: Optional[str] = Field(None, description="描述")
