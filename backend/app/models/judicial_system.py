"""
司法体系模型
"""
from sqlalchemy import Column, Integer, String, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class CourtType(str, Enum):
    """法院类型枚举"""
    SUPREME = "supreme"  # 最高法院
    APPELLATE = "appellate"  # 上诉法院
    TRIAL = "trial"  # 审判法院
    SPECIALIZED = "specialized"  # 专门法院
    MILITARY = "military"  # 军事法院
    RELIGIOUS = "religious"  # 宗教法院
    COMMERCIAL = "commercial"  # 商事法院
    FAMILY = "family"  # 家事法院


class LegalSystem(str, Enum):
    """法律体系类型枚举"""
    CIVIL_LAW = "civil_law"  # 成文法系
    COMMON_LAW = "common_law"  # 普通法系
    RELIGIOUS_LAW = "religious_law"  # 宗教法系
    CUSTOMARY_LAW = "customary_law"  # 习惯法系
    MIXED_SYSTEM = "mixed_system"  # 混合法系


class TrialProcedure(str, Enum):
    """审判程序类型枚举"""
    INQUISITORIAL = "inquisitorial"  # 纠问式
    ADVERSARIAL = "adversarial"  # 对抗式
    MIXED = "mixed"  # 混合式


class JudicialSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """司法体系模型"""

    __tablename__ = "judicial_systems"

    # 基本信息
    dimension_id = Column(Integer, comment="维度ID")
    jurisdiction_name = Column(String(200), comment="司法管辖区名称")
    legal_system_type = Column(String(50), default=LegalSystem.CIVIL_LAW, comment="法律体系类型")
    
    # 法院体系
    court_structure = Column(JSON, comment="法院结构")
    court_hierarchy = Column(JSON, comment="法院层级")
    specialized_courts = Column(JSON, comment="专门法院")
    
    # 审判程序
    trial_procedures = Column(JSON, comment="审判程序")
    procedure_type = Column(String(50), default=TrialProcedure.MIXED, comment="程序类型")
    appeal_process = Column(JSON, comment="上诉程序")
    
    # 执法机构
    law_enforcement = Column(JSON, comment="执法机构")
    police_system = Column(JSON, comment="警察体系")
    investigation_agencies = Column(JSON, comment="调查机构")
    
    # 法律条文
    legal_codes = Column(JSON, comment="法律法规")
    constitutional_law = Column(JSON, comment="宪法")
    criminal_law = Column(JSON, comment="刑法")
    civil_law = Column(JSON, comment="民法")
    administrative_law = Column(JSON, comment="行政法")
    
    # 司法人员
    judicial_personnel = Column(JSON, comment="司法人员")
    judge_system = Column(JSON, comment="法官制度")
    prosecutor_system = Column(JSON, comment="检察官制度")
    lawyer_system = Column(JSON, comment="律师制度")
    
    # 刑罚制度
    punishment_system = Column(JSON, comment="刑罚制度")
    sentencing_guidelines = Column(JSON, comment="量刑指导")
    rehabilitation_programs = Column(JSON, comment="改造项目")
    
    # 司法监督
    judicial_oversight = Column(JSON, comment="司法监督")
    accountability_mechanisms = Column(JSON, comment="问责机制")
    transparency_measures = Column(JSON, comment="透明度措施")
    
    # 替代性争议解决
    alternative_dispute_resolution = Column(JSON, comment="替代性争议解决")
    mediation_system = Column(JSON, comment="调解制度")
    arbitration_system = Column(JSON, comment="仲裁制度")
    
    # 司法统计
    case_statistics = Column(JSON, comment="案件统计")
    conviction_rates = Column(JSON, comment="定罪率")
    appeal_success_rates = Column(JSON, comment="上诉成功率")
    
    # 维度特性
    dimensional_laws = Column(JSON, comment="维度特有法律")
    cross_dimensional_jurisdiction = Column(JSON, comment="跨维度管辖权")
    dimensional_enforcement = Column(JSON, comment="维度执法机制")
    
    # 司法改革
    reform_history = Column(JSON, comment="改革历史")
    ongoing_reforms = Column(JSON, comment="正在进行的改革")
    future_plans = Column(JSON, comment="未来规划")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.court_structure:
            self.court_structure = {
                "courts": [],
                "hierarchy": [],
                "jurisdiction": {}
            }
        
        if not self.trial_procedures:
            self.trial_procedures = {
                "criminal": {},
                "civil": {},
                "administrative": {}
            }
        
        if not self.law_enforcement:
            self.law_enforcement = {
                "agencies": [],
                "structure": {},
                "powers": {}
            }
        
        if not self.legal_codes:
            self.legal_codes = {
                "constitution": {},
                "criminal": {},
                "civil": {},
                "administrative": {}
            }

    def add_court(self, court_data):
        """添加法院"""
        if not self.court_structure:
            self.court_structure = {"courts": [], "hierarchy": [], "jurisdiction": {}}
        
        self.court_structure["courts"].append(court_data)
        return True

    def add_legal_code(self, code_data):
        """添加法律条文"""
        if not self.legal_codes:
            self.legal_codes = {"constitution": {}, "criminal": {}, "civil": {}, "administrative": {}}
        
        code_type = code_data.get("type", "civil")
        if code_type in self.legal_codes:
            if "articles" not in self.legal_codes[code_type]:
                self.legal_codes[code_type]["articles"] = []
            self.legal_codes[code_type]["articles"].append(code_data)
        return True

    def add_enforcement_agency(self, agency_data):
        """添加执法机构"""
        if not self.law_enforcement:
            self.law_enforcement = {"agencies": [], "structure": {}, "powers": {}}
        
        self.law_enforcement["agencies"].append(agency_data)
        return True

    def add_judicial_personnel(self, personnel_data):
        """添加司法人员"""
        if not self.judicial_personnel:
            self.judicial_personnel = {"judges": [], "prosecutors": [], "lawyers": []}
        
        personnel_type = personnel_data.get("type", "judges")
        if personnel_type in self.judicial_personnel:
            self.judicial_personnel[personnel_type].append(personnel_data)
        return True

    def calculate_judicial_efficiency(self):
        """计算司法效率指标"""
        efficiency = {
            "case_processing_speed": 0.0,
            "conviction_accuracy": 0.0,
            "appeal_success_rate": 0.0,
            "public_trust": 0.0
        }
        
        # 案件处理速度
        if self.case_statistics and "average_processing_time" in self.case_statistics:
            avg_time = self.case_statistics["average_processing_time"]
            efficiency["case_processing_speed"] = max(0, 100 - avg_time)  # 简化计算
        
        # 定罪准确率
        if self.conviction_rates and "accuracy" in self.conviction_rates:
            efficiency["conviction_accuracy"] = self.conviction_rates["accuracy"]
        
        # 上诉成功率
        if self.appeal_success_rates and "overall" in self.appeal_success_rates:
            efficiency["appeal_success_rate"] = self.appeal_success_rates["overall"]
        
        return efficiency

    def get_dimensional_legal_differences(self, other_dimension_system):
        """获取与其他维度的法律差异"""
        if not other_dimension_system:
            return {}
        
        differences = {
            "legal_system_compatibility": 0.0,
            "procedure_similarity": 0.0,
            "enforcement_alignment": 0.0,
            "jurisdictional_conflicts": []
        }
        
        # 法律体系兼容性
        if self.legal_system_type == other_dimension_system.legal_system_type:
            differences["legal_system_compatibility"] = 1.0
        else:
            differences["legal_system_compatibility"] = 0.5  # 部分兼容
        
        # 程序相似性
        if self.procedure_type == other_dimension_system.procedure_type:
            differences["procedure_similarity"] = 1.0
        else:
            differences["procedure_similarity"] = 0.3
        
        return differences

    def validate_cross_dimensional_case(self, case_data):
        """验证跨维度案件的管辖权"""
        if not self.cross_dimensional_jurisdiction:
            return False
        
        case_type = case_data.get("type")
        involved_dimensions = case_data.get("dimensions", [])
        
        # 检查是否有管辖权
        jurisdiction_rules = self.cross_dimensional_jurisdiction.get("rules", {})
        
        for rule in jurisdiction_rules.get(case_type, []):
            if all(dim in rule.get("applicable_dimensions", []) for dim in involved_dimensions):
                return True
        
        return False

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            "judicial_efficiency": self.calculate_judicial_efficiency(),
            "dimension_id": self.dimension_id,
            "jurisdiction_name": self.jurisdiction_name,
            "legal_system_type": self.legal_system_type,
            "procedure_type": self.procedure_type
        })
        return data
