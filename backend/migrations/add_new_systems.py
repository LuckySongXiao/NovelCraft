#!/usr/bin/env python3
"""
添加新体系表的数据库迁移脚本
生民体系、司法体系、职业体系
"""
import sys
import os

# 添加后端路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine
from app.core.config import settings
from app.models.base import BaseModel
from app.models.civilian_system import CivilianSystem
from app.models.judicial_system import JudicialSystem
from app.models.profession_system import ProfessionSystem

def create_new_tables():
    """创建新的体系表"""
    try:
        # 创建数据库引擎
        engine = create_engine(settings.database_url)

        print("开始创建新体系表...")

        # 创建所有新表
        BaseModel.metadata.create_all(engine, tables=[
            CivilianSystem.__table__,
            JudicialSystem.__table__,
            ProfessionSystem.__table__
        ])

        print("✓ 生民体系表创建成功")
        print("✓ 司法体系表创建成功")
        print("✓ 职业体系表创建成功")
        print("所有新体系表创建完成！")

    except Exception as e:
        print(f"✗ 创建表失败: {e}")
        return False

    return True

def verify_tables():
    """验证表是否创建成功"""
    try:
        from sqlalchemy import inspect

        engine = create_engine(settings.database_url)
        inspector = inspect(engine)

        tables = inspector.get_table_names()

        required_tables = [
            'civilian_systems',
            'judicial_systems',
            'profession_systems'
        ]

        print("\n验证表创建状态:")
        for table in required_tables:
            if table in tables:
                print(f"✓ {table} 表存在")
            else:
                print(f"✗ {table} 表不存在")
                return False

        print("所有表验证通过！")
        return True

    except Exception as e:
        print(f"✗ 验证表失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 新体系表迁移脚本 ===")
    print("将创建以下表:")
    print("- civilian_systems (生民体系)")
    print("- judicial_systems (司法体系)")
    print("- profession_systems (职业体系)")
    print()

    # 创建表
    if create_new_tables():
        # 验证表
        if verify_tables():
            print("\n🎉 迁移完成！新体系表已成功创建。")
        else:
            print("\n❌ 迁移失败！表验证未通过。")
            sys.exit(1)
    else:
        print("\n❌ 迁移失败！表创建失败。")
        sys.exit(1)

if __name__ == "__main__":
    main()
