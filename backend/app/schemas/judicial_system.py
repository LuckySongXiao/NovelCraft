"""
司法体系数据模式
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.judicial_system import CourtType, LegalSystem, TrialProcedure


class JudicialSystemBase(BaseModel):
    """司法体系基础模式"""
    name: str = Field(..., description="司法体系名称")
    description: Optional[str] = Field(None, description="描述")
    dimension_id: Optional[int] = Field(None, description="维度ID")
    jurisdiction_name: Optional[str] = Field(None, description="司法管辖区名称")
    legal_system_type: LegalSystem = Field(LegalSystem.CIVIL_LAW, description="法律体系类型")
    
    # 法院体系
    court_structure: Optional[Dict[str, Any]] = Field(None, description="法院结构")
    court_hierarchy: Optional[Dict[str, Any]] = Field(None, description="法院层级")
    specialized_courts: Optional[Dict[str, Any]] = Field(None, description="专门法院")
    
    # 审判程序
    trial_procedures: Optional[Dict[str, Any]] = Field(None, description="审判程序")
    procedure_type: TrialProcedure = Field(TrialProcedure.MIXED, description="程序类型")
    appeal_process: Optional[Dict[str, Any]] = Field(None, description="上诉程序")
    
    # 执法机构
    law_enforcement: Optional[Dict[str, Any]] = Field(None, description="执法机构")
    police_system: Optional[Dict[str, Any]] = Field(None, description="警察体系")
    investigation_agencies: Optional[Dict[str, Any]] = Field(None, description="调查机构")
    
    # 法律条文
    legal_codes: Optional[Dict[str, Any]] = Field(None, description="法律法规")
    constitutional_law: Optional[Dict[str, Any]] = Field(None, description="宪法")
    criminal_law: Optional[Dict[str, Any]] = Field(None, description="刑法")
    civil_law: Optional[Dict[str, Any]] = Field(None, description="民法")
    administrative_law: Optional[Dict[str, Any]] = Field(None, description="行政法")
    
    # 司法人员
    judicial_personnel: Optional[Dict[str, Any]] = Field(None, description="司法人员")
    judge_system: Optional[Dict[str, Any]] = Field(None, description="法官制度")
    prosecutor_system: Optional[Dict[str, Any]] = Field(None, description="检察官制度")
    lawyer_system: Optional[Dict[str, Any]] = Field(None, description="律师制度")
    
    # 刑罚制度
    punishment_system: Optional[Dict[str, Any]] = Field(None, description="刑罚制度")
    sentencing_guidelines: Optional[Dict[str, Any]] = Field(None, description="量刑指导")
    rehabilitation_programs: Optional[Dict[str, Any]] = Field(None, description="改造项目")
    
    # 司法监督
    judicial_oversight: Optional[Dict[str, Any]] = Field(None, description="司法监督")
    accountability_mechanisms: Optional[Dict[str, Any]] = Field(None, description="问责机制")
    transparency_measures: Optional[Dict[str, Any]] = Field(None, description="透明度措施")
    
    # 替代性争议解决
    alternative_dispute_resolution: Optional[Dict[str, Any]] = Field(None, description="替代性争议解决")
    mediation_system: Optional[Dict[str, Any]] = Field(None, description="调解制度")
    arbitration_system: Optional[Dict[str, Any]] = Field(None, description="仲裁制度")
    
    # 司法统计
    case_statistics: Optional[Dict[str, Any]] = Field(None, description="案件统计")
    conviction_rates: Optional[Dict[str, Any]] = Field(None, description="定罪率")
    appeal_success_rates: Optional[Dict[str, Any]] = Field(None, description="上诉成功率")
    
    # 维度特性
    dimensional_laws: Optional[Dict[str, Any]] = Field(None, description="维度特有法律")
    cross_dimensional_jurisdiction: Optional[Dict[str, Any]] = Field(None, description="跨维度管辖权")
    dimensional_enforcement: Optional[Dict[str, Any]] = Field(None, description="维度执法机制")
    
    # 司法改革
    reform_history: Optional[Dict[str, Any]] = Field(None, description="改革历史")
    ongoing_reforms: Optional[Dict[str, Any]] = Field(None, description="正在进行的改革")
    future_plans: Optional[Dict[str, Any]] = Field(None, description="未来规划")


class JudicialSystemCreate(JudicialSystemBase):
    """创建司法体系模式"""
    project_id: int = Field(..., description="项目ID")
    world_setting_id: Optional[int] = Field(None, description="世界设定ID")


class JudicialSystemUpdate(BaseModel):
    """更新司法体系模式"""
    name: Optional[str] = Field(None, description="司法体系名称")
    description: Optional[str] = Field(None, description="描述")
    dimension_id: Optional[int] = Field(None, description="维度ID")
    jurisdiction_name: Optional[str] = Field(None, description="司法管辖区名称")
    legal_system_type: Optional[LegalSystem] = Field(None, description="法律体系类型")
    
    # 法院体系
    court_structure: Optional[Dict[str, Any]] = Field(None, description="法院结构")
    court_hierarchy: Optional[Dict[str, Any]] = Field(None, description="法院层级")
    specialized_courts: Optional[Dict[str, Any]] = Field(None, description="专门法院")
    
    # 审判程序
    trial_procedures: Optional[Dict[str, Any]] = Field(None, description="审判程序")
    procedure_type: Optional[TrialProcedure] = Field(None, description="程序类型")
    appeal_process: Optional[Dict[str, Any]] = Field(None, description="上诉程序")
    
    # 执法机构
    law_enforcement: Optional[Dict[str, Any]] = Field(None, description="执法机构")
    police_system: Optional[Dict[str, Any]] = Field(None, description="警察体系")
    investigation_agencies: Optional[Dict[str, Any]] = Field(None, description="调查机构")
    
    # 法律条文
    legal_codes: Optional[Dict[str, Any]] = Field(None, description="法律法规")
    constitutional_law: Optional[Dict[str, Any]] = Field(None, description="宪法")
    criminal_law: Optional[Dict[str, Any]] = Field(None, description="刑法")
    civil_law: Optional[Dict[str, Any]] = Field(None, description="民法")
    administrative_law: Optional[Dict[str, Any]] = Field(None, description="行政法")
    
    # 司法人员
    judicial_personnel: Optional[Dict[str, Any]] = Field(None, description="司法人员")
    judge_system: Optional[Dict[str, Any]] = Field(None, description="法官制度")
    prosecutor_system: Optional[Dict[str, Any]] = Field(None, description="检察官制度")
    lawyer_system: Optional[Dict[str, Any]] = Field(None, description="律师制度")
    
    # 刑罚制度
    punishment_system: Optional[Dict[str, Any]] = Field(None, description="刑罚制度")
    sentencing_guidelines: Optional[Dict[str, Any]] = Field(None, description="量刑指导")
    rehabilitation_programs: Optional[Dict[str, Any]] = Field(None, description="改造项目")
    
    # 司法监督
    judicial_oversight: Optional[Dict[str, Any]] = Field(None, description="司法监督")
    accountability_mechanisms: Optional[Dict[str, Any]] = Field(None, description="问责机制")
    transparency_measures: Optional[Dict[str, Any]] = Field(None, description="透明度措施")
    
    # 替代性争议解决
    alternative_dispute_resolution: Optional[Dict[str, Any]] = Field(None, description="替代性争议解决")
    mediation_system: Optional[Dict[str, Any]] = Field(None, description="调解制度")
    arbitration_system: Optional[Dict[str, Any]] = Field(None, description="仲裁制度")
    
    # 司法统计
    case_statistics: Optional[Dict[str, Any]] = Field(None, description="案件统计")
    conviction_rates: Optional[Dict[str, Any]] = Field(None, description="定罪率")
    appeal_success_rates: Optional[Dict[str, Any]] = Field(None, description="上诉成功率")
    
    # 维度特性
    dimensional_laws: Optional[Dict[str, Any]] = Field(None, description="维度特有法律")
    cross_dimensional_jurisdiction: Optional[Dict[str, Any]] = Field(None, description="跨维度管辖权")
    dimensional_enforcement: Optional[Dict[str, Any]] = Field(None, description="维度执法机制")
    
    # 司法改革
    reform_history: Optional[Dict[str, Any]] = Field(None, description="改革历史")
    ongoing_reforms: Optional[Dict[str, Any]] = Field(None, description="正在进行的改革")
    future_plans: Optional[Dict[str, Any]] = Field(None, description="未来规划")


class JudicialSystemResponse(JudicialSystemBase):
    """司法体系响应模式"""
    id: int = Field(..., description="ID")
    project_id: int = Field(..., description="项目ID")
    world_setting_id: Optional[int] = Field(None, description="世界设定ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    # 计算字段
    judicial_efficiency: Optional[Dict[str, Any]] = Field(None, description="司法效率指标")
    
    class Config:
        from_attributes = True


class CourtData(BaseModel):
    """法院数据模式"""
    name: str = Field(..., description="法院名称")
    court_type: CourtType = Field(..., description="法院类型")
    jurisdiction: Optional[str] = Field(None, description="管辖范围")
    level: Optional[int] = Field(None, description="法院级别")
    location: Optional[str] = Field(None, description="所在地")
    judges_count: Optional[int] = Field(None, description="法官数量")


class LegalCodeData(BaseModel):
    """法律条文数据模式"""
    title: str = Field(..., description="法律标题")
    type: str = Field(..., description="法律类型")
    content: str = Field(..., description="法律内容")
    effective_date: Optional[datetime] = Field(None, description="生效日期")
    status: Optional[str] = Field("active", description="状态")


class EnforcementAgencyData(BaseModel):
    """执法机构数据模式"""
    name: str = Field(..., description="机构名称")
    type: str = Field(..., description="机构类型")
    jurisdiction: Optional[str] = Field(None, description="管辖范围")
    powers: Optional[List[str]] = Field(None, description="执法权力")
    personnel_count: Optional[int] = Field(None, description="人员数量")


class JudicialPersonnelData(BaseModel):
    """司法人员数据模式"""
    name: str = Field(..., description="人员姓名")
    type: str = Field(..., description="人员类型")
    position: str = Field(..., description="职位")
    qualifications: Optional[List[str]] = Field(None, description="资格")
    experience_years: Optional[int] = Field(None, description="从业年限")


class CrossDimensionalCaseData(BaseModel):
    """跨维度案件数据模式"""
    case_id: str = Field(..., description="案件ID")
    type: str = Field(..., description="案件类型")
    dimensions: List[int] = Field(..., description="涉及维度")
    jurisdiction_rules: Optional[Dict[str, Any]] = Field(None, description="管辖规则")
    applicable_laws: Optional[List[str]] = Field(None, description="适用法律")
