#!/usr/bin/env python3
"""
简单测试新增体系模型
"""
import sys
import os

# 添加后端路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """测试模型导入"""
    try:
        from app.models.political_system import PoliticalSystem
        print("✓ 政治体系模型导入成功")
        
        from app.models.currency_system import CurrencySystem
        print("✓ 货币体系模型导入成功")
        
        from app.models.commerce_system import CommerceSystem
        print("✓ 商业体系模型导入成功")
        
        from app.models.race_system import RaceSystem
        print("✓ 种族类别模型导入成功")
        
        from app.models.martial_arts_system import MartialArtsSystem
        print("✓ 功法体系模型导入成功")
        
        return True
    except Exception as e:
        print(f"✗ 模型导入失败: {e}")
        return False

def test_currency_fix():
    """测试货币体系修复"""
    try:
        from app.models.currency_system import CurrencySystem, MonetarySystem
        
        currency_system = CurrencySystem(
            name="测试货币体系",
            monetary_system=MonetarySystem.GOLD_STANDARD,
            base_currency="金币"
        )
        
        # 测试经济稳定性计算
        stability = currency_system.calculate_economic_stability()
        print(f"✓ 经济稳定性计算成功: {stability:.1f}")
        
        return True
    except Exception as e:
        print(f"✗ 货币体系测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始简单测试...")
    
    if test_imports():
        print("所有模型导入成功！")
        
        if test_currency_fix():
            print("货币体系修复成功！")
            print("🎉 新增体系模型测试通过！")
        else:
            print("❌ 货币体系仍有问题")
    else:
        print("❌ 模型导入失败")
