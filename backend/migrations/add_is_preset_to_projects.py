"""
添加预置项目标识字段的数据库迁移脚本
"""
from sqlalchemy import text
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine


def upgrade():
    """添加is_preset字段到projects表"""
    with engine.connect() as connection:
        # 添加is_preset字段
        connection.execute(text("""
            ALTER TABLE projects
            ADD COLUMN is_preset BOOLEAN DEFAULT FALSE COMMENT '是否为预置项目'
        """))

        # 更新现有的预置项目数据
        connection.execute(text("""
            UPDATE projects
            SET is_preset = TRUE
            WHERE name LIKE '%预置%' OR name LIKE '%模板%' OR author = '系统'
        """))

        connection.commit()
        print("成功添加is_preset字段到projects表")


def downgrade():
    """移除is_preset字段"""
    with engine.connect() as connection:
        connection.execute(text("""
            ALTER TABLE projects
            DROP COLUMN is_preset
        """))

        connection.commit()
        print("成功移除is_preset字段")


if __name__ == "__main__":
    upgrade()
