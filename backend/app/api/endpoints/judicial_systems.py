"""
司法体系API接口
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.judicial_system import JudicialSystem
from ...schemas.judicial_system import (
    JudicialSystemCreate,
    JudicialSystemUpdate,
    JudicialSystemResponse,
    CourtData,
    LegalCodeData,
    EnforcementAgencyData,
    JudicialPersonnelData,
    CrossDimensionalCaseData
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[JudicialSystemResponse])
async def get_judicial_systems(
    project_id: int = Query(..., description="项目ID"),
    dimension_id: int = Query(None, description="维度ID"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取司法体系列表"""
    try:
        query = db.query(JudicialSystem).filter(
            JudicialSystem.project_id == project_id
        )

        if dimension_id is not None:
            query = query.filter(JudicialSystem.dimension_id == dimension_id)

        systems = query.offset(skip).limit(limit).all()

        return [system.to_dict() for system in systems]
    except Exception as e:
        logger.error(f"获取司法体系列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取司法体系列表失败")


@router.post("/", response_model=JudicialSystemResponse)
async def create_judicial_system(
    system_data: JudicialSystemCreate,
    db: Session = Depends(get_db)
):
    """创建新司法体系"""
    try:
        system = JudicialSystem(**system_data.dict())
        db.add(system)
        db.commit()
        db.refresh(system)

        logger.info(f"创建司法体系成功: {system.id}")
        return system.to_dict()
    except Exception as e:
        logger.error(f"创建司法体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="创建司法体系失败")


@router.get("/{system_id}", response_model=JudicialSystemResponse)
async def get_judicial_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    """获取司法体系详情"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        return system.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取司法体系详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取司法体系详情失败")


@router.put("/{system_id}", response_model=JudicialSystemResponse)
async def update_judicial_system(
    system_id: int,
    system_data: JudicialSystemUpdate,
    db: Session = Depends(get_db)
):
    """更新司法体系"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        # 更新字段
        update_data = system_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(system, field, value)

        db.commit()
        db.refresh(system)

        logger.info(f"更新司法体系成功: {system_id}")
        return system.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新司法体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="更新司法体系失败")


@router.delete("/{system_id}")
async def delete_judicial_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    """删除司法体系"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        db.delete(system)
        db.commit()

        logger.info(f"删除司法体系成功: {system_id}")
        return {"message": "司法体系删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除司法体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="删除司法体系失败")


@router.post("/{system_id}/courts")
async def add_court(
    system_id: int,
    court_data: CourtData,
    db: Session = Depends(get_db)
):
    """添加法院"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        system.add_court(court_data.dict())
        db.commit()

        logger.info(f"添加法院成功: {system_id}")
        return {"message": "法院添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加法院失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加法院失败")


@router.post("/{system_id}/legal-codes")
async def add_legal_code(
    system_id: int,
    code_data: LegalCodeData,
    db: Session = Depends(get_db)
):
    """添加法律条文"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        system.add_legal_code(code_data.dict())
        db.commit()

        logger.info(f"添加法律条文成功: {system_id}")
        return {"message": "法律条文添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加法律条文失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加法律条文失败")


@router.post("/{system_id}/enforcement-agencies")
async def add_enforcement_agency(
    system_id: int,
    agency_data: EnforcementAgencyData,
    db: Session = Depends(get_db)
):
    """添加执法机构"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        system.add_enforcement_agency(agency_data.dict())
        db.commit()

        logger.info(f"添加执法机构成功: {system_id}")
        return {"message": "执法机构添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加执法机构失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加执法机构失败")


@router.post("/{system_id}/judicial-personnel")
async def add_judicial_personnel(
    system_id: int,
    personnel_data: JudicialPersonnelData,
    db: Session = Depends(get_db)
):
    """添加司法人员"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        system.add_judicial_personnel(personnel_data.dict())
        db.commit()

        logger.info(f"添加司法人员成功: {system_id}")
        return {"message": "司法人员添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加司法人员失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加司法人员失败")


@router.get("/{system_id}/judicial-efficiency")
async def get_judicial_efficiency(
    system_id: int,
    db: Session = Depends(get_db)
):
    """获取司法效率指标"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        efficiency = system.calculate_judicial_efficiency()
        return efficiency
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取司法效率指标失败: {e}")
        raise HTTPException(status_code=500, detail="获取司法效率指标失败")


@router.get("/{system_id}/dimensional-differences/{target_system_id}")
async def get_dimensional_legal_differences(
    system_id: int,
    target_system_id: int,
    db: Session = Depends(get_db)
):
    """获取维度法律差异"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        target_system = db.query(JudicialSystem).filter(
            JudicialSystem.id == target_system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        if not target_system:
            raise HTTPException(status_code=404, detail="目标司法体系不存在")

        differences = system.get_dimensional_legal_differences(target_system)
        return differences
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取维度法律差异失败: {e}")
        raise HTTPException(status_code=500, detail="获取维度法律差异失败")


@router.post("/{system_id}/validate-cross-dimensional-case")
async def validate_cross_dimensional_case(
    system_id: int,
    case_data: CrossDimensionalCaseData,
    db: Session = Depends(get_db)
):
    """验证跨维度案件管辖权"""
    try:
        system = db.query(JudicialSystem).filter(
            JudicialSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="司法体系不存在")

        is_valid = system.validate_cross_dimensional_case(case_data.dict())
        return {"valid": is_valid, "message": "管辖权验证完成"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"验证跨维度案件管辖权失败: {e}")
        raise HTTPException(status_code=500, detail="验证跨维度案件管辖权失败")
