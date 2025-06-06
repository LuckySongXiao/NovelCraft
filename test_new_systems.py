#!/usr/bin/env python3
"""
测试新增体系模型的脚本
"""
import sys
import os
import json

# 添加后端路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_political_system():
    """测试政治体系模型"""
    try:
        from app.models.political_system import PoliticalSystem, GovernmentType, PowerStructure
        
        print("✓ 政治体系模型导入成功")
        
        # 创建测试实例
        political_system = PoliticalSystem(
            name="修仙界政治体系",
            description="修仙世界的政治制度",
            government_type=GovernmentType.MONARCHY,
            power_structure=PowerStructure.CENTRALIZED
        )
        
        # 测试添加机构
        political_system.add_institution({
            "name": "修仙联盟",
            "type": "regulatory",
            "description": "管理修仙者的联盟组织"
        })
        
        # 测试添加法律
        political_system.add_law({
            "name": "修仙者管理法",
            "type": "regulatory",
            "description": "规范修仙者行为的法律"
        })
        
        # 测试计算稳定性
        stability = political_system.calculate_stability_score()
        print(f"✓ 政治稳定性评分: {stability:.1f}")
        
        # 测试一致性验证
        issues = political_system.validate_consistency()
        print(f"✓ 一致性问题: {len(issues)}个")
        
        # 测试生成摘要
        summary = political_system.generate_summary()
        print(f"✓ 政治体系摘要: {summary}")
        
        return True
        
    except Exception as e:
        print(f"✗ 政治体系模型测试失败: {e}")
        return False


def test_currency_system():
    """测试货币体系模型"""
    try:
        from app.models.currency_system import CurrencySystem, MonetarySystem
        
        print("✓ 货币体系模型导入成功")
        
        # 创建测试实例
        currency_system = CurrencySystem(
            name="修仙界货币体系",
            description="修仙世界的货币制度",
            monetary_system=MonetarySystem.GOLD_STANDARD,
            base_currency="灵石"
        )
        
        # 测试添加货币
        currency_system.add_currency({
            "name": "灵石",
            "type": "magical",
            "description": "修仙者使用的主要货币"
        })
        
        # 测试设置汇率
        currency_system.set_exchange_rate("灵石", "金币", 100)
        
        # 测试计算经济稳定性
        stability = currency_system.calculate_economic_stability()
        print(f"✓ 经济稳定性评分: {stability:.1f}")
        
        # 测试一致性验证
        issues = currency_system.validate_consistency()
        print(f"✓ 一致性问题: {len(issues)}个")
        
        # 测试生成摘要
        summary = currency_system.generate_summary()
        print(f"✓ 货币体系摘要: {summary}")
        
        return True
        
    except Exception as e:
        print(f"✗ 货币体系模型测试失败: {e}")
        return False


def test_commerce_system():
    """测试商业体系模型"""
    try:
        from app.models.commerce_system import CommerceSystem, EconomicSystem
        
        print("✓ 商业体系模型导入成功")
        
        # 创建测试实例
        commerce_system = CommerceSystem(
            name="修仙界商业体系",
            description="修仙世界的商业制度",
            economic_system=EconomicSystem.FEUDALISM
        )
        
        # 测试添加贸易路线
        commerce_system.add_trade_route({
            "name": "灵石商路",
            "start_point": "青云宗",
            "end_point": "天剑门",
            "volume": 1000
        })
        
        # 测试添加商会
        commerce_system.add_guild({
            "name": "修仙商会",
            "type": "trade",
            "trade_volume": 5000
        })
        
        # 测试计算经济繁荣度
        prosperity = commerce_system.calculate_economic_prosperity()
        print(f"✓ 经济繁荣度评分: {prosperity:.1f}")
        
        # 测试一致性验证
        issues = commerce_system.validate_consistency()
        print(f"✓ 一致性问题: {len(issues)}个")
        
        # 测试生成摘要
        summary = commerce_system.generate_summary()
        print(f"✓ 商业体系摘要: {summary}")
        
        return True
        
    except Exception as e:
        print(f"✗ 商业体系模型测试失败: {e}")
        return False


def test_race_system():
    """测试种族类别模型"""
    try:
        from app.models.race_system import RaceSystem, RaceType, LifespanCategory
        
        print("✓ 种族类别模型导入成功")
        
        # 创建测试实例
        race_system = RaceSystem(
            name="人族",
            description="修仙世界的人类种族",
            race_type=RaceType.HUMANOID,
            lifespan_category=LifespanCategory.MEDIUM
        )
        
        # 测试添加种族能力
        race_system.add_racial_ability({
            "name": "修炼天赋",
            "description": "天生具备修炼能力",
            "effect": "修炼速度+10%"
        })
        
        # 测试添加特殊天赋
        race_system.add_special_talent({
            "name": "灵根",
            "description": "修炼的根基",
            "rarity": "common"
        })
        
        # 测试计算实力等级
        power = race_system.calculate_power_level()
        print(f"✓ 种族实力等级: {power:.1f}")
        
        # 测试计算文明等级
        civilization = race_system.calculate_civilization_level()
        print(f"✓ 文明等级: {civilization:.1f}")
        
        # 测试一致性验证
        issues = race_system.validate_consistency()
        print(f"✓ 一致性问题: {len(issues)}个")
        
        # 测试生成摘要
        summary = race_system.generate_summary()
        print(f"✓ 种族摘要: {summary}")
        
        return True
        
    except Exception as e:
        print(f"✗ 种族类别模型测试失败: {e}")
        return False


def test_martial_arts_system():
    """测试功法体系模型"""
    try:
        from app.models.martial_arts_system import MartialArtsSystem, TechniqueType, TechniqueGrade
        
        print("✓ 功法体系模型导入成功")
        
        # 创建测试实例
        martial_arts = MartialArtsSystem(
            name="青云心法",
            description="青云宗的基础内功心法",
            technique_type=TechniqueType.INTERNAL,
            technique_grade=TechniqueGrade.INTERMEDIATE,
            power_source="天地灵气",
            offensive_power=60.0,
            defensive_power=70.0,
            utility_value=50.0
        )
        
        # 测试添加招式
        martial_arts.add_technique({
            "name": "青云剑法",
            "type": "sword",
            "description": "青云宗的基础剑法"
        })
        
        # 测试添加修炼阶段
        martial_arts.add_training_stage({
            "level": 1,
            "name": "入门",
            "description": "初学者阶段",
            "requirements": "练气期"
        })
        
        # 测试计算总体威力
        power = martial_arts.calculate_total_power()
        print(f"✓ 功法总体威力: {power:.1f}")
        
        # 测试计算修炼难度
        difficulty = martial_arts.calculate_difficulty()
        print(f"✓ 修炼难度: {difficulty:.1f}")
        
        # 测试一致性验证
        issues = martial_arts.validate_consistency()
        print(f"✓ 一致性问题: {len(issues)}个")
        
        # 测试生成摘要
        summary = martial_arts.generate_summary()
        print(f"✓ 功法摘要: {summary}")
        
        return True
        
    except Exception as e:
        print(f"✗ 功法体系模型测试失败: {e}")
        return False


def test_world_setting_extensions():
    """测试世界设定模型的扩展"""
    try:
        from app.models.world_setting import WorldSetting
        
        print("✓ 世界设定模型导入成功")
        
        # 创建测试实例
        world_setting = WorldSetting(
            name="修仙世界设定",
            description="完整的修仙世界设定"
        )
        
        # 测试新增的货币方法
        world_setting.add_currency({
            "name": "灵石",
            "type": "magical",
            "value": 1
        })
        
        # 测试新增的种族方法
        world_setting.add_race({
            "name": "人族",
            "type": "humanoid",
            "traits": ["修炼天赋"]
        })
        
        # 测试新增的功法方法
        world_setting.add_martial_art({
            "name": "基础心法",
            "type": "internal",
            "grade": "basic"
        })
        
        # 测试获取方法
        currency = world_setting.get_currency_by_name("灵石")
        race = world_setting.get_race_by_name("人族")
        martial_art = world_setting.get_martial_art_by_name("基础心法")
        
        print(f"✓ 货币查询: {currency['name'] if currency else 'None'}")
        print(f"✓ 种族查询: {race['name'] if race else 'None'}")
        print(f"✓ 功法查询: {martial_art['name'] if martial_art else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"✗ 世界设定扩展测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("开始测试新增体系模型...")
    print("=" * 50)
    
    tests = [
        ("政治体系模型", test_political_system),
        ("货币体系模型", test_currency_system),
        ("商业体系模型", test_commerce_system),
        ("种族类别模型", test_race_system),
        ("功法体系模型", test_martial_arts_system),
        ("世界设定扩展", test_world_setting_extensions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n测试 {test_name}:")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"✓ {test_name} 测试通过")
        else:
            print(f"✗ {test_name} 测试失败")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有新增体系模型测试通过！")
        return True
    else:
        print("❌ 部分测试失败，请检查错误信息")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
