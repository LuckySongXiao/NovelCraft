"""
预置项目功能完整验证脚本
"""
import requests
import json
import time
from datetime import datetime

# 配置
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_api():
    """测试后端API"""
    print("🔍 测试后端API...")
    
    try:
        # 测试健康检查
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端API服务正常")
        else:
            print("❌ 后端API服务异常")
            return False
    except Exception as e:
        print(f"❌ 后端API连接失败: {e}")
        return False
    
    return True

def test_frontend_service():
    """测试前端服务"""
    print("🔍 测试前端服务...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常")
        else:
            print("❌ 前端服务异常")
            return False
    except Exception as e:
        print(f"❌ 前端服务连接失败: {e}")
        return False
    
    return True

def test_project_api():
    """测试项目API"""
    print("🔍 测试项目管理API...")
    
    try:
        # 获取项目列表
        response = requests.get(f"{BACKEND_URL}/api/projects/", timeout=10)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ 项目列表获取成功，共 {len(projects)} 个项目")
            
            # 检查预置项目
            preset_projects = [p for p in projects if p.get('is_preset', False)]
            print(f"📋 发现 {len(preset_projects)} 个预置项目")
            
            for project in preset_projects:
                print(f"   - {project['name']} (ID: {project['id']})")
            
            return True
        else:
            print(f"❌ 项目列表获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 项目API测试失败: {e}")
        return False

def test_preset_project_restrictions():
    """测试预置项目权限限制"""
    print("🔍 测试预置项目权限限制...")
    
    try:
        # 获取项目列表
        response = requests.get(f"{BACKEND_URL}/api/projects/", timeout=10)
        if response.status_code != 200:
            print("❌ 无法获取项目列表")
            return False
        
        projects = response.json()
        preset_projects = [p for p in projects if p.get('is_preset', False)]
        
        if not preset_projects:
            print("⚠️  未找到预置项目，跳过权限测试")
            return True
        
        preset_project = preset_projects[0]
        project_id = preset_project['id']
        
        # 测试编辑限制
        print(f"🔒 测试预置项目 {preset_project['name']} 的编辑限制...")
        update_data = {
            "name": "测试修改名称",
            "title": "测试修改标题"
        }
        
        response = requests.put(
            f"{BACKEND_URL}/api/projects/{project_id}",
            json=update_data,
            timeout=10
        )
        
        if response.status_code == 400:
            error_msg = response.json().get('detail', '')
            if "预置项目不允许编辑" in error_msg:
                print("✅ 预置项目编辑限制正常工作")
            else:
                print(f"⚠️  编辑限制消息异常: {error_msg}")
        else:
            print(f"❌ 预置项目编辑限制失效: {response.status_code}")
            return False
        
        # 测试删除限制
        print(f"🗑️  测试预置项目 {preset_project['name']} 的删除限制...")
        response = requests.delete(f"{BACKEND_URL}/api/projects/{project_id}", timeout=10)
        
        if response.status_code == 400:
            error_msg = response.json().get('detail', '')
            if "预置项目不允许删除" in error_msg:
                print("✅ 预置项目删除限制正常工作")
            else:
                print(f"⚠️  删除限制消息异常: {error_msg}")
        else:
            print(f"❌ 预置项目删除限制失效: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 预置项目权限测试失败: {e}")
        return False

def test_project_copy():
    """测试项目复制功能"""
    print("🔍 测试项目复制功能...")
    
    try:
        # 获取项目列表
        response = requests.get(f"{BACKEND_URL}/api/projects/", timeout=10)
        if response.status_code != 200:
            print("❌ 无法获取项目列表")
            return False
        
        projects = response.json()
        preset_projects = [p for p in projects if p.get('is_preset', False)]
        
        if not preset_projects:
            print("⚠️  未找到预置项目，跳过复制测试")
            return True
        
        preset_project = preset_projects[0]
        project_id = preset_project['id']
        
        # 测试复制功能
        print(f"📋 测试复制预置项目 {preset_project['name']}...")
        copy_name = f"测试复制_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        response = requests.post(
            f"{BACKEND_URL}/api/projects/{project_id}/duplicate",
            json={"new_name": copy_name},
            timeout=10
        )
        
        if response.status_code == 200:
            copied_project = response.json()
            print(f"✅ 项目复制成功: {copied_project['name']}")
            
            # 验证复制的项目不是预置项目
            if not copied_project.get('is_preset', True):
                print("✅ 复制的项目正确设置为非预置项目")
            else:
                print("❌ 复制的项目错误地标记为预置项目")
                return False
            
            # 清理测试数据
            cleanup_id = copied_project['id']
            requests.delete(f"{BACKEND_URL}/api/projects/{cleanup_id}")
            print("🧹 测试数据已清理")
            
            return True
        else:
            print(f"❌ 项目复制失败: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ 项目复制测试失败: {e}")
        return False

def generate_test_report():
    """生成测试报告"""
    print("\n" + "="*60)
    print("📊 预置项目功能验证报告")
    print("="*60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("后端API服务", test_backend_api),
        ("前端服务", test_frontend_service),
        ("项目管理API", test_project_api),
        ("预置项目权限限制", test_preset_project_restrictions),
        ("项目复制功能", test_project_copy)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 执行测试: {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试执行异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "="*60)
    print("📋 测试结果汇总")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！预置项目功能正常工作。")
    else:
        print("⚠️  部分测试失败，请检查相关功能。")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("🚀 开始预置项目功能完整验证...")
    generate_test_report()
