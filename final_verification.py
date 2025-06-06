#!/usr/bin/env python3
"""
最终验证脚本 - 验证新体系功能完整性
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def verify_new_systems():
    """验证新体系功能"""
    print("🔍 最终验证：新体系功能完整性检查")
    print("=" * 50)
    
    results = {
        "civilian_systems": False,
        "judicial_systems": False,
        "profession_systems": False,
        "api_endpoints": False,
        "database_tables": False
    }
    
    # 1. 验证API端点可访问性
    print("\n1. 验证API端点...")
    try:
        # 生民体系
        response = requests.get(f"{BASE_URL}/civilian-systems/?project_id=1")
        if response.status_code == 200:
            print("✅ 生民体系API端点正常")
            results["civilian_systems"] = True
        else:
            print(f"❌ 生民体系API端点异常: {response.status_code}")
        
        # 司法体系
        response = requests.get(f"{BASE_URL}/judicial-systems/?project_id=1")
        if response.status_code == 200:
            print("✅ 司法体系API端点正常")
            results["judicial_systems"] = True
        else:
            print(f"❌ 司法体系API端点异常: {response.status_code}")
        
        # 职业体系
        response = requests.get(f"{BASE_URL}/profession-systems/?project_id=1")
        if response.status_code == 200:
            print("✅ 职业体系API端点正常")
            results["profession_systems"] = True
        else:
            print(f"❌ 职业体系API端点异常: {response.status_code}")
        
        if all([results["civilian_systems"], results["judicial_systems"], results["profession_systems"]]):
            results["api_endpoints"] = True
            print("✅ 所有API端点验证通过")
        
    except Exception as e:
        print(f"❌ API端点验证失败: {e}")
    
    # 2. 验证数据创建功能
    print("\n2. 验证数据创建功能...")
    try:
        # 创建生民体系
        civilian_data = {
            "name": "验证测试生民体系",
            "description": "最终验证用的生民体系",
            "project_id": 1,
            "dimension_id": 1,
            "total_population": 50000,
            "literacy_rate": 80.0
        }
        response = requests.post(f"{BASE_URL}/civilian-systems/", json=civilian_data)
        if response.status_code == 200:
            civilian_id = response.json()["id"]
            print(f"✅ 生民体系创建成功 (ID: {civilian_id})")
        else:
            print(f"❌ 生民体系创建失败: {response.status_code}")
        
        # 创建司法体系
        judicial_data = {
            "name": "验证测试司法体系",
            "description": "最终验证用的司法体系",
            "project_id": 1,
            "dimension_id": 1,
            "legal_system_type": "civil_law",
            "procedure_type": "mixed"
        }
        response = requests.post(f"{BASE_URL}/judicial-systems/", json=judicial_data)
        if response.status_code == 200:
            judicial_id = response.json()["id"]
            print(f"✅ 司法体系创建成功 (ID: {judicial_id})")
        else:
            print(f"❌ 司法体系创建失败: {response.status_code}")
        
        # 创建职业体系
        profession_data = {
            "name": "验证测试职业体系",
            "description": "最终验证用的职业体系",
            "project_id": 1,
            "dimension_id": 1,
            "economic_context": "验证测试经济"
        }
        response = requests.post(f"{BASE_URL}/profession-systems/", json=profession_data)
        if response.status_code == 200:
            profession_id = response.json()["id"]
            print(f"✅ 职业体系创建成功 (ID: {profession_id})")
        else:
            print(f"❌ 职业体系创建失败: {response.status_code}")
        
    except Exception as e:
        print(f"❌ 数据创建验证失败: {e}")
    
    # 3. 验证数据查询功能
    print("\n3. 验证数据查询功能...")
    try:
        # 查询生民体系列表
        response = requests.get(f"{BASE_URL}/civilian-systems/?project_id=1")
        if response.status_code == 200:
            systems = response.json()
            print(f"✅ 生民体系查询成功，共 {len(systems)} 个体系")
        
        # 查询司法体系列表
        response = requests.get(f"{BASE_URL}/judicial-systems/?project_id=1")
        if response.status_code == 200:
            systems = response.json()
            print(f"✅ 司法体系查询成功，共 {len(systems)} 个体系")
        
        # 查询职业体系列表
        response = requests.get(f"{BASE_URL}/profession-systems/?project_id=1")
        if response.status_code == 200:
            systems = response.json()
            print(f"✅ 职业体系查询成功，共 {len(systems)} 个体系")
        
    except Exception as e:
        print(f"❌ 数据查询验证失败: {e}")
    
    # 4. 验证模型功能
    print("\n4. 验证模型功能...")
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from app.models.civilian_system import CivilianSystem
        from app.models.judicial_system import JudicialSystem
        from app.models.profession_system import ProfessionSystem
        
        # 测试生民体系模型
        civilian = CivilianSystem(name="模型测试", total_population=10000)
        metrics = civilian.calculate_social_metrics()
        print(f"✅ 生民体系模型功能正常，社会指标: {metrics['social_stability']:.1f}%")
        
        # 测试司法体系模型
        judicial = JudicialSystem(name="模型测试", legal_system_type="civil_law")
        efficiency = judicial.calculate_judicial_efficiency()
        print(f"✅ 司法体系模型功能正常，效率指标计算完成")
        
        # 测试职业体系模型
        profession = ProfessionSystem(name="模型测试")
        prof_metrics = profession.calculate_profession_metrics()
        print(f"✅ 职业体系模型功能正常，职业指标计算完成")
        
        results["database_tables"] = True
        
    except Exception as e:
        print(f"❌ 模型功能验证失败: {e}")
    
    # 5. 生成验证报告
    print("\n" + "=" * 50)
    print("📊 验证结果汇总:")
    print(f"  生民体系: {'✅ 通过' if results['civilian_systems'] else '❌ 失败'}")
    print(f"  司法体系: {'✅ 通过' if results['judicial_systems'] else '❌ 失败'}")
    print(f"  职业体系: {'✅ 通过' if results['profession_systems'] else '❌ 失败'}")
    print(f"  API端点: {'✅ 通过' if results['api_endpoints'] else '❌ 失败'}")
    print(f"  数据模型: {'✅ 通过' if results['database_tables'] else '❌ 失败'}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n🎯 总体结果: {passed}/{total} 项通过")
    
    if passed == total:
        print("\n🎉 恭喜！新体系功能验证全部通过！")
        print("✨ 生民体系、司法体系、职业体系已成功集成到小说管理系统中")
        print("🚀 系统已准备就绪，可以开始使用新功能")
        return True
    else:
        print(f"\n⚠️  验证未完全通过，还有 {total - passed} 项需要修复")
        return False

if __name__ == "__main__":
    success = verify_new_systems()
    exit(0 if success else 1)
