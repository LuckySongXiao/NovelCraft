"""
项目数据管理API端点
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...services.project_data_service import ProjectDataService
from ...services.ai_project_service import AIProjectService

router = APIRouter()


class ProjectDataRequest(BaseModel):
    """项目数据请求模型"""
    data: Dict[str, Any]


class BatchDataRequest(BaseModel):
    """批量数据请求模型"""
    batch_data: Dict[str, List[Dict[str, Any]]]


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str
    data_types: Optional[List[str]] = None


@router.get("/projects/{project_id}/data")
async def get_project_data(
    project_id: int,
    model_name: Optional[str] = Query(None, description="指定模型类型，不指定则返回所有数据"),
    db: Session = Depends(get_db)
):
    """获取项目数据"""
    service = ProjectDataService(db)
    
    try:
        if model_name:
            data = service.get_project_model_data(project_id, model_name)
            return {"data": {model_name: data}}
        else:
            data = service.get_project_data(project_id)
            return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取项目数据失败: {str(e)}")


@router.post("/projects/{project_id}/data/{model_name}")
async def create_project_data(
    project_id: int,
    model_name: str,
    request: ProjectDataRequest,
    db: Session = Depends(get_db)
):
    """创建项目数据"""
    service = ProjectDataService(db)
    
    try:
        result = service.create_project_data(project_id, model_name, request.data)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建项目数据失败: {str(e)}")


@router.put("/projects/{project_id}/data/{model_name}/{item_id}")
async def update_project_data(
    project_id: int,
    model_name: str,
    item_id: int,
    request: ProjectDataRequest,
    db: Session = Depends(get_db)
):
    """更新项目数据"""
    service = ProjectDataService(db)
    
    try:
        result = service.update_project_data(project_id, model_name, item_id, request.data)
        if result is None:
            raise HTTPException(status_code=404, detail="数据记录不存在")
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新项目数据失败: {str(e)}")


@router.delete("/projects/{project_id}/data/{model_name}/{item_id}")
async def delete_project_data(
    project_id: int,
    model_name: str,
    item_id: int,
    db: Session = Depends(get_db)
):
    """删除项目数据"""
    service = ProjectDataService(db)
    
    try:
        success = service.delete_project_data(project_id, model_name, item_id)
        if not success:
            raise HTTPException(status_code=404, detail="数据记录不存在")
        return {"success": True, "message": "删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除项目数据失败: {str(e)}")


@router.get("/projects/{project_id}/statistics")
async def get_project_statistics(
    project_id: int,
    db: Session = Depends(get_db)
):
    """获取项目统计信息"""
    service = ProjectDataService(db)
    
    try:
        stats = service.get_project_statistics(project_id)
        return {"statistics": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取项目统计失败: {str(e)}")


@router.delete("/projects/{project_id}/data")
async def clear_project_data(
    project_id: int,
    model_names: Optional[List[str]] = Query(None, description="指定要清空的模型类型"),
    db: Session = Depends(get_db)
):
    """清空项目数据"""
    service = ProjectDataService(db)
    
    try:
        success = service.clear_project_data(project_id, model_names)
        if not success:
            raise HTTPException(status_code=500, detail="清空项目数据失败")
        return {"success": True, "message": "清空成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空项目数据失败: {str(e)}")


@router.post("/projects/{source_project_id}/copy-to/{target_project_id}")
async def copy_project_data(
    source_project_id: int,
    target_project_id: int,
    model_names: Optional[List[str]] = Query(None, description="指定要复制的模型类型"),
    db: Session = Depends(get_db)
):
    """复制项目数据"""
    service = ProjectDataService(db)
    
    try:
        success = service.copy_project_data(source_project_id, target_project_id, model_names)
        if not success:
            raise HTTPException(status_code=500, detail="复制项目数据失败")
        return {"success": True, "message": "复制成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"复制项目数据失败: {str(e)}")


@router.get("/projects/{project_id}/validate")
async def validate_project_data(
    project_id: int,
    db: Session = Depends(get_db)
):
    """验证项目数据完整性"""
    service = ProjectDataService(db)
    
    try:
        result = service.validate_project_data_integrity(project_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"验证项目数据失败: {str(e)}")


# AI助手专用接口
@router.post("/ai/set-project/{project_id}")
async def ai_set_current_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """AI助手设置当前操作项目"""
    service = AIProjectService(db)
    
    try:
        success = service.set_current_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="项目不存在")
        return {"success": True, "message": f"当前项目已设置为 {project_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"设置当前项目失败: {str(e)}")


@router.get("/ai/current-project")
async def ai_get_current_project(
    db: Session = Depends(get_db)
):
    """AI助手获取当前操作项目"""
    service = AIProjectService(db)
    
    project_id = service.get_current_project_id()
    if project_id is None:
        raise HTTPException(status_code=400, detail="未设置当前操作项目")
    
    return {"current_project_id": project_id}


@router.get("/ai/read-data")
async def ai_read_project_data(
    data_type: Optional[str] = Query(None, description="数据类型"),
    db: Session = Depends(get_db)
):
    """AI助手读取项目数据"""
    service = AIProjectService(db)
    
    try:
        data = service.read_project_data(data_type)
        return {"success": True, "data": data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI读取数据失败: {str(e)}")


@router.post("/ai/write-data/{data_type}")
async def ai_write_project_data(
    data_type: str,
    request: ProjectDataRequest,
    operation: str = Query("create", description="操作类型: create 或 update"),
    db: Session = Depends(get_db)
):
    """AI助手写入项目数据"""
    service = AIProjectService(db)
    
    try:
        result = service.write_project_data(data_type, request.data, operation)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI写入数据失败: {str(e)}")


@router.post("/ai/batch-write")
async def ai_batch_write_project_data(
    request: BatchDataRequest,
    db: Session = Depends(get_db)
):
    """AI助手批量写入项目数据"""
    service = AIProjectService(db)
    
    try:
        result = service.batch_write_project_data(request.batch_data)
        return {"success": True, "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI批量写入数据失败: {str(e)}")


@router.post("/ai/search")
async def ai_search_project_data(
    request: SearchRequest,
    db: Session = Depends(get_db)
):
    """AI助手搜索项目数据"""
    service = AIProjectService(db)
    
    try:
        results = service.search_project_data(request.query, request.data_types)
        return {"success": True, "results": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI搜索数据失败: {str(e)}")


@router.get("/ai/context")
async def ai_get_project_context(
    db: Session = Depends(get_db)
):
    """AI助手获取项目上下文"""
    service = AIProjectService(db)
    
    try:
        context = service.get_project_context()
        return {"success": True, "context": context}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取项目上下文失败: {str(e)}")


@router.get("/ai/operation-log")
async def ai_get_operation_log(
    limit: int = Query(50, description="返回记录数量"),
    db: Session = Depends(get_db)
):
    """获取AI操作日志"""
    service = AIProjectService(db)
    
    try:
        log = service.get_ai_operation_log(limit)
        return {"success": True, "log": log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取操作日志失败: {str(e)}")


@router.delete("/ai/operation-log")
async def ai_clear_operation_log(
    db: Session = Depends(get_db)
):
    """清空AI操作日志"""
    service = AIProjectService(db)
    
    try:
        service.clear_ai_operation_log()
        return {"success": True, "message": "操作日志已清空"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空操作日志失败: {str(e)}")
