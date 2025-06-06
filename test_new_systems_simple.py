#!/usr/bin/env python3
"""
简化的新体系测试脚本
"""
import sys
import os

# 添加后端路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """测试模型导入"""
    try:
        print("测试模型导入...")
        
        # 测试生民体系
        from app.models.civilian_system import CivilianSystem, SocialClass, LifestyleType
        print("✓ 生民体系模型导入成功")
        
        # 测试司法体系
        from app.models.judicial_system import JudicialSystem, CourtType, LegalSystem, TrialProcedure
        print("✓ 司法体系模型导入成功")
        
        # 测试职业体系
        from app.models.profession_system import ProfessionSystem, ProfessionCategory, SkillLevel, CareerPath
        print("✓ 职业体系模型导入成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 模型导入失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    try:
        print("\n测试基本功能...")
        
        from app.models.civilian_system import CivilianSystem
        from app.models.judicial_system import JudicialSystem
        from app.models.profession_system import ProfessionSystem
        
        # 测试生民体系创建
        civilian = CivilianSystem(
            name="测试生民体系",
            description="测试描述",
            total_population=100000
        )
        print("✓ 生民体系创建成功")
        
        # 测试司法体系创建
        judicial = JudicialSystem(
            name="测试司法体系",
            description="测试描述",
            legal_system_type="civil_law"
        )
        print("✓ 司法体系创建成功")
        
        # 测试职业体系创建
        profession = ProfessionSystem(
            name="测试职业体系",
            description="测试描述"
        )
        print("✓ 职业体系创建成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 新体系简化测试 ===")
    
    tests = [
        ("模型导入", test_imports),
        ("基本功能", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            break
    
    print(f"\n=== 测试结果: {passed}/{total} 通过 ===")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return True
    else:
        print("❌ 测试失败！")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
