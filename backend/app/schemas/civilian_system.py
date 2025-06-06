"""
生民体系数据模式
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.civilian_system import SocialClass, LifestyleType


class CivilianSystemBase(BaseModel):
    """生民体系基础模式"""
    name: str = Field(..., description="生民体系名称")
    description: Optional[str] = Field(None, description="描述")
    dimension_id: Optional[int] = Field(None, description="维度ID")
    region_name: Optional[str] = Field(None, description="区域名称")
    
    # 人口统计
    total_population: Optional[int] = Field(0, description="总人口")
    population_density: Optional[float] = Field(0.0, description="人口密度")
    population_growth_rate: Optional[float] = Field(0.0, description="人口增长率")
    age_distribution: Optional[Dict[str, Any]] = Field(None, description="年龄分布")
    gender_distribution: Optional[Dict[str, Any]] = Field(None, description="性别分布")
    
    # 社会阶层
    social_classes: Optional[Dict[str, Any]] = Field(None, description="社会阶层结构")
    class_mobility: Optional[Dict[str, Any]] = Field(None, description="阶层流动性")
    social_hierarchy: Optional[Dict[str, Any]] = Field(None, description="社会等级制度")
    
    # 生活方式
    lifestyle_types: Optional[Dict[str, Any]] = Field(None, description="生活方式类型")
    living_conditions: Optional[Dict[str, Any]] = Field(None, description="生活条件")
    daily_routines: Optional[Dict[str, Any]] = Field(None, description="日常作息")
    
    # 文化习俗
    cultural_practices: Optional[Dict[str, Any]] = Field(None, description="文化习俗")
    traditions: Optional[Dict[str, Any]] = Field(None, description="传统节日")
    customs: Optional[Dict[str, Any]] = Field(None, description="风俗习惯")
    languages: Optional[Dict[str, Any]] = Field(None, description="语言文字")
    
    # 教育体系
    education_system: Optional[Dict[str, Any]] = Field(None, description="教育制度")
    literacy_rate: Optional[float] = Field(0.0, description="识字率")
    educational_institutions: Optional[Dict[str, Any]] = Field(None, description="教育机构")
    
    # 宗教信仰
    religious_beliefs: Optional[Dict[str, Any]] = Field(None, description="宗教信仰")
    religious_practices: Optional[Dict[str, Any]] = Field(None, description="宗教仪式")
    religious_institutions: Optional[Dict[str, Any]] = Field(None, description="宗教机构")
    
    # 社会保障
    welfare_system: Optional[Dict[str, Any]] = Field(None, description="社会保障制度")
    healthcare_system: Optional[Dict[str, Any]] = Field(None, description="医疗保健体系")
    social_services: Optional[Dict[str, Any]] = Field(None, description="社会服务")
    
    # 家庭结构
    family_structure: Optional[Dict[str, Any]] = Field(None, description="家庭结构")
    marriage_customs: Optional[Dict[str, Any]] = Field(None, description="婚姻习俗")
    inheritance_rules: Optional[Dict[str, Any]] = Field(None, description="继承规则")
    
    # 社会问题
    social_issues: Optional[Dict[str, Any]] = Field(None, description="社会问题")
    crime_rates: Optional[Dict[str, Any]] = Field(None, description="犯罪率统计")
    social_conflicts: Optional[Dict[str, Any]] = Field(None, description="社会冲突")
    
    # 维度特性
    dimensional_traits: Optional[Dict[str, Any]] = Field(None, description="维度特有特征")
    cross_dimensional_relations: Optional[Dict[str, Any]] = Field(None, description="跨维度关系")


class CivilianSystemCreate(CivilianSystemBase):
    """创建生民体系模式"""
    project_id: int = Field(..., description="项目ID")
    world_setting_id: Optional[int] = Field(None, description="世界设定ID")


class CivilianSystemUpdate(BaseModel):
    """更新生民体系模式"""
    name: Optional[str] = Field(None, description="生民体系名称")
    description: Optional[str] = Field(None, description="描述")
    dimension_id: Optional[int] = Field(None, description="维度ID")
    region_name: Optional[str] = Field(None, description="区域名称")
    
    # 人口统计
    total_population: Optional[int] = Field(None, description="总人口")
    population_density: Optional[float] = Field(None, description="人口密度")
    population_growth_rate: Optional[float] = Field(None, description="人口增长率")
    age_distribution: Optional[Dict[str, Any]] = Field(None, description="年龄分布")
    gender_distribution: Optional[Dict[str, Any]] = Field(None, description="性别分布")
    
    # 社会阶层
    social_classes: Optional[Dict[str, Any]] = Field(None, description="社会阶层结构")
    class_mobility: Optional[Dict[str, Any]] = Field(None, description="阶层流动性")
    social_hierarchy: Optional[Dict[str, Any]] = Field(None, description="社会等级制度")
    
    # 生活方式
    lifestyle_types: Optional[Dict[str, Any]] = Field(None, description="生活方式类型")
    living_conditions: Optional[Dict[str, Any]] = Field(None, description="生活条件")
    daily_routines: Optional[Dict[str, Any]] = Field(None, description="日常作息")
    
    # 文化习俗
    cultural_practices: Optional[Dict[str, Any]] = Field(None, description="文化习俗")
    traditions: Optional[Dict[str, Any]] = Field(None, description="传统节日")
    customs: Optional[Dict[str, Any]] = Field(None, description="风俗习惯")
    languages: Optional[Dict[str, Any]] = Field(None, description="语言文字")
    
    # 教育体系
    education_system: Optional[Dict[str, Any]] = Field(None, description="教育制度")
    literacy_rate: Optional[float] = Field(None, description="识字率")
    educational_institutions: Optional[Dict[str, Any]] = Field(None, description="教育机构")
    
    # 宗教信仰
    religious_beliefs: Optional[Dict[str, Any]] = Field(None, description="宗教信仰")
    religious_practices: Optional[Dict[str, Any]] = Field(None, description="宗教仪式")
    religious_institutions: Optional[Dict[str, Any]] = Field(None, description="宗教机构")
    
    # 社会保障
    welfare_system: Optional[Dict[str, Any]] = Field(None, description="社会保障制度")
    healthcare_system: Optional[Dict[str, Any]] = Field(None, description="医疗保健体系")
    social_services: Optional[Dict[str, Any]] = Field(None, description="社会服务")
    
    # 家庭结构
    family_structure: Optional[Dict[str, Any]] = Field(None, description="家庭结构")
    marriage_customs: Optional[Dict[str, Any]] = Field(None, description="婚姻习俗")
    inheritance_rules: Optional[Dict[str, Any]] = Field(None, description="继承规则")
    
    # 社会问题
    social_issues: Optional[Dict[str, Any]] = Field(None, description="社会问题")
    crime_rates: Optional[Dict[str, Any]] = Field(None, description="犯罪率统计")
    social_conflicts: Optional[Dict[str, Any]] = Field(None, description="社会冲突")
    
    # 维度特性
    dimensional_traits: Optional[Dict[str, Any]] = Field(None, description="维度特有特征")
    cross_dimensional_relations: Optional[Dict[str, Any]] = Field(None, description="跨维度关系")


class CivilianSystemResponse(CivilianSystemBase):
    """生民体系响应模式"""
    id: int = Field(..., description="ID")
    project_id: int = Field(..., description="项目ID")
    world_setting_id: Optional[int] = Field(None, description="世界设定ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    # 计算字段
    social_metrics: Optional[Dict[str, Any]] = Field(None, description="社会指标")
    
    class Config:
        from_attributes = True


class SocialClassData(BaseModel):
    """社会阶层数据模式"""
    name: str = Field(..., description="阶层名称")
    class_type: SocialClass = Field(..., description="阶层类型")
    population_percentage: float = Field(0.0, description="人口占比")
    characteristics: Optional[Dict[str, Any]] = Field(None, description="阶层特征")
    privileges: Optional[List[str]] = Field(None, description="特权")
    responsibilities: Optional[List[str]] = Field(None, description="责任")


class LifestyleData(BaseModel):
    """生活方式数据模式"""
    name: str = Field(..., description="生活方式名称")
    lifestyle_type: LifestyleType = Field(..., description="生活方式类型")
    description: Optional[str] = Field(None, description="描述")
    characteristics: Optional[Dict[str, Any]] = Field(None, description="特征")
    requirements: Optional[List[str]] = Field(None, description="要求")


class CulturalPracticeData(BaseModel):
    """文化习俗数据模式"""
    name: str = Field(..., description="习俗名称")
    type: str = Field(..., description="习俗类型")
    description: Optional[str] = Field(None, description="描述")
    significance: Optional[str] = Field(None, description="意义")
    participants: Optional[List[str]] = Field(None, description="参与者")
    frequency: Optional[str] = Field(None, description="频率")


class PopulationStatsData(BaseModel):
    """人口统计数据模式"""
    total_population: int = Field(..., description="总人口")
    population_density: float = Field(..., description="人口密度")
    growth_rate: float = Field(..., description="增长率")
    age_distribution: Dict[str, float] = Field(..., description="年龄分布")
    gender_distribution: Dict[str, float] = Field(..., description="性别分布")


class DimensionalComparisonData(BaseModel):
    """维度比较数据模式"""
    target_dimension_id: int = Field(..., description="目标维度ID")
    population_ratio: float = Field(0.0, description="人口比例")
    cultural_similarity: float = Field(0.0, description="文化相似性")
    social_structure_similarity: float = Field(0.0, description="社会结构相似性")
    lifestyle_similarity: float = Field(0.0, description="生活方式相似性")
