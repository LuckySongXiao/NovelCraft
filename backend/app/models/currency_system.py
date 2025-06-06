"""
货币体系数据模型
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Dict, Any, List
from enum import Enum

from .base import ProjectBaseModel, TaggedMixin, VersionedMixin


class CurrencyType(str, Enum):
    """货币类型枚举"""
    METAL = "metal"                 # 金属货币
    PAPER = "paper"                 # 纸币
    DIGITAL = "digital"             # 数字货币
    COMMODITY = "commodity"         # 商品货币
    CREDIT = "credit"               # 信用货币
    MAGICAL = "magical"             # 魔法货币
    ENERGY = "energy"               # 能量货币
    OTHER = "other"                 # 其他


class MonetarySystem(str, Enum):
    """货币制度枚举"""
    GOLD_STANDARD = "gold_standard"         # 金本位
    SILVER_STANDARD = "silver_standard"     # 银本位
    BIMETALLIC = "bimetallic"              # 双本位
    FIAT = "fiat"                          # 法定货币
    FLOATING = "floating"                   # 浮动汇率
    FIXED = "fixed"                        # 固定汇率
    MANAGED = "managed"                    # 管理汇率
    OTHER = "other"                        # 其他


class CurrencySystem(ProjectBaseModel, TaggedMixin, VersionedMixin):
    """货币体系模型"""

    __tablename__ = "currency_systems"

    # 基本信息
    monetary_system = Column(SQLEnum(MonetarySystem), default=MonetarySystem.GOLD_STANDARD, comment="货币制度")
    base_currency = Column(String(100), comment="基础货币")

    # 货币种类
    currencies = Column(JSON, comment="货币种类")
    exchange_rates = Column(JSON, comment="汇率体系")
    denominations = Column(JSON, comment="面额体系")

    # 发行机构
    issuing_authority = Column(JSON, comment="发行机构")
    monetary_policy = Column(JSON, comment="货币政策")
    regulation = Column(JSON, comment="监管制度")

    # 经济指标
    inflation_rate = Column(Float, default=0.0, comment="通胀率")
    interest_rate = Column(Float, default=0.0, comment="利率")
    money_supply = Column(JSON, comment="货币供应量")

    # 支付系统
    payment_methods = Column(JSON, comment="支付方式")
    banking_system = Column(JSON, comment="银行体系")
    financial_institutions = Column(JSON, comment="金融机构")

    # 国际贸易
    trade_currencies = Column(JSON, comment="贸易货币")
    foreign_exchange = Column(JSON, comment="外汇市场")
    international_agreements = Column(JSON, comment="国际协议")

    # 历史发展
    currency_history = Column(JSON, comment="货币历史")
    major_reforms = Column(JSON, comment="重大改革")
    economic_crises = Column(JSON, comment="经济危机")

    # 关联关系
    project_id = Column(Integer, ForeignKey("projects.id"), comment="项目ID")
    world_setting_id = Column(Integer, ForeignKey("world_settings.id"), comment="世界设定ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if not self.currencies:
            self.currencies = []
        if not self.exchange_rates:
            self.exchange_rates = {}
        if not self.denominations:
            self.denominations = {}
        if not self.issuing_authority:
            self.issuing_authority = {}
        if not self.monetary_policy:
            self.monetary_policy = {}
        if not self.regulation:
            self.regulation = {}
        if not self.money_supply:
            self.money_supply = {}
        if not self.payment_methods:
            self.payment_methods = []
        if not self.banking_system:
            self.banking_system = {}
        if not self.financial_institutions:
            self.financial_institutions = []
        if not self.trade_currencies:
            self.trade_currencies = []
        if not self.foreign_exchange:
            self.foreign_exchange = {}
        if not self.international_agreements:
            self.international_agreements = []
        if not self.currency_history:
            self.currency_history = []
        if not self.major_reforms:
            self.major_reforms = []
        if not self.economic_crises:
            self.economic_crises = []

    def add_currency(self, currency_data: Dict[str, Any]):
        """添加货币"""
        self.currencies.append(currency_data)

    def add_payment_method(self, payment_data: Dict[str, Any]):
        """添加支付方式"""
        self.payment_methods.append(payment_data)

    def add_financial_institution(self, institution_data: Dict[str, Any]):
        """添加金融机构"""
        self.financial_institutions.append(institution_data)

    def add_historical_event(self, event_data: Dict[str, Any]):
        """添加历史事件"""
        self.currency_history.append(event_data)
        # 按时间排序
        self.currency_history.sort(key=lambda x: x.get("time", 0))

    def set_exchange_rate(self, from_currency: str, to_currency: str, rate: float):
        """设置汇率"""
        if from_currency not in self.exchange_rates:
            self.exchange_rates[from_currency] = {}
        self.exchange_rates[from_currency][to_currency] = rate

    def get_currency_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取货币"""
        for currency in self.currencies:
            if currency.get("name") == name:
                return currency
        return None

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """获取汇率"""
        if from_currency in self.exchange_rates:
            return self.exchange_rates[from_currency].get(to_currency, 0.0)
        return 0.0

    def calculate_currency_value(self, amount: float, currency: str, target_currency: str) -> float:
        """计算货币价值转换"""
        if currency == target_currency:
            return amount

        rate = self.get_exchange_rate(currency, target_currency)
        if rate > 0:
            return amount * rate

        # 尝试反向汇率
        reverse_rate = self.get_exchange_rate(target_currency, currency)
        if reverse_rate > 0:
            return amount / reverse_rate

        return 0.0

    def calculate_economic_stability(self) -> float:
        """计算经济稳定性"""
        score = 50.0  # 基础分数

        # 通胀率影响
        inflation_rate = self.inflation_rate or 0.0
        if abs(inflation_rate) < 2:
            score += 20
        elif abs(inflation_rate) < 5:
            score += 10
        else:
            score -= 10

        # 货币制度稳定性
        if self.monetary_system in [MonetarySystem.GOLD_STANDARD, MonetarySystem.FIAT]:
            score += 15

        # 金融机构数量
        score += len(self.financial_institutions) * 2

        # 支付方式多样性
        score += len(self.payment_methods) * 3

        return min(100.0, max(0.0, score))

    def validate_consistency(self) -> List[str]:
        """验证货币体系一致性"""
        issues = []

        # 检查基础货币是否在货币列表中
        if self.base_currency:
            base_found = any(c.get("name") == self.base_currency for c in self.currencies)
            if not base_found:
                issues.append(f"基础货币 '{self.base_currency}' 未在货币列表中定义")

        # 检查汇率的对称性
        for from_curr, rates in self.exchange_rates.items():
            for to_curr, rate in rates.items():
                reverse_rate = self.get_exchange_rate(to_curr, from_curr)
                if reverse_rate > 0:
                    expected_reverse = 1.0 / rate
                    if abs(reverse_rate - expected_reverse) > 0.01:
                        issues.append(f"汇率不对称: {from_curr}->{to_curr} 与 {to_curr}->{from_curr}")

        # 检查通胀率合理性
        inflation_rate = self.inflation_rate or 0.0
        if abs(inflation_rate) > 50:
            issues.append("通胀率过高，可能导致经济不稳定")

        return issues

    def generate_summary(self) -> str:
        """生成货币体系摘要"""
        summary_parts = []

        if self.description:
            summary_parts.append(self.description)

        # 货币制度
        system_map = {
            MonetarySystem.GOLD_STANDARD: "金本位",
            MonetarySystem.SILVER_STANDARD: "银本位",
            MonetarySystem.BIMETALLIC: "双本位",
            MonetarySystem.FIAT: "法定货币",
            MonetarySystem.FLOATING: "浮动汇率",
            MonetarySystem.FIXED: "固定汇率",
            MonetarySystem.MANAGED: "管理汇率",
            MonetarySystem.OTHER: "其他"
        }
        summary_parts.append(f"货币制度: {system_map.get(self.monetary_system, '未知')}")

        # 基础货币
        if self.base_currency:
            summary_parts.append(f"基础货币: {self.base_currency}")

        # 货币数量
        summary_parts.append(f"货币种类: {len(self.currencies)}种")

        # 经济稳定性
        stability = self.calculate_economic_stability()
        summary_parts.append(f"经济稳定性: {stability:.1f}/100")

        return " | ".join(summary_parts)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = super().to_dict()
        result["summary"] = self.generate_summary()
        result["economic_stability"] = self.calculate_economic_stability()
        result["consistency_issues"] = self.validate_consistency()
        result["tags"] = self.get_tags()
        return result
