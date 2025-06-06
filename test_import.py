#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入脚本
"""

import requests
import json

def test_create_project():
    """测试创建项目"""
    base_url = "http://localhost:8000/api"
    
    project_data = {
        "name": "千面劫·宿命轮回",
        "description": "高考结束的夜晚，宋少雨在夜市偶遇诡异面具摊，一枚千面面具竟让他觉醒前世仙君身份——千面郎君幻三千！",
        "genre": "fantasy",
        "tags": ["宿命轮回", "身份觉醒", "仙妖恋情", "都市修真", "面具觉醒"],
        "status": "writing",
        "author": "原创作者",
        "is_preset": False
    }
    
    try:
        # 先清空现有项目
        response = requests.get(f"{base_url}/projects/")
        if response.status_code == 200:
            projects = response.json()["projects"]
            for project in projects:
                project_id = project["id"]
                delete_response = requests.delete(f"{base_url}/projects/{project_id}")
                print(f"删除项目 {project['name']}: {delete_response.status_code}")
        
        # 创建新项目
        response = requests.post(f"{base_url}/projects/", json=project_data)
        print(f"创建项目响应状态: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 项目创建成功，ID: {result['id']}")
            return result['id']
        else:
            print(f"❌ 项目创建失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 创建项目时出错: {e}")
        return None

if __name__ == "__main__":
    test_create_project()
