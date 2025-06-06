"""
生民体系API接口
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.civilian_system import CivilianSystem
from ...schemas.civilian_system import (
    CivilianSystemCreate,
    CivilianSystemUpdate,
    CivilianSystemResponse,
    SocialClassData,
    LifestyleData,
    CulturalPracticeData,
    PopulationStatsData,
    DimensionalComparisonData
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[CivilianSystemResponse])
async def get_civilian_systems(
    project_id: int = Query(..., description="项目ID"),
    dimension_id: int = Query(None, description="维度ID"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取生民体系列表"""
    try:
        query = db.query(CivilianSystem).filter(
            CivilianSystem.project_id == project_id
        )

        if dimension_id is not None:
            query = query.filter(CivilianSystem.dimension_id == dimension_id)

        systems = query.offset(skip).limit(limit).all()

        return [system.to_dict() for system in systems]
    except Exception as e:
        logger.error(f"获取生民体系列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取生民体系列表失败")


@router.post("/", response_model=CivilianSystemResponse)
async def create_civilian_system(
    system_data: CivilianSystemCreate,
    db: Session = Depends(get_db)
):
    """创建新生民体系"""
    try:
        system = CivilianSystem(**system_data.dict())
        db.add(system)
        db.commit()
        db.refresh(system)

        logger.info(f"创建生民体系成功: {system.id}")
        return system.to_dict()
    except Exception as e:
        logger.error(f"创建生民体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="创建生民体系失败")


@router.get("/{system_id}", response_model=CivilianSystemResponse)
async def get_civilian_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    """获取生民体系详情"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        return system.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取生民体系详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取生民体系详情失败")


@router.put("/{system_id}", response_model=CivilianSystemResponse)
async def update_civilian_system(
    system_id: int,
    system_data: CivilianSystemUpdate,
    db: Session = Depends(get_db)
):
    """更新生民体系"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        # 更新字段
        update_data = system_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(system, field, value)

        db.commit()
        db.refresh(system)

        logger.info(f"更新生民体系成功: {system_id}")
        return system.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新生民体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="更新生民体系失败")


@router.delete("/{system_id}")
async def delete_civilian_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    """删除生民体系"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        db.delete(system)
        db.commit()

        logger.info(f"删除生民体系成功: {system_id}")
        return {"message": "生民体系删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除生民体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="删除生民体系失败")


@router.post("/{system_id}/social-classes")
async def add_social_class(
    system_id: int,
    class_data: SocialClassData,
    db: Session = Depends(get_db)
):
    """添加社会阶层"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        system.add_social_class(class_data.dict())
        db.commit()

        logger.info(f"添加社会阶层成功: {system_id}")
        return {"message": "社会阶层添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加社会阶层失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加社会阶层失败")


@router.post("/{system_id}/lifestyle-types")
async def add_lifestyle_type(
    system_id: int,
    lifestyle_data: LifestyleData,
    db: Session = Depends(get_db)
):
    """添加生活方式"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        system.add_lifestyle_type(lifestyle_data.dict())
        db.commit()

        logger.info(f"添加生活方式成功: {system_id}")
        return {"message": "生活方式添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加生活方式失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加生活方式失败")


@router.post("/{system_id}/cultural-practices")
async def add_cultural_practice(
    system_id: int,
    practice_data: CulturalPracticeData,
    db: Session = Depends(get_db)
):
    """添加文化习俗"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        system.add_cultural_practice(practice_data.dict())
        db.commit()

        logger.info(f"添加文化习俗成功: {system_id}")
        return {"message": "文化习俗添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加文化习俗失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加文化习俗失败")


@router.put("/{system_id}/population-stats")
async def update_population_stats(
    system_id: int,
    stats_data: PopulationStatsData,
    db: Session = Depends(get_db)
):
    """更新人口统计"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        system.update_population_stats(stats_data.dict())
        db.commit()

        logger.info(f"更新人口统计成功: {system_id}")
        return {"message": "人口统计更新成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新人口统计失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="更新人口统计失败")


@router.get("/{system_id}/social-metrics")
async def get_social_metrics(
    system_id: int,
    db: Session = Depends(get_db)
):
    """获取社会指标"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        metrics = system.calculate_social_metrics()
        return metrics
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取社会指标失败: {e}")
        raise HTTPException(status_code=500, detail="获取社会指标失败")


@router.get("/{system_id}/dimensional-comparison/{target_system_id}")
async def get_dimensional_comparison(
    system_id: int,
    target_system_id: int,
    db: Session = Depends(get_db)
):
    """获取维度比较"""
    try:
        system = db.query(CivilianSystem).filter(
            CivilianSystem.id == system_id
        ).first()

        target_system = db.query(CivilianSystem).filter(
            CivilianSystem.id == target_system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="生民体系不存在")

        if not target_system:
            raise HTTPException(status_code=404, detail="目标生民体系不存在")

        comparison = system.get_dimensional_comparison(target_system)
        return comparison
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取维度比较失败: {e}")
        raise HTTPException(status_code=500, detail="获取维度比较失败")
