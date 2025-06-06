#!/usr/bin/env python3
"""
测试新增体系模型的完整功能脚本
生民体系、司法体系、职业体系
"""
import sys
import os
import json

# 添加后端路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_civilian_system():
    """测试生民体系模型"""
    try:
        from app.models.civilian_system import CivilianSystem, SocialClass, LifestyleType
        
        print("✓ 生民体系模型导入成功")
        
        # 创建测试实例
        civilian_system = CivilianSystem(
            name="修仙界生民体系",
            description="修仙世界的生民社会结构",
            dimension_id=1,
            region_name="青云大陆",
            total_population=1000000,
            population_density=50.5,
            population_growth_rate=2.1,
            literacy_rate=65.0
        )
        
        # 测试添加社会阶层
        civilian_system.add_social_class({
            "name": "修仙者",
            "class_type": "warrior",
            "population_percentage": 5.0,
            "characteristics": {"special_abilities": True, "longevity": True}
        })
        
        # 测试添加生活方式
        civilian_system.add_lifestyle_type({
            "name": "修道生活",
            "lifestyle_type": "monastic",
            "description": "专注于修炼的生活方式"
        })
        
        # 测试添加文化习俗
        civilian_system.add_cultural_practice({
            "name": "飞升大典",
            "type": "festivals",
            "description": "庆祝修仙者飞升的节日"
        })
        
        # 测试更新人口统计
        civilian_system.update_population_stats({
            "total_population": 1200000,
            "age_distribution": {"children": 20, "adults": 65, "elderly": 15}
        })
        
        # 测试计算社会指标
        metrics = civilian_system.calculate_social_metrics()
        print(f"✓ 社会指标计算成功: {metrics}")
        
        # 测试转换为字典
        data = civilian_system.to_dict()
        print(f"✓ 生民体系数据转换成功，包含 {len(data)} 个字段")
        
        return True
        
    except Exception as e:
        print(f"✗ 生民体系模型测试失败: {e}")
        return False

def test_judicial_system():
    """测试司法体系模型"""
    try:
        from app.models.judicial_system import JudicialSystem, CourtType, LegalSystem, TrialProcedure
        
        print("✓ 司法体系模型导入成功")
        
        # 创建测试实例
        judicial_system = JudicialSystem(
            name="修仙界司法体系",
            description="修仙世界的法律制度",
            dimension_id=1,
            jurisdiction_name="青云法域",
            legal_system_type=LegalSystem.MIXED_SYSTEM,
            procedure_type=TrialProcedure.MIXED
        )
        
        # 测试添加法院
        judicial_system.add_court({
            "name": "青云最高法院",
            "court_type": "supreme",
            "jurisdiction": "全域",
            "level": 1
        })
        
        # 测试添加法律条文
        judicial_system.add_legal_code({
            "title": "修仙者管理法",
            "type": "criminal",
            "content": "规范修仙者行为的基本法律"
        })
        
        # 测试添加执法机构
        judicial_system.add_enforcement_agency({
            "name": "修仙监察司",
            "type": "specialized",
            "jurisdiction": "修仙者事务"
        })
        
        # 测试添加司法人员
        judicial_system.add_judicial_personnel({
            "name": "张法官",
            "type": "judges",
            "position": "首席法官"
        })
        
        # 测试计算司法效率
        efficiency = judicial_system.calculate_judicial_efficiency()
        print(f"✓ 司法效率计算成功: {efficiency}")
        
        # 测试转换为字典
        data = judicial_system.to_dict()
        print(f"✓ 司法体系数据转换成功，包含 {len(data)} 个字段")
        
        return True
        
    except Exception as e:
        print(f"✗ 司法体系模型测试失败: {e}")
        return False

def test_profession_system():
    """测试职业体系模型"""
    try:
        from app.models.profession_system import ProfessionSystem, ProfessionCategory, SkillLevel, CareerPath
        
        print("✓ 职业体系模型导入成功")
        
        # 创建测试实例
        profession_system = ProfessionSystem(
            name="修仙界职业体系",
            description="修仙世界的职业结构",
            dimension_id=1,
            economic_context="修仙经济体系"
        )
        
        # 测试添加职业
        profession_system.add_profession({
            "name": "炼丹师",
            "category": "crafting",
            "description": "专门炼制丹药的职业"
        })
        
        # 测试添加技能要求
        profession_system.add_skill_requirement("炼丹师", {
            "name": "火候控制",
            "category": "technical",
            "level": "expert"
        })
        
        # 测试添加职业发展路径
        profession_system.add_career_path({
            "name": "炼丹师进阶路径",
            "path_type": "linear",
            "from_profession": "学徒炼丹师",
            "to_profession": "大师炼丹师"
        })
        
        # 测试添加行业组织
        profession_system.add_professional_organization({
            "name": "炼丹师公会",
            "type": "guilds",
            "professions": ["炼丹师", "药师"]
        })
        
        # 测试计算职业指标
        metrics = profession_system.calculate_profession_metrics()
        print(f"✓ 职业指标计算成功: {metrics}")
        
        # 测试验证职业转换
        is_valid = profession_system.validate_career_transition("学徒炼丹师", "大师炼丹师")
        print(f"✓ 职业转换验证: {is_valid}")
        
        # 测试技能差距分析
        gap_analysis = profession_system.get_skill_gap_analysis("炼丹师")
        print(f"✓ 技能差距分析成功: {gap_analysis}")
        
        # 测试转换为字典
        data = profession_system.to_dict()
        print(f"✓ 职业体系数据转换成功，包含 {len(data)} 个字段")
        
        return True
        
    except Exception as e:
        print(f"✗ 职业体系模型测试失败: {e}")
        return False

def test_dimensional_features():
    """测试维度特性功能"""
    try:
        from app.models.civilian_system import CivilianSystem
        from app.models.judicial_system import JudicialSystem
        from app.models.profession_system import ProfessionSystem
        
        print("✓ 开始测试维度特性功能")
        
        # 创建两个不同维度的生民体系
        civilian1 = CivilianSystem(
            name="主维度生民体系",
            dimension_id=1,
            total_population=1000000
        )
        
        civilian2 = CivilianSystem(
            name="次维度生民体系", 
            dimension_id=2,
            total_population=500000
        )
        
        # 测试维度比较
        comparison = civilian1.get_dimensional_comparison(civilian2)
        print(f"✓ 维度比较功能测试成功: {comparison}")
        
        # 创建两个不同维度的司法体系
        judicial1 = JudicialSystem(
            name="主维度司法体系",
            dimension_id=1,
            legal_system_type="civil_law"
        )
        
        judicial2 = JudicialSystem(
            name="次维度司法体系",
            dimension_id=2,
            legal_system_type="common_law"
        )
        
        # 测试法律差异分析
        differences = judicial1.get_dimensional_legal_differences(judicial2)
        print(f"✓ 维度法律差异分析成功: {differences}")
        
        # 创建两个不同维度的职业体系
        profession1 = ProfessionSystem(
            name="主维度职业体系",
            dimension_id=1
        )
        
        profession2 = ProfessionSystem(
            name="次维度职业体系",
            dimension_id=2
        )
        
        # 测试维度职业分析
        analysis = profession1.get_dimensional_profession_analysis(profession2)
        print(f"✓ 维度职业分析成功: {analysis}")
        
        return True
        
    except Exception as e:
        print(f"✗ 维度特性功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== 新体系模型完整功能测试 ===")
    print()
    
    tests = [
        ("生民体系", test_civilian_system),
        ("司法体系", test_judicial_system),
        ("职业体系", test_profession_system),
        ("维度特性", test_dimensional_features)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"--- 测试 {test_name} ---")
        if test_func():
            print(f"✅ {test_name} 测试通过")
            passed += 1
        else:
            print(f"❌ {test_name} 测试失败")
        print()
    
    print(f"=== 测试结果: {passed}/{total} 通过 ===")
    
    if passed == total:
        print("🎉 所有测试通过！新体系功能正常。")
        return True
    else:
        print("❌ 部分测试失败，请检查相关功能。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
