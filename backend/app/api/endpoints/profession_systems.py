"""
职业体系API接口
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.profession_system import ProfessionSystem
from ...schemas.profession_system import (
    ProfessionSystemCreate,
    ProfessionSystemUpdate,
    ProfessionSystemResponse,
    ProfessionData,
    SkillData,
    CareerPathData,
    ProfessionalOrganizationData,
    SkillGapAnalysisData
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[ProfessionSystemResponse])
async def get_profession_systems(
    project_id: int = Query(..., description="项目ID"),
    dimension_id: int = Query(None, description="维度ID"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取职业体系列表"""
    try:
        query = db.query(ProfessionSystem).filter(
            ProfessionSystem.project_id == project_id
        )

        if dimension_id is not None:
            query = query.filter(ProfessionSystem.dimension_id == dimension_id)

        systems = query.offset(skip).limit(limit).all()

        return [system.to_dict() for system in systems]
    except Exception as e:
        logger.error(f"获取职业体系列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取职业体系列表失败")


@router.post("/", response_model=ProfessionSystemResponse)
async def create_profession_system(
    system_data: ProfessionSystemCreate,
    db: Session = Depends(get_db)
):
    """创建新职业体系"""
    try:
        system = ProfessionSystem(**system_data.dict())
        db.add(system)
        db.commit()
        db.refresh(system)

        logger.info(f"创建职业体系成功: {system.id}")
        return system.to_dict()
    except Exception as e:
        logger.error(f"创建职业体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="创建职业体系失败")


@router.get("/{system_id}", response_model=ProfessionSystemResponse)
async def get_profession_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    """获取职业体系详情"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        return system.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取职业体系详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取职业体系详情失败")


@router.put("/{system_id}", response_model=ProfessionSystemResponse)
async def update_profession_system(
    system_id: int,
    system_data: ProfessionSystemUpdate,
    db: Session = Depends(get_db)
):
    """更新职业体系"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        # 更新字段
        update_data = system_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(system, field, value)

        db.commit()
        db.refresh(system)

        logger.info(f"更新职业体系成功: {system_id}")
        return system.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新职业体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="更新职业体系失败")


@router.delete("/{system_id}")
async def delete_profession_system(
    system_id: int,
    db: Session = Depends(get_db)
):
    """删除职业体系"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        db.delete(system)
        db.commit()

        logger.info(f"删除职业体系成功: {system_id}")
        return {"message": "职业体系删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除职业体系失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="删除职业体系失败")


@router.post("/{system_id}/professions")
async def add_profession(
    system_id: int,
    profession_data: ProfessionData,
    db: Session = Depends(get_db)
):
    """添加职业"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        system.add_profession(profession_data.dict())
        db.commit()

        logger.info(f"添加职业成功: {system_id}")
        return {"message": "职业添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加职业失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加职业失败")


@router.post("/{system_id}/skills/{profession_name}")
async def add_skill_requirement(
    system_id: int,
    profession_name: str,
    skill_data: SkillData,
    db: Session = Depends(get_db)
):
    """为职业添加技能要求"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        system.add_skill_requirement(profession_name, skill_data.dict())
        db.commit()

        logger.info(f"添加技能要求成功: {system_id}")
        return {"message": "技能要求添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加技能要求失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加技能要求失败")


@router.post("/{system_id}/career-paths")
async def add_career_path(
    system_id: int,
    path_data: CareerPathData,
    db: Session = Depends(get_db)
):
    """添加职业发展路径"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        system.add_career_path(path_data.dict())
        db.commit()

        logger.info(f"添加职业发展路径成功: {system_id}")
        return {"message": "职业发展路径添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加职业发展路径失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加职业发展路径失败")


@router.post("/{system_id}/organizations")
async def add_professional_organization(
    system_id: int,
    org_data: ProfessionalOrganizationData,
    db: Session = Depends(get_db)
):
    """添加行业组织"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        system.add_professional_organization(org_data.dict())
        db.commit()

        logger.info(f"添加行业组织成功: {system_id}")
        return {"message": "行业组织添加成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"添加行业组织失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="添加行业组织失败")


@router.get("/{system_id}/profession-metrics")
async def get_profession_metrics(
    system_id: int,
    db: Session = Depends(get_db)
):
    """获取职业体系指标"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        metrics = system.calculate_profession_metrics()
        return metrics
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取职业体系指标失败: {e}")
        raise HTTPException(status_code=500, detail="获取职业体系指标失败")


@router.get("/{system_id}/dimensional-analysis/{target_system_id}")
async def get_dimensional_profession_analysis(
    system_id: int,
    target_system_id: int,
    db: Session = Depends(get_db)
):
    """获取维度职业分析"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        target_system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == target_system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        if not target_system:
            raise HTTPException(status_code=404, detail="目标职业体系不存在")

        analysis = system.get_dimensional_profession_analysis(target_system)
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取维度职业分析失败: {e}")
        raise HTTPException(status_code=500, detail="获取维度职业分析失败")


@router.get("/{system_id}/career-transition/{from_profession}/{to_profession}")
async def validate_career_transition(
    system_id: int,
    from_profession: str,
    to_profession: str,
    db: Session = Depends(get_db)
):
    """验证职业转换可行性"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        is_valid = system.validate_career_transition(from_profession, to_profession)
        return {"valid": is_valid, "message": "职业转换验证完成"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"验证职业转换可行性失败: {e}")
        raise HTTPException(status_code=500, detail="验证职业转换可行性失败")


@router.get("/{system_id}/skill-gap-analysis/{target_profession}")
async def get_skill_gap_analysis(
    system_id: int,
    target_profession: str,
    db: Session = Depends(get_db)
):
    """获取技能差距分析"""
    try:
        system = db.query(ProfessionSystem).filter(
            ProfessionSystem.id == system_id
        ).first()

        if not system:
            raise HTTPException(status_code=404, detail="职业体系不存在")

        analysis = system.get_skill_gap_analysis(target_profession)
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取技能差距分析失败: {e}")
        raise HTTPException(status_code=500, detail="获取技能差距分析失败")
