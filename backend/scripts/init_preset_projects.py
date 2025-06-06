"""
初始化预置项目数据脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.project import Project, ProjectType, ProjectStatus
from backend.app.services.project_service import ProjectService


def create_preset_projects():
    """创建预置项目"""
    db = next(get_db())
    service = ProjectService(db)
    
    preset_projects = [
        {
            "name": "【预置】玄幻世界模板",
            "title": "修仙世界设定模板",
            "author": "系统",
            "project_type": ProjectType.FANTASY,
            "status": ProjectStatus.COMPLETED,
            "summary": "完整的修仙世界设定模板，包含修炼体系、门派势力、法宝装备等完整设定",
            "description": "这是一个完整的玄幻修仙世界模板，包含了详细的世界观设定、修炼体系、门派势力、人物关系、法宝装备等各个方面的内容。可以作为创作玄幻小说的参考模板。",
            "outline": "包含修炼境界、门派设定、法宝体系、地理环境、历史背景等完整大纲",
            "word_count": 50000,
            "chapter_count": 20,
            "character_count": 15,
            "is_preset": True,
            "settings": {
                "ai_enabled": True,
                "auto_save": True,
                "auto_backup": True,
                "consistency_check": True,
                "word_count_target": 50000,
                "chapter_target": 20,
                "writing_style": "third_person",
                "language": "zh-CN",
                "theme": "fantasy"
            },
            "tags": ["玄幻", "修仙", "模板", "预置"]
        },
        {
            "name": "【预置】现代都市模板",
            "title": "都市异能设定模板",
            "author": "系统",
            "project_type": ProjectType.MODERN,
            "status": ProjectStatus.COMPLETED,
            "summary": "现代都市背景的异能世界设定模板，包含异能体系、组织势力、现代科技等设定",
            "description": "这是一个现代都市异能世界模板，融合了现代科技与超自然能力，包含异能分类、觉醒机制、组织架构、社会结构等详细设定。适合创作都市异能类小说。",
            "outline": "包含异能体系、觉醒机制、组织势力、科技发展、社会结构等完整设定",
            "word_count": 30000,
            "chapter_count": 15,
            "character_count": 10,
            "is_preset": True,
            "settings": {
                "ai_enabled": True,
                "auto_save": True,
                "auto_backup": True,
                "consistency_check": True,
                "word_count_target": 30000,
                "chapter_target": 15,
                "writing_style": "third_person",
                "language": "zh-CN",
                "theme": "modern"
            },
            "tags": ["都市", "异能", "现代", "模板", "预置"]
        },
        {
            "name": "【预置】科幻星际模板",
            "title": "星际文明设定模板",
            "author": "系统",
            "project_type": ProjectType.SCIFI,
            "status": ProjectStatus.COMPLETED,
            "summary": "科幻星际背景的世界设定模板，包含星际文明、科技体系、宇宙结构等设定",
            "description": "这是一个科幻星际世界模板，描述了未来星际时代的文明发展、科技进步、宇宙探索等内容。包含详细的科技体系、文明等级、星际政治等设定。",
            "outline": "包含科技发展、文明等级、星际政治、宇宙结构、种族设定等完整框架",
            "word_count": 40000,
            "chapter_count": 18,
            "character_count": 12,
            "is_preset": True,
            "settings": {
                "ai_enabled": True,
                "auto_save": True,
                "auto_backup": True,
                "consistency_check": True,
                "word_count_target": 40000,
                "chapter_target": 18,
                "writing_style": "third_person",
                "language": "zh-CN",
                "theme": "scifi"
            },
            "tags": ["科幻", "星际", "未来", "模板", "预置"]
        }
    ]
    
    for project_data in preset_projects:
        try:
            # 检查是否已存在
            existing = db.query(Project).filter(Project.name == project_data["name"]).first()
            if existing:
                print(f"预置项目 '{project_data['name']}' 已存在，跳过创建")
                continue
            
            # 创建项目
            project = Project(**project_data)
            project.set_tags(project_data["tags"])
            
            db.add(project)
            db.commit()
            db.refresh(project)
            
            print(f"成功创建预置项目: {project_data['name']}")
            
        except Exception as e:
            print(f"创建预置项目 '{project_data['name']}' 失败: {e}")
            db.rollback()
    
    db.close()


if __name__ == "__main__":
    create_preset_projects()
    print("预置项目初始化完成")
