#!/usr/bin/env python3
"""
快速API测试
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_basic_api():
    """测试基本API功能"""
    print("=== 快速API测试 ===")
    
    # 测试根路径
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✓ 根路径测试: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  服务名称: {data.get('message', 'N/A')}")
    except Exception as e:
        print(f"✗ 根路径测试失败: {e}")
    
    # 测试项目列表
    try:
        response = requests.get(f"{BASE_URL}/projects/")
        print(f"✓ 项目列表测试: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  项目数量: {len(data.get('projects', []))}")
    except Exception as e:
        print(f"✗ 项目列表测试失败: {e}")
    
    # 测试生民体系列表（使用项目ID=1）
    try:
        response = requests.get(f"{BASE_URL}/civilian-systems/?project_id=1")
        print(f"✓ 生民体系列表测试: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  生民体系数量: {len(data)}")
        else:
            print(f"  错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 生民体系列表测试失败: {e}")
    
    # 测试司法体系列表
    try:
        response = requests.get(f"{BASE_URL}/judicial-systems/?project_id=1")
        print(f"✓ 司法体系列表测试: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  司法体系数量: {len(data)}")
        else:
            print(f"  错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 司法体系列表测试失败: {e}")
    
    # 测试职业体系列表
    try:
        response = requests.get(f"{BASE_URL}/profession-systems/?project_id=1")
        print(f"✓ 职业体系列表测试: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  职业体系数量: {len(data)}")
        else:
            print(f"  错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 职业体系列表测试失败: {e}")
    
    # 测试创建生民体系
    try:
        test_data = {
            "name": "快速测试生民体系",
            "description": "快速测试用",
            "project_id": 1
        }
        response = requests.post(f"{BASE_URL}/civilian-systems/", json=test_data)
        print(f"✓ 创建生民体系测试: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  创建的体系ID: {data.get('id', 'N/A')}")
        else:
            print(f"  错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 创建生民体系测试失败: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_basic_api()
