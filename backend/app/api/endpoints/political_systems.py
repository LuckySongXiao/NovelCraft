"""
政治体系管理 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ...core.database import get_db
from ...models.political_system import PoliticalSystem
from ...schemas.political_system import (
    PoliticalSystemCreate,
    PoliticalSystemUpdate,
    PoliticalSystemResponse
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[PoliticalSystemResponse])
async def get_political_systems(
    project_id: int = Query(..., description="项目ID"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取政治体系列表"""
    try:
        systems = db.query(PoliticalSystem).filter(
            PoliticalSystem.project_id == project_id
        ).offset(skip).limit(limit).all()
        
        return [system.to_dict() for system in systems]
    except Exception as e:
        logger.error(f"获取政治体系列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取政治体系列表失败")


@router.post("/", response_model=PoliticalSystemResponse)
async def create_political_system(
    system_data: PoliticalSystemCreate,
    db: Session = Depends(get_db)
):
    """创建新政治体系"""
    try:
        system = PoliticalSystem(**system_data.dict())
        db.add(system)
        db.commit()
        db.refresh(system)
        
        logger.info(f"创建政治体系成功: {system.id}")
        return system.to_dict()
    except Exception as e:
        logger.error(f"创建政治体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="创建政治体系失败")


@router.get("/{system_id}", response_model=PoliticalSystemResponse)
async def get_political_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    """获取政治体系详情"""
    try:
        system = db.query(PoliticalSystem).filter(
            PoliticalSystem.id == system_id
        ).first()
        
        if not system:
            raise HTTPException(status_code=404, detail="政治体系不存在")
        
        return system.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取政治体系详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取政治体系详情失败")


@router.put("/{system_id}", response_model=PoliticalSystemResponse)
async def update_political_system(
    system_id: int,
    system_data: PoliticalSystemUpdate,
    db: Session = Depends(get_db)
):
    """更新政治体系"""
    try:
        system = db.query(PoliticalSystem).filter(
            PoliticalSystem.id == system_id
        ).first()
        
        if not system:
            raise HTTPException(status_code=404, detail="政治体系不存在")
        
        # 更新字段
        update_data = system_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(system, field, value)
        
        db.commit()
        db.refresh(system)
        
        logger.info(f"更新政治体系成功: {system_id}")
        return system.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新政治体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="更新政治体系失败")


@router.delete("/{system_id}")
async def delete_political_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    """删除政治体系"""
    try:
        system = db.query(PoliticalSystem).filter(
            PoliticalSystem.id == system_id
        ).first()
        
        if not system:
            raise HTTPException(status_code=404, detail="政治体系不存在")
        
        db.delete(system)
        db.commit()
        
        logger.info(f"删除政治体系成功: {system_id}")
        return {"message": "政治体系删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除政治体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="删除政治体系失败")


@router.post("/{system_id}/institutions")
async def add_institution(
    system_id: int,
    institution_data: dict,
    db: Session = Depends(get_db)
):
    """添加政治机构"""
    try:
        system = db.query(PoliticalSystem).filter(
            PoliticalSystem.id == system_id
        ).first()
        
        if not system:
            raise HTTPException(status_code=404, detail="政治体系不存在")
        
        system.add_institution(institution_data)
        db.commit()
        
        logger.info(f"添加政治机构成功: {system_id}")
        return {"message": "政治机构添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加政治机构失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加政治机构失败")


@router.post("/{system_id}/laws")
async def add_law(
    system_id: int,
    law_data: dict,
    db: Session = Depends(get_db)
):
    """添加法律"""
    try:
        system = db.query(PoliticalSystem).filter(
            PoliticalSystem.id == system_id
        ).first()
        
        if not system:
            raise HTTPException(status_code=404, detail="政治体系不存在")
        
        system.add_law(law_data)
        db.commit()
        
        logger.info(f"添加法律成功: {system_id}")
        return {"message": "法律添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加法律失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加法律失败")


@router.get("/{system_id}/stability")
async def get_stability_score(
    system_id: int,
    db: Session = Depends(get_db)
):
    """获取政治稳定性评分"""
    try:
        system = db.query(PoliticalSystem).filter(
            PoliticalSystem.id == system_id
        ).first()
        
        if not system:
            raise HTTPException(status_code=404, detail="政治体系不存在")
        
        stability = system.calculate_stability_score()
        return {"stability_score": stability}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取稳定性评分失败: {e}")
        raise HTTPException(status_code=500, detail="获取稳定性评分失败")


@router.get("/{system_id}/validate")
async def validate_consistency(
    system_id: int,
    db: Session = Depends(get_db)
):
    """验证政治体系一致性"""
    try:
        system = db.query(PoliticalSystem).filter(
            PoliticalSystem.id == system_id
        ).first()
        
        if not system:
            raise HTTPException(status_code=404, detail="政治体系不存在")
        
        issues = system.validate_consistency()
        return {"consistency_issues": issues}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"验证一致性失败: {e}")
        raise HTTPException(status_code=500, detail="验证一致性失败")
