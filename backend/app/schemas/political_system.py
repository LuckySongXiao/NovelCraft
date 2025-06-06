"""
政治体系数据模式
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.political_system import GovernmentType, PowerStructure


class PoliticalSystemBase(BaseModel):
    """政治体系基础模式"""
    name: str = Field(..., description="政治体系名称")
    description: Optional[str] = Field(None, description="描述")
    government_type: GovernmentType = Field(GovernmentType.MONARCHY, description="政府类型")
    power_structure: PowerStructure = Field(PowerStructure.CENTRALIZED, description="权力结构")
    
    # 政府组织
    government_structure: Optional[Dict[str, Any]] = Field(None, description="政府结构")
    leadership: Optional[Dict[str, Any]] = Field(None, description="领导层")
    institutions: Optional[Dict[str, Any]] = Field(None, description="政治机构")
    
    # 法律体系
    legal_system: Optional[Dict[str, Any]] = Field(None, description="法律体系")
    laws: Optional[List[Dict[str, Any]]] = Field(None, description="法律条文")
    enforcement: Optional[Dict[str, Any]] = Field(None, description="执法机构")
    
    # 权力分配
    power_distribution: Optional[Dict[str, Any]] = Field(None, description="权力分配")
    checks_balances: Optional[Dict[str, Any]] = Field(None, description="制衡机制")
    succession_rules: Optional[Dict[str, Any]] = Field(None, description="继承规则")
    
    # 行政区划
    administrative_divisions: Optional[Dict[str, Any]] = Field(None, description="行政区划")
    local_governance: Optional[Dict[str, Any]] = Field(None, description="地方治理")
    
    # 政治文化
    political_culture: Optional[Dict[str, Any]] = Field(None, description="政治文化")
    ideology: Optional[str] = Field(None, description="政治理念")
    traditions: Optional[List[Dict[str, Any]]] = Field(None, description="政治传统")
    
    # 对外关系
    diplomacy: Optional[Dict[str, Any]] = Field(None, description="外交政策")
    alliances: Optional[List[Dict[str, Any]]] = Field(None, description="政治联盟")
    treaties: Optional[List[Dict[str, Any]]] = Field(None, description="条约协议")


class PoliticalSystemCreate(PoliticalSystemBase):
    """创建政治体系模式"""
    project_id: int = Field(..., description="项目ID")
    world_setting_id: Optional[int] = Field(None, description="世界设定ID")


class PoliticalSystemUpdate(BaseModel):
    """更新政治体系模式"""
    name: Optional[str] = Field(None, description="政治体系名称")
    description: Optional[str] = Field(None, description="描述")
    government_type: Optional[GovernmentType] = Field(None, description="政府类型")
    power_structure: Optional[PowerStructure] = Field(None, description="权力结构")
    
    # 政府组织
    government_structure: Optional[Dict[str, Any]] = Field(None, description="政府结构")
    leadership: Optional[Dict[str, Any]] = Field(None, description="领导层")
    institutions: Optional[Dict[str, Any]] = Field(None, description="政治机构")
    
    # 法律体系
    legal_system: Optional[Dict[str, Any]] = Field(None, description="法律体系")
    laws: Optional[List[Dict[str, Any]]] = Field(None, description="法律条文")
    enforcement: Optional[Dict[str, Any]] = Field(None, description="执法机构")
    
    # 权力分配
    power_distribution: Optional[Dict[str, Any]] = Field(None, description="权力分配")
    checks_balances: Optional[Dict[str, Any]] = Field(None, description="制衡机制")
    succession_rules: Optional[Dict[str, Any]] = Field(None, description="继承规则")
    
    # 行政区划
    administrative_divisions: Optional[Dict[str, Any]] = Field(None, description="行政区划")
    local_governance: Optional[Dict[str, Any]] = Field(None, description="地方治理")
    
    # 政治文化
    political_culture: Optional[Dict[str, Any]] = Field(None, description="政治文化")
    ideology: Optional[str] = Field(None, description="政治理念")
    traditions: Optional[List[Dict[str, Any]]] = Field(None, description="政治传统")
    
    # 对外关系
    diplomacy: Optional[Dict[str, Any]] = Field(None, description="外交政策")
    alliances: Optional[List[Dict[str, Any]]] = Field(None, description="政治联盟")
    treaties: Optional[List[Dict[str, Any]]] = Field(None, description="条约协议")


class PoliticalSystemResponse(PoliticalSystemBase):
    """政治体系响应模式"""
    id: int = Field(..., description="ID")
    project_id: int = Field(..., description="项目ID")
    world_setting_id: Optional[int] = Field(None, description="世界设定ID")
    
    # 时间戳
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    # 计算字段
    summary: Optional[str] = Field(None, description="摘要")
    stability_score: Optional[float] = Field(None, description="稳定性评分")
    consistency_issues: Optional[List[str]] = Field(None, description="一致性问题")
    tags: Optional[List[str]] = Field(None, description="标签")

    class Config:
        from_attributes = True


class InstitutionCreate(BaseModel):
    """政治机构创建模式"""
    name: str = Field(..., description="机构名称")
    type: str = Field(..., description="机构类型")
    description: Optional[str] = Field(None, description="描述")
    functions: Optional[List[str]] = Field(None, description="职能")
    structure: Optional[Dict[str, Any]] = Field(None, description="组织结构")
    powers: Optional[List[str]] = Field(None, description="权力")


class LawCreate(BaseModel):
    """法律创建模式"""
    name: str = Field(..., description="法律名称")
    type: str = Field(..., description="法律类型")
    description: Optional[str] = Field(None, description="描述")
    content: Optional[str] = Field(None, description="法律内容")
    scope: Optional[str] = Field(None, description="适用范围")
    penalties: Optional[List[Dict[str, Any]]] = Field(None, description="处罚措施")


class AllianceCreate(BaseModel):
    """政治联盟创建模式"""
    name: str = Field(..., description="联盟名称")
    type: str = Field(..., description="联盟类型")
    description: Optional[str] = Field(None, description="描述")
    members: Optional[List[str]] = Field(None, description="成员")
    purpose: Optional[str] = Field(None, description="目的")
    terms: Optional[Dict[str, Any]] = Field(None, description="条款")


class TreatyCreate(BaseModel):
    """条约创建模式"""
    name: str = Field(..., description="条约名称")
    type: str = Field(..., description="条约类型")
    description: Optional[str] = Field(None, description="描述")
    parties: Optional[List[str]] = Field(None, description="缔约方")
    content: Optional[str] = Field(None, description="条约内容")
    duration: Optional[str] = Field(None, description="有效期")
    conditions: Optional[Dict[str, Any]] = Field(None, description="条件")
