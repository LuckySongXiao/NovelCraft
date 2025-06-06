"""
职业体系模型
"""
from sqlalchemy import Column, Integer, String, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class ProfessionCategory(str, Enum):
    """职业类别枚举"""
    COMBAT = "combat"  # 战斗类
    CRAFTING = "crafting"  # 制作类
    SCHOLARLY = "scholarly"  # 学术类
    MERCANTILE = "mercantile"  # 商业类
    AGRICULTURAL = "agricultural"  # 农业类
    ARTISTIC = "artistic"  # 艺术类
    RELIGIOUS = "religious"  # 宗教类
    ADMINISTRATIVE = "administrative"  # 行政类
    MEDICAL = "medical"  # 医疗类
    MAGICAL = "magical"  # 魔法类
    TECHNICAL = "technical"  # 技术类
    SERVICE = "service"  # 服务类


class SkillLevel(str, Enum):
    """技能等级枚举"""
    NOVICE = "novice"  # 新手
    APPRENTICE = "apprentice"  # 学徒
    JOURNEYMAN = "journeyman"  # 熟练工
    EXPERT = "expert"  # 专家
    MASTER = "master"  # 大师
    GRANDMASTER = "grandmaster"  # 宗师


class CareerPath(str, Enum):
    """职业发展路径枚举"""
    LINEAR = "linear"  # 线性发展
    BRANCHING = "branching"  # 分支发展
    CIRCULAR = "circular"  # 循环发展
    HYBRID = "hybrid"  # 混合发展


class ProfessionSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """职业体系模型"""

    __tablename__ = "profession_systems"

    # 基本信息
    dimension_id = Column(Integer, comment="维度ID")
    economic_context = Column(String(200), comment="经济背景")
    
    # 职业分类
    profession_categories = Column(JSON, comment="职业分类")
    profession_hierarchy = Column(JSON, comment="职业等级")
    profession_relationships = Column(JSON, comment="职业关系")
    
    # 技能体系
    skill_framework = Column(JSON, comment="技能框架")
    skill_requirements = Column(JSON, comment="技能要求")
    skill_development = Column(JSON, comment="技能发展")
    
    # 晋升路径
    career_paths = Column(JSON, comment="职业发展路径")
    promotion_criteria = Column(JSON, comment="晋升标准")
    advancement_barriers = Column(JSON, comment="晋升障碍")
    
    # 行业组织
    professional_organizations = Column(JSON, comment="行业组织")
    guilds = Column(JSON, comment="公会组织")
    unions = Column(JSON, comment="工会组织")
    
    # 教育培训
    training_systems = Column(JSON, comment="培训体系")
    apprenticeship_programs = Column(JSON, comment="学徒制度")
    certification_systems = Column(JSON, comment="认证体系")
    
    # 薪酬福利
    compensation_structure = Column(JSON, comment="薪酬结构")
    benefit_systems = Column(JSON, comment="福利制度")
    economic_incentives = Column(JSON, comment="经济激励")
    
    # 工作环境
    working_conditions = Column(JSON, comment="工作条件")
    workplace_culture = Column(JSON, comment="职场文化")
    safety_standards = Column(JSON, comment="安全标准")
    
    # 职业流动性
    mobility_patterns = Column(JSON, comment="流动模式")
    career_transitions = Column(JSON, comment="职业转换")
    social_mobility = Column(JSON, comment="社会流动")
    
    # 专业伦理
    professional_ethics = Column(JSON, comment="职业伦理")
    codes_of_conduct = Column(JSON, comment="行为准则")
    disciplinary_measures = Column(JSON, comment="纪律措施")
    
    # 技术创新
    technological_impact = Column(JSON, comment="技术影响")
    innovation_trends = Column(JSON, comment="创新趋势")
    future_skills = Column(JSON, comment="未来技能")
    
    # 维度特性
    dimensional_professions = Column(JSON, comment="维度特有职业")
    cross_dimensional_careers = Column(JSON, comment="跨维度职业")
    dimensional_skill_transfer = Column(JSON, comment="维度技能转移")
    
    # 市场需求
    labor_market = Column(JSON, comment="劳动力市场")
    demand_trends = Column(JSON, comment="需求趋势")
    supply_analysis = Column(JSON, comment="供给分析")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.profession_categories:
            self.profession_categories = {
                "categories": [],
                "distribution": {},
                "characteristics": {}
            }
        
        if not self.skill_framework:
            self.skill_framework = {
                "core_skills": [],
                "specialized_skills": [],
                "soft_skills": []
            }
        
        if not self.career_paths:
            self.career_paths = {
                "paths": [],
                "requirements": {},
                "timelines": {}
            }
        
        if not self.professional_organizations:
            self.professional_organizations = {
                "guilds": [],
                "associations": [],
                "unions": []
            }

    def add_profession(self, profession_data):
        """添加职业"""
        if not self.profession_categories:
            self.profession_categories = {"categories": [], "distribution": {}, "characteristics": {}}
        
        category = profession_data.get("category", "service")
        if category not in self.profession_categories["categories"]:
            self.profession_categories["categories"].append({
                "name": category,
                "professions": []
            })
        
        # 找到对应类别并添加职业
        for cat in self.profession_categories["categories"]:
            if cat["name"] == category:
                cat["professions"].append(profession_data)
                break
        
        return True

    def add_skill_requirement(self, profession_name, skill_data):
        """为职业添加技能要求"""
        if not self.skill_requirements:
            self.skill_requirements = {}
        
        if profession_name not in self.skill_requirements:
            self.skill_requirements[profession_name] = {
                "required_skills": [],
                "preferred_skills": [],
                "skill_levels": {}
            }
        
        self.skill_requirements[profession_name]["required_skills"].append(skill_data)
        return True

    def add_career_path(self, path_data):
        """添加职业发展路径"""
        if not self.career_paths:
            self.career_paths = {"paths": [], "requirements": {}, "timelines": {}}
        
        self.career_paths["paths"].append(path_data)
        return True

    def add_professional_organization(self, org_data):
        """添加行业组织"""
        if not self.professional_organizations:
            self.professional_organizations = {"guilds": [], "associations": [], "unions": []}
        
        org_type = org_data.get("type", "associations")
        if org_type in self.professional_organizations:
            self.professional_organizations[org_type].append(org_data)
        return True

    def calculate_profession_metrics(self):
        """计算职业体系指标"""
        metrics = {
            "profession_diversity": 0.0,
            "skill_complexity": 0.0,
            "career_mobility": 0.0,
            "organization_coverage": 0.0
        }
        
        # 职业多样性
        if self.profession_categories and "categories" in self.profession_categories:
            total_professions = sum(len(cat.get("professions", [])) for cat in self.profession_categories["categories"])
            metrics["profession_diversity"] = min(100, total_professions * 2)
        
        # 技能复杂性
        if self.skill_framework:
            total_skills = sum(len(skills) for skills in self.skill_framework.values() if isinstance(skills, list))
            metrics["skill_complexity"] = min(100, total_skills * 3)
        
        # 职业流动性
        if self.career_paths and "paths" in self.career_paths:
            path_count = len(self.career_paths["paths"])
            metrics["career_mobility"] = min(100, path_count * 10)
        
        # 组织覆盖率
        if self.professional_organizations:
            total_orgs = sum(len(orgs) for orgs in self.professional_organizations.values() if isinstance(orgs, list))
            metrics["organization_coverage"] = min(100, total_orgs * 5)
        
        return metrics

    def get_dimensional_profession_analysis(self, other_dimension_system):
        """获取与其他维度的职业分析"""
        if not other_dimension_system:
            return {}
        
        analysis = {
            "profession_overlap": 0.0,
            "skill_transferability": 0.0,
            "career_compatibility": 0.0,
            "unique_professions": []
        }
        
        # 职业重叠度
        if (self.profession_categories and other_dimension_system.profession_categories and
            "categories" in self.profession_categories and "categories" in other_dimension_system.profession_categories):
            
            self_professions = set()
            other_professions = set()
            
            for cat in self.profession_categories["categories"]:
                for prof in cat.get("professions", []):
                    self_professions.add(prof.get("name", ""))
            
            for cat in other_dimension_system.profession_categories["categories"]:
                for prof in cat.get("professions", []):
                    other_professions.add(prof.get("name", ""))
            
            if self_professions or other_professions:
                intersection = len(self_professions & other_professions)
                union = len(self_professions | other_professions)
                analysis["profession_overlap"] = intersection / union if union > 0 else 0
                analysis["unique_professions"] = list(self_professions - other_professions)
        
        return analysis

    def validate_career_transition(self, from_profession, to_profession):
        """验证职业转换的可行性"""
        if not self.career_paths or "paths" not in self.career_paths:
            return False
        
        for path in self.career_paths["paths"]:
            if (path.get("from") == from_profession and 
                path.get("to") == to_profession):
                return True
        
        return False

    def get_skill_gap_analysis(self, target_profession):
        """获取目标职业的技能差距分析"""
        if not self.skill_requirements or target_profession not in self.skill_requirements:
            return {}
        
        required_skills = self.skill_requirements[target_profession].get("required_skills", [])
        
        gap_analysis = {
            "total_skills_required": len(required_skills),
            "skill_categories": {},
            "difficulty_levels": {},
            "training_recommendations": []
        }
        
        for skill in required_skills:
            category = skill.get("category", "general")
            level = skill.get("level", "novice")
            
            if category not in gap_analysis["skill_categories"]:
                gap_analysis["skill_categories"][category] = 0
            gap_analysis["skill_categories"][category] += 1
            
            if level not in gap_analysis["difficulty_levels"]:
                gap_analysis["difficulty_levels"][level] = 0
            gap_analysis["difficulty_levels"][level] += 1
        
        return gap_analysis

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            "profession_metrics": self.calculate_profession_metrics(),
            "dimension_id": self.dimension_id,
            "economic_context": self.economic_context
        })
        return data
