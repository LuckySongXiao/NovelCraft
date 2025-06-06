"""
项目管理 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ...core.database import get_db
from ...models.project import Project, ProjectType, ProjectStatus
from ...services.project_service import ProjectService
from ...schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
    ProjectListItem
)

logger = logging.getLogger(__name__)
router = APIRouter()


def build_project_response(project: Project) -> dict:
    """构建项目响应数据字典"""
    return {
        'id': project.id,
        'name': project.name,
        'title': project.title,
        'subtitle': project.subtitle,
        'author': project.author,
        'project_type': project.project_type,
        'status': project.status,
        'summary': project.summary,
        'description': project.description,
        'outline': project.outline,
        'tags': project.get_tags(),
        'is_preset': project.is_preset,
        'word_count': project.word_count,
        'chapter_count': project.chapter_count,
        'character_count': project.character_count,
        'version': project.version,
        'version_note': project.version_note,
        'settings': project.settings or {},
        'metadata': project.project_metadata or {},
        'progress': project.get_progress(),
        'created_at': project.created_at,
        'updated_at': project.updated_at
    }


@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    project_type: Optional[ProjectType] = Query(None, description="项目类型筛选"),
    status: Optional[ProjectStatus] = Query(None, description="项目状态筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取项目列表"""
    try:
        service = ProjectService(db)
        projects, total = service.get_projects(
            skip=skip,
            limit=limit,
            project_type=project_type,
            status=status,
            search=search
        )

        # 手动构建项目列表项
        project_items = []
        for project in projects:
            project_dict = {
                'id': project.id,
                'name': project.name,
                'title': project.title,
                'author': project.author,
                'project_type': project.project_type,
                'status': project.status,
                'word_count': project.word_count,
                'chapter_count': project.chapter_count,
                'progress': project.get_progress(),
                'created_at': project.created_at,
                'updated_at': project.updated_at,
                'tags': project.get_tags(),
                'is_preset': project.is_preset
            }
            project_items.append(ProjectListItem(**project_dict))

        return ProjectListResponse(
            projects=project_items,
            total=total,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        logger.error(f"获取项目列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取项目列表失败")


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    """创建新项目"""
    try:
        service = ProjectService(db)
        project = service.create_project(project_data)

        return ProjectResponse(**build_project_response(project))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建项目失败: {e}")
        raise HTTPException(status_code=500, detail="创建项目失败")


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """获取项目详情"""
    try:
        service = ProjectService(db)
        project = service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")

        return ProjectResponse(**build_project_response(project))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取项目详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取项目详情失败")


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """更新项目"""
    try:
        service = ProjectService(db)
        project = service.update_project(project_id, project_data)
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        return ProjectResponse(**build_project_response(project))
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"更新项目失败: {e}")
        raise HTTPException(status_code=500, detail="更新项目失败")


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """删除项目"""
    try:
        service = ProjectService(db)
        success = service.delete_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="项目不存在")
        return {"message": "项目删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除项目失败: {e}")
        raise HTTPException(status_code=500, detail="删除项目失败")


@router.get("/{project_id}/statistics")
async def get_project_statistics(
    project_id: int,
    db: Session = Depends(get_db)
):
    """获取项目统计信息"""
    try:
        service = ProjectService(db)
        stats = service.get_project_statistics(project_id)
        if not stats:
            raise HTTPException(status_code=404, detail="项目不存在")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取项目统计失败: {e}")
        raise HTTPException(status_code=500, detail="获取项目统计失败")


@router.post("/{project_id}/duplicate")
async def duplicate_project(
    project_id: int,
    new_name: str = Query(..., description="新项目名称"),
    db: Session = Depends(get_db)
):
    """复制项目"""
    try:
        service = ProjectService(db)
        new_project = service.duplicate_project(project_id, new_name)
        if not new_project:
            raise HTTPException(status_code=404, detail="原项目不存在")
        return ProjectResponse(**build_project_response(new_project))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"复制项目失败: {e}")
        raise HTTPException(status_code=500, detail="复制项目失败")


@router.post("/{project_id}/export")
async def export_project(
    project_id: int,
    format: str = Query("json", description="导出格式"),
    db: Session = Depends(get_db)
):
    """导出项目"""
    try:
        service = ProjectService(db)
        export_data = service.export_project(project_id, format)
        if not export_data:
            raise HTTPException(status_code=404, detail="项目不存在")
        return export_data
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"导出项目失败: {e}")
        raise HTTPException(status_code=500, detail="导出项目失败")


@router.post("/import")
async def import_project(
    import_data: dict,
    db: Session = Depends(get_db)
):
    """导入项目"""
    try:
        service = ProjectService(db)
        project = service.import_project(import_data)
        return ProjectResponse(**build_project_response(project))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"导入项目失败: {e}")
        raise HTTPException(status_code=500, detail="导入项目失败")


@router.get("/{project_id}/backup")
async def backup_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """备份项目"""
    try:
        service = ProjectService(db)
        backup_info = service.backup_project(project_id)
        if not backup_info:
            raise HTTPException(status_code=404, detail="项目不存在")
        return backup_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"备份项目失败: {e}")
        raise HTTPException(status_code=500, detail="备份项目失败")


@router.post("/{project_id}/restore")
async def restore_project(
    project_id: int,
    backup_id: str = Query(..., description="备份ID"),
    db: Session = Depends(get_db)
):
    """恢复项目"""
    try:
        service = ProjectService(db)
        success = service.restore_project(project_id, backup_id)
        if not success:
            raise HTTPException(status_code=404, detail="项目或备份不存在")
        return {"message": "项目恢复成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"恢复项目失败: {e}")
        raise HTTPException(status_code=500, detail="恢复项目失败")
