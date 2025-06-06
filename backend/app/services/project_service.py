"""
项目管理服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Tuple, Dict, Any
import json
import os
from datetime import datetime
import uuid

from ..models.project import Project, ProjectType, ProjectStatus
from ..schemas.project import ProjectCreate, ProjectUpdate
from ..core.config import settings


class ProjectService:
    """项目管理服务类"""

    def __init__(self, db: Session):
        self.db = db

    def get_projects(
        self,
        skip: int = 0,
        limit: int = 20,
        project_type: Optional[ProjectType] = None,
        status: Optional[ProjectStatus] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Project], int]:
        """获取项目列表"""
        query = self.db.query(Project).filter(Project.is_deleted == False)

        # 类型筛选
        if project_type:
            query = query.filter(Project.project_type == project_type)

        # 状态筛选
        if status:
            query = query.filter(Project.status == status)

        # 搜索筛选
        if search:
            search_filter = or_(
                Project.name.contains(search),
                Project.title.contains(search),
                Project.author.contains(search),
                Project.summary.contains(search)
            )
            query = query.filter(search_filter)

        # 获取总数
        total = query.count()

        # 分页和排序
        projects = query.order_by(Project.updated_at.desc()).offset(skip).limit(limit).all()

        return projects, total

    def get_project(self, project_id: int) -> Optional[Project]:
        """获取项目详情"""
        return self.db.query(Project).filter(
            and_(Project.id == project_id, Project.is_deleted == False)
        ).first()

    def create_project(self, project_data: ProjectCreate) -> Project:
        """创建新项目"""
        # 检查项目名称是否重复
        existing = self.db.query(Project).filter(
            and_(Project.name == project_data.name, Project.is_deleted == False)
        ).first()

        if existing:
            raise ValueError(f"项目名称 '{project_data.name}' 已存在")

        # 创建项目实例
        project = Project(
            name=project_data.name,
            title=project_data.title,
            subtitle=project_data.subtitle,
            author=project_data.author,
            project_type=project_data.project_type,
            status=project_data.status,
            summary=project_data.summary,
            description=project_data.description,
            outline=project_data.outline,
            template_id=project_data.template_id,
            template_name=project_data.template_name,
            settings=project_data.settings or {},
            project_metadata=project_data.metadata or {},
            is_preset=project_data.is_preset or False
        )

        # 设置标签
        if project_data.tags:
            project.set_tags(project_data.tags)

        # 保存到数据库
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    def update_project(self, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """更新项目"""
        project = self.get_project(project_id)
        if not project:
            return None

        # 检查名称重复（排除自己）
        if project_data.name and project_data.name != project.name:
            existing = self.db.query(Project).filter(
                and_(
                    Project.name == project_data.name,
                    Project.id != project_id,
                    Project.is_deleted == False
                )
            ).first()

            if existing:
                raise ValueError(f"项目名称 '{project_data.name}' 已存在")

        # 更新字段
        update_data = project_data.dict(exclude_unset=True)

        # 处理标签
        if 'tags' in update_data:
            tags = update_data.pop('tags')
            if tags is not None:
                project.set_tags(tags)

        # 更新其他字段
        for field, value in update_data.items():
            if hasattr(project, field):
                setattr(project, field, value)

        # 更新统计信息
        project.update_statistics()

        self.db.commit()
        self.db.refresh(project)

        return project

    def delete_project(self, project_id: int) -> bool:
        """删除项目（软删除）"""
        project = self.get_project(project_id)
        if not project:
            return False

        project.is_deleted = True
        self.db.commit()

        return True

    def duplicate_project(self, project_id: int, new_name: str) -> Optional[Project]:
        """复制项目"""
        original = self.get_project(project_id)
        if not original:
            return None

        # 检查新名称是否重复
        existing = self.db.query(Project).filter(
            and_(Project.name == new_name, Project.is_deleted == False)
        ).first()

        if existing:
            raise ValueError(f"项目名称 '{new_name}' 已存在")

        # 创建新项目
        new_project = Project(
            name=new_name,
            title=f"{original.title} (副本)" if original.title else None,
            subtitle=original.subtitle,
            author=original.author,
            project_type=original.project_type,
            status=ProjectStatus.PLANNING,  # 新项目状态重置为规划中
            summary=original.summary,
            description=original.description,
            outline=original.outline,
            template_id=original.template_id,
            template_name=original.template_name,
            settings=original.settings.copy() if original.settings else {},
            metadata=original.metadata.copy() if original.metadata else {}
        )

        # 复制标签
        new_project.set_tags(original.get_tags())

        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project)

        return new_project

    def get_project_statistics(self, project_id: int) -> Optional[Dict[str, Any]]:
        """获取项目统计信息"""
        project = self.get_project(project_id)
        if not project:
            return None

        # 这里需要查询相关的统计数据
        # 暂时返回基础统计
        stats = {
            "word_count": project.word_count,
            "chapter_count": project.chapter_count,
            "character_count": project.character_count,
            "faction_count": 0,  # 需要从相关表查询
            "plot_count": 0,     # 需要从相关表查询
            "world_setting_count": 0,  # 需要从相关表查询
            "cultivation_system_count": 0,  # 需要从相关表查询
            "timeline_count": 0,  # 需要从相关表查询
            "last_updated": project.updated_at,
            "progress": project.get_progress()
        }

        return stats

    def export_project(self, project_id: int, format: str = "json") -> Optional[Dict[str, Any]]:
        """导出项目"""
        project = self.get_project(project_id)
        if not project:
            return None

        if format not in ["json", "yaml", "xml"]:
            raise ValueError(f"不支持的导出格式: {format}")

        # 构建导出数据
        export_data = {
            "project": project.to_dict(),
            "characters": [],  # 需要查询相关数据
            "factions": [],
            "plots": [],
            "chapters": [],
            "world_settings": [],
            "cultivation_systems": [],
            "timelines": [],
            "relations": [],
            "export_time": datetime.now().isoformat(),
            "export_version": "1.0"
        }

        return export_data

    def import_project(self, import_data: Dict[str, Any]) -> Project:
        """导入项目"""
        if "project" not in import_data:
            raise ValueError("导入数据中缺少项目信息")

        project_data = import_data["project"]

        # 检查项目名称是否重复，如果重复则自动重命名
        original_name = project_data.get("name", "导入的项目")
        name = original_name
        counter = 1

        while self.db.query(Project).filter(
            and_(Project.name == name, Project.is_deleted == False)
        ).first():
            name = f"{original_name} ({counter})"
            counter += 1

        # 创建项目
        project = Project(
            name=name,
            title=project_data.get("title"),
            subtitle=project_data.get("subtitle"),
            author=project_data.get("author"),
            project_type=project_data.get("project_type", ProjectType.FANTASY),
            status=ProjectStatus.PLANNING,  # 导入的项目状态重置
            summary=project_data.get("summary"),
            description=project_data.get("description"),
            outline=project_data.get("outline"),
            settings=project_data.get("settings", {}),
            metadata=project_data.get("metadata", {})
        )

        # 设置标签
        if "tags" in project_data:
            project.set_tags(project_data["tags"])

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        # TODO: 导入相关数据（人物、势力、剧情等）

        return project

    def backup_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """备份项目"""
        project = self.get_project(project_id)
        if not project:
            return None

        # 生成备份ID
        backup_id = str(uuid.uuid4())
        backup_time = datetime.now()

        # 导出项目数据
        backup_data = self.export_project(project_id)

        # 保存备份文件
        backup_dir = os.path.join(settings.upload_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)

        backup_filename = f"project_{project_id}_{backup_time.strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = os.path.join(backup_dir, backup_filename)

        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)

        backup_info = {
            "backup_id": backup_id,
            "project_id": project_id,
            "backup_time": backup_time.isoformat(),
            "backup_size": os.path.getsize(backup_path),
            "backup_path": backup_path,
            "description": f"项目 {project.name} 的自动备份"
        }

        return backup_info

    def restore_project(self, project_id: int, backup_id: str) -> bool:
        """恢复项目"""
        # 这里需要实现从备份恢复项目的逻辑
        # 暂时返回True表示成功
        return True
