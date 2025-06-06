"""
职业体系数据模式
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.profession_system import ProfessionCategory, SkillLevel, CareerPath


class ProfessionSystemBase(BaseModel):
    """职业体系基础模式"""
    name: str = Field(..., description="职业体系名称")
    description: Optional[str] = Field(None, description="描述")
    dimension_id: Optional[int] = Field(None, description="维度ID")
    economic_context: Optional[str] = Field(None, description="经济背景")
    
    # 职业分类
    profession_categories: Optional[Dict[str, Any]] = Field(None, description="职业分类")
    profession_hierarchy: Optional[Dict[str, Any]] = Field(None, description="职业等级")
    profession_relationships: Optional[Dict[str, Any]] = Field(None, description="职业关系")
    
    # 技能体系
    skill_framework: Optional[Dict[str, Any]] = Field(None, description="技能框架")
    skill_requirements: Optional[Dict[str, Any]] = Field(None, description="技能要求")
    skill_development: Optional[Dict[str, Any]] = Field(None, description="技能发展")
    
    # 晋升路径
    career_paths: Optional[Dict[str, Any]] = Field(None, description="职业发展路径")
    promotion_criteria: Optional[Dict[str, Any]] = Field(None, description="晋升标准")
    advancement_barriers: Optional[Dict[str, Any]] = Field(None, description="晋升障碍")
    
    # 行业组织
    professional_organizations: Optional[Dict[str, Any]] = Field(None, description="行业组织")
    guilds: Optional[Dict[str, Any]] = Field(None, description="公会组织")
    unions: Optional[Dict[str, Any]] = Field(None, description="工会组织")
    
    # 教育培训
    training_systems: Optional[Dict[str, Any]] = Field(None, description="培训体系")
    apprenticeship_programs: Optional[Dict[str, Any]] = Field(None, description="学徒制度")
    certification_systems: Optional[Dict[str, Any]] = Field(None, description="认证体系")
    
    # 薪酬福利
    compensation_structure: Optional[Dict[str, Any]] = Field(None, description="薪酬结构")
    benefit_systems: Optional[Dict[str, Any]] = Field(None, description="福利制度")
    economic_incentives: Optional[Dict[str, Any]] = Field(None, description="经济激励")
    
    # 工作环境
    working_conditions: Optional[Dict[str, Any]] = Field(None, description="工作条件")
    workplace_culture: Optional[Dict[str, Any]] = Field(None, description="职场文化")
    safety_standards: Optional[Dict[str, Any]] = Field(None, description="安全标准")
    
    # 职业流动性
    mobility_patterns: Optional[Dict[str, Any]] = Field(None, description="流动模式")
    career_transitions: Optional[Dict[str, Any]] = Field(None, description="职业转换")
    social_mobility: Optional[Dict[str, Any]] = Field(None, description="社会流动")
    
    # 专业伦理
    professional_ethics: Optional[Dict[str, Any]] = Field(None, description="职业伦理")
    codes_of_conduct: Optional[Dict[str, Any]] = Field(None, description="行为准则")
    disciplinary_measures: Optional[Dict[str, Any]] = Field(None, description="纪律措施")
    
    # 技术创新
    technological_impact: Optional[Dict[str, Any]] = Field(None, description="技术影响")
    innovation_trends: Optional[Dict[str, Any]] = Field(None, description="创新趋势")
    future_skills: Optional[Dict[str, Any]] = Field(None, description="未来技能")
    
    # 维度特性
    dimensional_professions: Optional[Dict[str, Any]] = Field(None, description="维度特有职业")
    cross_dimensional_careers: Optional[Dict[str, Any]] = Field(None, description="跨维度职业")
    dimensional_skill_transfer: Optional[Dict[str, Any]] = Field(None, description="维度技能转移")
    
    # 市场需求
    labor_market: Optional[Dict[str, Any]] = Field(None, description="劳动力市场")
    demand_trends: Optional[Dict[str, Any]] = Field(None, description="需求趋势")
    supply_analysis: Optional[Dict[str, Any]] = Field(None, description="供给分析")


class ProfessionSystemCreate(ProfessionSystemBase):
    """创建职业体系模式"""
    project_id: int = Field(..., description="项目ID")
    world_setting_id: Optional[int] = Field(None, description="世界设定ID")


class ProfessionSystemUpdate(BaseModel):
    """更新职业体系模式"""
    name: Optional[str] = Field(None, description="职业体系名称")
    description: Optional[str] = Field(None, description="描述")
    dimension_id: Optional[int] = Field(None, description="维度ID")
    economic_context: Optional[str] = Field(None, description="经济背景")
    
    # 职业分类
    profession_categories: Optional[Dict[str, Any]] = Field(None, description="职业分类")
    profession_hierarchy: Optional[Dict[str, Any]] = Field(None, description="职业等级")
    profession_relationships: Optional[Dict[str, Any]] = Field(None, description="职业关系")
    
    # 技能体系
    skill_framework: Optional[Dict[str, Any]] = Field(None, description="技能框架")
    skill_requirements: Optional[Dict[str, Any]] = Field(None, description="技能要求")
    skill_development: Optional[Dict[str, Any]] = Field(None, description="技能发展")
    
    # 晋升路径
    career_paths: Optional[Dict[str, Any]] = Field(None, description="职业发展路径")
    promotion_criteria: Optional[Dict[str, Any]] = Field(None, description="晋升标准")
    advancement_barriers: Optional[Dict[str, Any]] = Field(None, description="晋升障碍")
    
    # 行业组织
    professional_organizations: Optional[Dict[str, Any]] = Field(None, description="行业组织")
    guilds: Optional[Dict[str, Any]] = Field(None, description="公会组织")
    unions: Optional[Dict[str, Any]] = Field(None, description="工会组织")
    
    # 教育培训
    training_systems: Optional[Dict[str, Any]] = Field(None, description="培训体系")
    apprenticeship_programs: Optional[Dict[str, Any]] = Field(None, description="学徒制度")
    certification_systems: Optional[Dict[str, Any]] = Field(None, description="认证体系")
    
    # 薪酬福利
    compensation_structure: Optional[Dict[str, Any]] = Field(None, description="薪酬结构")
    benefit_systems: Optional[Dict[str, Any]] = Field(None, description="福利制度")
    economic_incentives: Optional[Dict[str, Any]] = Field(None, description="经济激励")
    
    # 工作环境
    working_conditions: Optional[Dict[str, Any]] = Field(None, description="工作条件")
    workplace_culture: Optional[Dict[str, Any]] = Field(None, description="职场文化")
    safety_standards: Optional[Dict[str, Any]] = Field(None, description="安全标准")
    
    # 职业流动性
    mobility_patterns: Optional[Dict[str, Any]] = Field(None, description="流动模式")
    career_transitions: Optional[Dict[str, Any]] = Field(None, description="职业转换")
    social_mobility: Optional[Dict[str, Any]] = Field(None, description="社会流动")
    
    # 专业伦理
    professional_ethics: Optional[Dict[str, Any]] = Field(None, description="职业伦理")
    codes_of_conduct: Optional[Dict[str, Any]] = Field(None, description="行为准则")
    disciplinary_measures: Optional[Dict[str, Any]] = Field(None, description="纪律措施")
    
    # 技术创新
    technological_impact: Optional[Dict[str, Any]] = Field(None, description="技术影响")
    innovation_trends: Optional[Dict[str, Any]] = Field(None, description="创新趋势")
    future_skills: Optional[Dict[str, Any]] = Field(None, description="未来技能")
    
    # 维度特性
    dimensional_professions: Optional[Dict[str, Any]] = Field(None, description="维度特有职业")
    cross_dimensional_careers: Optional[Dict[str, Any]] = Field(None, description="跨维度职业")
    dimensional_skill_transfer: Optional[Dict[str, Any]] = Field(None, description="维度技能转移")
    
    # 市场需求
    labor_market: Optional[Dict[str, Any]] = Field(None, description="劳动力市场")
    demand_trends: Optional[Dict[str, Any]] = Field(None, description="需求趋势")
    supply_analysis: Optional[Dict[str, Any]] = Field(None, description="供给分析")


class ProfessionSystemResponse(ProfessionSystemBase):
    """职业体系响应模式"""
    id: int = Field(..., description="ID")
    project_id: int = Field(..., description="项目ID")
    world_setting_id: Optional[int] = Field(None, description="世界设定ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    # 计算字段
    profession_metrics: Optional[Dict[str, Any]] = Field(None, description="职业体系指标")
    
    class Config:
        from_attributes = True


class ProfessionData(BaseModel):
    """职业数据模式"""
    name: str = Field(..., description="职业名称")
    category: ProfessionCategory = Field(..., description="职业类别")
    description: Optional[str] = Field(None, description="职业描述")
    requirements: Optional[List[str]] = Field(None, description="职业要求")
    responsibilities: Optional[List[str]] = Field(None, description="职责")
    salary_range: Optional[Dict[str, float]] = Field(None, description="薪资范围")


class SkillData(BaseModel):
    """技能数据模式"""
    name: str = Field(..., description="技能名称")
    category: str = Field(..., description="技能类别")
    level: SkillLevel = Field(..., description="技能等级")
    description: Optional[str] = Field(None, description="技能描述")
    prerequisites: Optional[List[str]] = Field(None, description="前置条件")
    learning_time: Optional[int] = Field(None, description="学习时间(小时)")


class CareerPathData(BaseModel):
    """职业发展路径数据模式"""
    name: str = Field(..., description="路径名称")
    path_type: CareerPath = Field(..., description="路径类型")
    from_profession: str = Field(..., description="起始职业")
    to_profession: str = Field(..., description="目标职业")
    requirements: Optional[List[str]] = Field(None, description="转换要求")
    duration: Optional[int] = Field(None, description="转换时间(月)")


class ProfessionalOrganizationData(BaseModel):
    """行业组织数据模式"""
    name: str = Field(..., description="组织名称")
    type: str = Field(..., description="组织类型")
    professions: List[str] = Field(..., description="相关职业")
    services: Optional[List[str]] = Field(None, description="提供服务")
    membership_requirements: Optional[List[str]] = Field(None, description="会员要求")


class SkillGapAnalysisData(BaseModel):
    """技能差距分析数据模式"""
    target_profession: str = Field(..., description="目标职业")
    total_skills_required: int = Field(..., description="所需技能总数")
    skill_categories: Dict[str, int] = Field(..., description="技能类别分布")
    difficulty_levels: Dict[str, int] = Field(..., description="难度等级分布")
    training_recommendations: List[str] = Field(..., description="培训建议")
