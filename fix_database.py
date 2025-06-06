#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复数据库结构脚本
"""

import sqlite3
import os

def fix_database():
    """修复数据库结构"""
    db_path = "backend/novelcraft.db"
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查is_preset字段是否存在
        cursor.execute("PRAGMA table_info(projects)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_preset' not in columns:
            print("🔧 添加is_preset字段到projects表...")
            cursor.execute("ALTER TABLE projects ADD COLUMN is_preset BOOLEAN DEFAULT FALSE")
            print("✅ is_preset字段添加成功")
        else:
            print("✅ is_preset字段已存在")
        
        # 清空所有现有数据
        print("🗑️ 清空现有项目数据...")
        
        # 获取所有项目表
        tables_to_clear = [
            'projects', 'world_settings', 'cultivation_systems', 'characters', 
            'factions', 'plots', 'chapters', 'volumes', 'timelines',
            'character_relations', 'faction_relations', 'event_associations',
            'political_systems', 'currency_systems', 'commerce_systems',
            'race_systems', 'martial_arts_systems', 'equipment_systems',
            'pet_systems', 'map_structures', 'dimension_structures',
            'resource_distributions', 'race_distributions', 'secret_realm_distributions',
            'spiritual_treasure_systems', 'civilian_systems', 'judicial_systems',
            'profession_systems'
        ]
        
        for table in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"✅ 清空表 {table}")
            except sqlite3.OperationalError as e:
                if "no such table" not in str(e):
                    print(f"⚠️ 清空表 {table} 时出错: {e}")
        
        conn.commit()
        conn.close()
        
        print("✅ 数据库修复完成")
        return True
        
    except Exception as e:
        print(f"❌ 修复数据库时出错: {e}")
        return False

if __name__ == "__main__":
    fix_database()
