"""
生民体系模型
"""
from sqlalchemy import Column, Integer, String, Text, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class SocialClass(str, Enum):
    """社会阶层枚举"""
    NOBILITY = "nobility"  # 贵族
    MERCHANT = "merchant"  # 商人
    ARTISAN = "artisan"  # 工匠
    FARMER = "farmer"  # 农民
    LABORER = "laborer"  # 劳工
    SLAVE = "slave"  # 奴隶
    CLERGY = "clergy"  # 神职人员
    SCHOLAR = "scholar"  # 学者
    WARRIOR = "warrior"  # 武士
    OTHER = "other"  # 其他


class LifestyleType(str, Enum):
    """生活方式类型枚举"""
    URBAN = "urban"  # 城市生活
    RURAL = "rural"  # 乡村生活
    NOMADIC = "nomadic"  # 游牧生活
    TRIBAL = "tribal"  # 部落生活
    MONASTIC = "monastic"  # 修道生活
    MILITARY = "military"  # 军事生活
    MERCHANT = "merchant"  # 商旅生活
    SCHOLARLY = "scholarly"  # 学者生活


class CivilianSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """生民体系模型"""

    __tablename__ = "civilian_systems"

    # 基本信息
    dimension_id = Column(Integer, comment="维度ID")
    region_name = Column(String(200), comment="区域名称")
    
    # 人口统计
    total_population = Column(Integer, default=0, comment="总人口")
    population_density = Column(Float, default=0.0, comment="人口密度")
    population_growth_rate = Column(Float, default=0.0, comment="人口增长率")
    age_distribution = Column(JSON, comment="年龄分布")
    gender_distribution = Column(JSON, comment="性别分布")
    
    # 社会阶层
    social_classes = Column(JSON, comment="社会阶层结构")
    class_mobility = Column(JSON, comment="阶层流动性")
    social_hierarchy = Column(JSON, comment="社会等级制度")
    
    # 生活方式
    lifestyle_types = Column(JSON, comment="生活方式类型")
    living_conditions = Column(JSON, comment="生活条件")
    daily_routines = Column(JSON, comment="日常作息")
    
    # 文化习俗
    cultural_practices = Column(JSON, comment="文化习俗")
    traditions = Column(JSON, comment="传统节日")
    customs = Column(JSON, comment="风俗习惯")
    languages = Column(JSON, comment="语言文字")
    
    # 教育体系
    education_system = Column(JSON, comment="教育制度")
    literacy_rate = Column(Float, default=0.0, comment="识字率")
    educational_institutions = Column(JSON, comment="教育机构")
    
    # 宗教信仰
    religious_beliefs = Column(JSON, comment="宗教信仰")
    religious_practices = Column(JSON, comment="宗教仪式")
    religious_institutions = Column(JSON, comment="宗教机构")
    
    # 社会保障
    welfare_system = Column(JSON, comment="社会保障制度")
    healthcare_system = Column(JSON, comment="医疗保健体系")
    social_services = Column(JSON, comment="社会服务")
    
    # 家庭结构
    family_structure = Column(JSON, comment="家庭结构")
    marriage_customs = Column(JSON, comment="婚姻习俗")
    inheritance_rules = Column(JSON, comment="继承规则")
    
    # 社会问题
    social_issues = Column(JSON, comment="社会问题")
    crime_rates = Column(JSON, comment="犯罪率统计")
    social_conflicts = Column(JSON, comment="社会冲突")
    
    # 维度特性
    dimensional_traits = Column(JSON, comment="维度特有特征")
    cross_dimensional_relations = Column(JSON, comment="跨维度关系")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.social_classes:
            self.social_classes = {
                "classes": [],
                "distribution": {},
                "characteristics": {}
            }
        
        if not self.lifestyle_types:
            self.lifestyle_types = {
                "types": [],
                "distribution": {},
                "characteristics": {}
            }
        
        if not self.cultural_practices:
            self.cultural_practices = {
                "festivals": [],
                "ceremonies": [],
                "traditions": []
            }
        
        if not self.age_distribution:
            self.age_distribution = {
                "children": 0,
                "adults": 0,
                "elderly": 0
            }
        
        if not self.gender_distribution:
            self.gender_distribution = {
                "male": 50,
                "female": 50,
                "other": 0
            }

    def add_social_class(self, class_data):
        """添加社会阶层"""
        if not self.social_classes:
            self.social_classes = {"classes": [], "distribution": {}, "characteristics": {}}
        
        self.social_classes["classes"].append(class_data)
        return True

    def add_lifestyle_type(self, lifestyle_data):
        """添加生活方式"""
        if not self.lifestyle_types:
            self.lifestyle_types = {"types": [], "distribution": {}, "characteristics": {}}
        
        self.lifestyle_types["types"].append(lifestyle_data)
        return True

    def add_cultural_practice(self, practice_data):
        """添加文化习俗"""
        if not self.cultural_practices:
            self.cultural_practices = {"festivals": [], "ceremonies": [], "traditions": []}
        
        practice_type = practice_data.get("type", "traditions")
        if practice_type in self.cultural_practices:
            self.cultural_practices[practice_type].append(practice_data)
        return True

    def update_population_stats(self, stats_data):
        """更新人口统计"""
        if "total_population" in stats_data:
            self.total_population = stats_data["total_population"]
        if "population_density" in stats_data:
            self.population_density = stats_data["population_density"]
        if "growth_rate" in stats_data:
            self.population_growth_rate = stats_data["growth_rate"]
        if "age_distribution" in stats_data:
            self.age_distribution = stats_data["age_distribution"]
        if "gender_distribution" in stats_data:
            self.gender_distribution = stats_data["gender_distribution"]
        return True

    def calculate_social_metrics(self):
        """计算社会指标"""
        metrics = {
            "social_stability": 0.0,
            "cultural_diversity": 0.0,
            "education_level": self.literacy_rate or 0.0,
            "living_standard": 0.0
        }
        
        # 计算社会稳定性
        if self.social_issues and "conflicts" in self.social_issues:
            conflict_count = len(self.social_issues["conflicts"])
            metrics["social_stability"] = max(0, 100 - conflict_count * 10)
        else:
            metrics["social_stability"] = 80.0
        
        # 计算文化多样性
        if self.cultural_practices:
            practice_count = sum(len(practices) for practices in self.cultural_practices.values())
            metrics["cultural_diversity"] = min(100, practice_count * 5)
        
        return metrics

    def get_dimensional_comparison(self, other_dimension_system):
        """获取与其他维度的比较"""
        if not other_dimension_system:
            return {}
        
        comparison = {
            "population_ratio": 0.0,
            "cultural_similarity": 0.0,
            "social_structure_similarity": 0.0,
            "lifestyle_similarity": 0.0
        }
        
        # 人口比较
        if self.total_population and other_dimension_system.total_population:
            comparison["population_ratio"] = self.total_population / other_dimension_system.total_population
        
        # 文化相似性比较（简化算法）
        if self.cultural_practices and other_dimension_system.cultural_practices:
            self_practices = set(str(p) for practices in self.cultural_practices.values() for p in practices)
            other_practices = set(str(p) for practices in other_dimension_system.cultural_practices.values() for p in practices)
            if self_practices or other_practices:
                intersection = len(self_practices & other_practices)
                union = len(self_practices | other_practices)
                comparison["cultural_similarity"] = intersection / union if union > 0 else 0
        
        return comparison

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            "social_metrics": self.calculate_social_metrics(),
            "dimension_id": self.dimension_id,
            "region_name": self.region_name,
            "total_population": self.total_population,
            "population_density": self.population_density,
            "population_growth_rate": self.population_growth_rate
        })
        return data
