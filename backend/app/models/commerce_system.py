"""
商业体系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class EconomicSystem(str, Enum):
    """经济制度枚举"""
    FEUDALISM = "feudalism"         # 封建制
    CAPITALISM = "capitalism"       # 资本主义
    SOCIALISM = "socialism"         # 社会主义
    MERCANTILISM = "mercantilism"   # 重商主义
    MIXED = "mixed"                 # 混合经济
    PLANNED = "planned"             # 计划经济
    MARKET = "market"               # 市场经济
    TRADITIONAL = "traditional"     # 传统经济
    OTHER = "other"                 # 其他


class TradeType(str, Enum):
    """贸易类型枚举"""
    DOMESTIC = "domestic"           # 国内贸易
    INTERNATIONAL = "international" # 国际贸易
    REGIONAL = "regional"           # 区域贸易
    MARITIME = "maritime"           # 海上贸易
    OVERLAND = "overland"           # 陆上贸易
    MAGICAL = "magical"             # 魔法贸易
    OTHER = "other"                 # 其他


class CommerceSystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """商业体系模型"""

    __tablename__ = "commerce_systems"

    # 基本信息
    economic_system = Column(SQLEnum(EconomicSystem), default=EconomicSystem.FEUDALISM, comment="经济制度")
    market_structure = Column(String(100), comment="市场结构")
    
    # 贸易体系
    trade_routes = Column(JSON, comment="贸易路线")
    trade_agreements = Column(JSON, comment="贸易协议")
    trade_regulations = Column(JSON, comment="贸易法规")
    
    # 商品与服务
    commodities = Column(JSON, comment="商品分类")
    services = Column(JSON, comment="服务行业")
    luxury_goods = Column(JSON, comment="奢侈品")
    
    # 商业组织
    guilds = Column(JSON, comment="商会公会")
    trading_companies = Column(JSON, comment="贸易公司")
    merchants = Column(JSON, comment="商人组织")
    
    # 市场机制
    pricing_mechanisms = Column(JSON, comment="定价机制")
    supply_demand = Column(JSON, comment="供需关系")
    market_competition = Column(JSON, comment="市场竞争")
    
    # 税收制度
    taxation_system = Column(JSON, comment="税收制度")
    tariffs = Column(JSON, comment="关税体系")
    trade_taxes = Column(JSON, comment="贸易税")
    
    # 金融服务
    banking_services = Column(JSON, comment="银行服务")
    credit_system = Column(JSON, comment="信贷体系")
    insurance = Column(JSON, comment="保险制度")
    
    # 基础设施
    transportation = Column(JSON, comment="运输体系")
    communication = Column(JSON, comment="通信网络")
    storage_facilities = Column(JSON, comment="仓储设施")
    
    # 法律框架
    commercial_law = Column(JSON, comment="商法体系")
    contract_enforcement = Column(JSON, comment="合同执行")
    dispute_resolution = Column(JSON, comment="争议解决")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.trade_routes:
            self.trade_routes = []
        if not self.trade_agreements:
            self.trade_agreements = []
        if not self.trade_regulations:
            self.trade_regulations = {}
        if not self.commodities:
            self.commodities = {}
        if not self.services:
            self.services = []
        if not self.luxury_goods:
            self.luxury_goods = []
        if not self.guilds:
            self.guilds = []
        if not self.trading_companies:
            self.trading_companies = []
        if not self.merchants:
            self.merchants = []
        if not self.pricing_mechanisms:
            self.pricing_mechanisms = {}
        if not self.supply_demand:
            self.supply_demand = {}
        if not self.market_competition:
            self.market_competition = {}
        if not self.taxation_system:
            self.taxation_system = {}
        if not self.tariffs:
            self.tariffs = {}
        if not self.trade_taxes:
            self.trade_taxes = {}
        if not self.banking_services:
            self.banking_services = []
        if not self.credit_system:
            self.credit_system = {}
        if not self.insurance:
            self.insurance = {}
        if not self.transportation:
            self.transportation = {}
        if not self.communication:
            self.communication = {}
        if not self.storage_facilities:
            self.storage_facilities = []
        if not self.commercial_law:
            self.commercial_law = {}
        if not self.contract_enforcement:
            self.contract_enforcement = {}
        if not self.dispute_resolution:
            self.dispute_resolution = {}

    def add_trade_route(self, route_data: Dict[str, Any]):
        """添加贸易路线"""
        self.trade_routes.append(route_data)

    def add_guild(self, guild_data: Dict[str, Any]):
        """添加商会公会"""
        self.guilds.append(guild_data)

    def add_trading_company(self, company_data: Dict[str, Any]):
        """添加贸易公司"""
        self.trading_companies.append(company_data)

    def add_commodity(self, category: str, commodity_data: Dict[str, Any]):
        """添加商品"""
        if category not in self.commodities:
            self.commodities[category] = []
        self.commodities[category].append(commodity_data)

    def add_service(self, service_data: Dict[str, Any]):
        """添加服务"""
        self.services.append(service_data)

    def set_tax_rate(self, tax_type: str, rate: float):
        """设置税率"""
        if "rates" not in self.taxation_system:
            self.taxation_system["rates"] = {}
        self.taxation_system["rates"][tax_type] = rate

    def get_trade_route_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取贸易路线"""
        for route in self.trade_routes:
            if route.get("name") == name:
                return route
        return None

    def get_guild_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取商会"""
        for guild in self.guilds:
            if guild.get("name") == name:
                return guild
        return None

    def get_commodities_by_category(self, category: str) -> List[Dict[str, Any]]:
        """根据分类获取商品"""
        return self.commodities.get(category, [])

    def calculate_trade_volume(self) -> float:
        """计算贸易总量"""
        volume = 0.0
        
        # 贸易路线贡献
        for route in self.trade_routes:
            volume += route.get("volume", 0.0)
        
        # 商会贡献
        for guild in self.guilds:
            volume += guild.get("trade_volume", 0.0)
        
        # 贸易公司贡献
        for company in self.trading_companies:
            volume += company.get("annual_volume", 0.0)
        
        return volume

    def calculate_economic_prosperity(self) -> float:
        """计算经济繁荣度"""
        score = 50.0  # 基础分数
        
        # 贸易路线数量
        score += len(self.trade_routes) * 5
        
        # 商会数量
        score += len(self.guilds) * 3
        
        # 贸易公司数量
        score += len(self.trading_companies) * 4
        
        # 商品种类
        total_commodities = sum(len(items) for items in self.commodities.values())
        score += total_commodities * 2
        
        # 服务种类
        score += len(self.services) * 2
        
        # 基础设施完善度
        if self.transportation:
            score += len(self.transportation) * 3
        
        return min(100.0, max(0.0, score))

    def validate_consistency(self) -> List[str]:
        """验证商业体系一致性"""
        issues = []
        
        # 检查经济制度与市场结构的一致性
        if self.economic_system == EconomicSystem.PLANNED and "free_market" in str(self.market_structure):
            issues.append("计划经济与自由市场结构存在矛盾")
        
        # 检查贸易路线的连通性
        for route in self.trade_routes:
            start = route.get("start_point")
            end = route.get("end_point")
            if start == end:
                issues.append(f"贸易路线 '{route.get('name', '未知')}' 起点和终点相同")
        
        # 检查税率合理性
        if "rates" in self.taxation_system:
            for tax_type, rate in self.taxation_system["rates"].items():
                if rate < 0 or rate > 100:
                    issues.append(f"税率 '{tax_type}' 设置不合理: {rate}%")
        
        return issues

    def generate_summary(self) -> str:
        """生成商业体系摘要"""
        summary_parts = []
        
        if self.description:
            summary_parts.append(self.description)
        
        # 经济制度
        system_map = {
            EconomicSystem.FEUDALISM: "封建制",
            EconomicSystem.CAPITALISM: "资本主义",
            EconomicSystem.SOCIALISM: "社会主义",
            EconomicSystem.MERCANTILISM: "重商主义",
            EconomicSystem.MIXED: "混合经济",
            EconomicSystem.PLANNED: "计划经济",
            EconomicSystem.MARKET: "市场经济",
            EconomicSystem.TRADITIONAL: "传统经济",
            EconomicSystem.OTHER: "其他"
        }
        summary_parts.append(f"经济制度: {system_map.get(self.economic_system, '未知')}")
        
        # 贸易路线数量
        summary_parts.append(f"贸易路线: {len(self.trade_routes)}条")
        
        # 商会数量
        summary_parts.append(f"商会公会: {len(self.guilds)}个")
        
        # 经济繁荣度
        prosperity = self.calculate_economic_prosperity()
        summary_parts.append(f"经济繁荣度: {prosperity:.1f}/100")
        
        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["trade_volume"] = self.calculate_trade_volume()
        result["economic_prosperity"] = self.calculate_economic_prosperity()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
