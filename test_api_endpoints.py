#!/usr/bin/env python3
"""
测试新体系API端点
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_api_health():
    """测试API健康状态"""
    try:
        # 测试根路径
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✓ API服务正常运行")
            return True
        else:
            print(f"✗ API服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 无法连接到API服务: {e}")
        return False

def create_test_project():
    """创建测试项目"""
    try:
        # 先检查是否已有项目
        response = requests.get(f"{BASE_URL}/projects/")
        if response.status_code == 200:
            projects = response.json()
            if isinstance(projects, dict) and "projects" in projects:
                projects_list = projects["projects"]
            else:
                projects_list = projects

            if projects_list:
                project_id = projects_list[0]["id"]
                print(f"✓ 使用现有项目: ID {project_id}")
                return project_id

        # 创建新项目
        project_data = {
            "name": "API测试项目",
            "description": "用于测试新体系API的项目",
            "project_type": "fantasy",
            "status": "planning"
        }

        response = requests.post(f"{BASE_URL}/projects/", json=project_data)
        if response.status_code == 200:
            project = response.json()
            project_id = project["id"]
            print(f"✓ 创建测试项目成功: ID {project_id}")
            return project_id
        else:
            print(f"✗ 创建测试项目失败: {response.status_code}")
            print(f"  错误信息: {response.text}")
            return None

    except Exception as e:
        print(f"✗ 创建测试项目异常: {e}")
        return None

def test_civilian_systems_api(project_id):
    """测试生民体系API"""
    try:
        print("\n--- 测试生民体系API ---")

        # 测试获取列表（应该为空）
        response = requests.get(f"{BASE_URL}/civilian-systems/?project_id={project_id}")
        if response.status_code == 200:
            print("✓ 获取生民体系列表成功")
            systems = response.json()
            print(f"  当前生民体系数量: {len(systems)}")
        else:
            print(f"✗ 获取生民体系列表失败: {response.status_code}")
            return False

        # 测试创建生民体系
        test_data = {
            "name": "测试生民体系",
            "description": "API测试用的生民体系",
            "project_id": project_id,
            "dimension_id": 1,
            "region_name": "测试区域",
            "total_population": 100000,
            "population_density": 50.5,
            "literacy_rate": 75.0
        }

        response = requests.post(f"{BASE_URL}/civilian-systems/", json=test_data)
        if response.status_code == 200:
            print("✓ 创建生民体系成功")
            created_system = response.json()
            system_id = created_system["id"]
            print(f"  创建的体系ID: {system_id}")

            # 测试获取详情
            response = requests.get(f"{BASE_URL}/civilian-systems/{system_id}")
            if response.status_code == 200:
                print("✓ 获取生民体系详情成功")
                system_detail = response.json()
                print(f"  体系名称: {system_detail['name']}")
                print(f"  总人口: {system_detail['total_population']}")
            else:
                print(f"✗ 获取生民体系详情失败: {response.status_code}")

            return True
        else:
            print(f"✗ 创建生民体系失败: {response.status_code}")
            print(f"  错误信息: {response.text}")
            return False

    except Exception as e:
        print(f"✗ 生民体系API测试失败: {e}")
        return False

def test_judicial_systems_api(project_id):
    """测试司法体系API"""
    try:
        print("\n--- 测试司法体系API ---")

        # 测试获取列表
        response = requests.get(f"{BASE_URL}/judicial-systems/?project_id={project_id}")
        if response.status_code == 200:
            print("✓ 获取司法体系列表成功")
            systems = response.json()
            print(f"  当前司法体系数量: {len(systems)}")
        else:
            print(f"✗ 获取司法体系列表失败: {response.status_code}")
            return False

        # 测试创建司法体系
        test_data = {
            "name": "测试司法体系",
            "description": "API测试用的司法体系",
            "project_id": project_id,
            "dimension_id": 1,
            "jurisdiction_name": "测试法域",
            "legal_system_type": "civil_law",
            "procedure_type": "mixed"
        }

        response = requests.post(f"{BASE_URL}/judicial-systems/", json=test_data)
        if response.status_code == 200:
            print("✓ 创建司法体系成功")
            created_system = response.json()
            system_id = created_system["id"]
            print(f"  创建的体系ID: {system_id}")

            # 测试获取详情
            response = requests.get(f"{BASE_URL}/judicial-systems/{system_id}")
            if response.status_code == 200:
                print("✓ 获取司法体系详情成功")
                system_detail = response.json()
                print(f"  体系名称: {system_detail['name']}")
                print(f"  法律体系类型: {system_detail['legal_system_type']}")
            else:
                print(f"✗ 获取司法体系详情失败: {response.status_code}")

            return True
        else:
            print(f"✗ 创建司法体系失败: {response.status_code}")
            print(f"  错误信息: {response.text}")
            return False

    except Exception as e:
        print(f"✗ 司法体系API测试失败: {e}")
        return False

def test_profession_systems_api(project_id):
    """测试职业体系API"""
    try:
        print("\n--- 测试职业体系API ---")

        # 测试获取列表
        response = requests.get(f"{BASE_URL}/profession-systems/?project_id={project_id}")
        if response.status_code == 200:
            print("✓ 获取职业体系列表成功")
            systems = response.json()
            print(f"  当前职业体系数量: {len(systems)}")
        else:
            print(f"✗ 获取职业体系列表失败: {response.status_code}")
            return False

        # 测试创建职业体系
        test_data = {
            "name": "测试职业体系",
            "description": "API测试用的职业体系",
            "project_id": project_id,
            "dimension_id": 1,
            "economic_context": "测试经济背景"
        }

        response = requests.post(f"{BASE_URL}/profession-systems/", json=test_data)
        if response.status_code == 200:
            print("✓ 创建职业体系成功")
            created_system = response.json()
            system_id = created_system["id"]
            print(f"  创建的体系ID: {system_id}")

            # 测试获取详情
            response = requests.get(f"{BASE_URL}/profession-systems/{system_id}")
            if response.status_code == 200:
                print("✓ 获取职业体系详情成功")
                system_detail = response.json()
                print(f"  体系名称: {system_detail['name']}")
                print(f"  经济背景: {system_detail['economic_context']}")
            else:
                print(f"✗ 获取职业体系详情失败: {response.status_code}")

            return True
        else:
            print(f"✗ 创建职业体系失败: {response.status_code}")
            print(f"  错误信息: {response.text}")
            return False

    except Exception as e:
        print(f"✗ 职业体系API测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== 新体系API端点测试 ===")

    # 等待服务启动
    print("等待API服务启动...")
    time.sleep(2)

    # 测试API健康状态
    if not test_api_health():
        print("❌ API服务未正常运行，请先启动后端服务")
        return False

    # 创建或获取测试项目
    project_id = create_test_project()
    if not project_id:
        print("❌ 无法创建测试项目")
        return False

    tests = [
        ("生民体系API", lambda: test_civilian_systems_api(project_id)),
        ("司法体系API", lambda: test_judicial_systems_api(project_id)),
        ("职业体系API", lambda: test_profession_systems_api(project_id))
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        if test_func():
            print(f"✅ {test_name} 测试通过")
            passed += 1
        else:
            print(f"❌ {test_name} 测试失败")

    print(f"\n=== 测试结果: {passed}/{total} 通过 ===")

    if passed == total:
        print("🎉 所有API端点测试通过！")
        return True
    else:
        print("❌ 部分API端点测试失败")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
