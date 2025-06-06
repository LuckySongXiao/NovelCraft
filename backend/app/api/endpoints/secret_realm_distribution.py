"""
秘境分布管理 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ...core.database import get_db
from ...models.secret_realm_distribution import SecretRealmDistribution, RealmType, DangerLevel, AccessType
from ...schemas.secret_realm_distribution import (
    SecretRealmDistributionCreate,
    SecretRealmDistributionUpdate,
    SecretRealmDistributionResponse
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[SecretRealmDistributionResponse])
async def get_secret_realm_distributions(
    project_id: int = Query(..., description="项目ID"),
    realm_type: Optional[RealmType] = Query(None, description="秘境类型"),
    danger_level: Optional[DangerLevel] = Query(None, description="危险等级"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取秘境分布列表"""
    try:
        query = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.project_id == project_id
        )

        if realm_type is not None:
            query = query.filter(SecretRealmDistribution.realm_type == realm_type)

        if danger_level is not None:
            query = query.filter(SecretRealmDistribution.danger_level == danger_level)

        distributions = query.offset(skip).limit(limit).all()

        return [distribution.to_dict() for distribution in distributions]
    except Exception as e:
        logger.error(f"获取秘境分布列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取秘境分布列表失败")


@router.post("/", response_model=SecretRealmDistributionResponse)
async def create_secret_realm_distribution(
    distribution_data: SecretRealmDistributionCreate,
    db: Session = Depends(get_db)
):
    """创建新秘境分布"""
    try:
        distribution = SecretRealmDistribution(**distribution_data.dict())
        db.add(distribution)
        db.commit()
        db.refresh(distribution)

        logger.info(f"创建秘境分布成功: {distribution.name}")
        return distribution.to_dict()
    except Exception as e:
        db.rollback()
        logger.error(f"创建秘境分布失败: {e}")
        raise HTTPException(status_code=500, detail="创建秘境分布失败")


@router.get("/{distribution_id}", response_model=SecretRealmDistributionResponse)
async def get_secret_realm_distribution(
    distribution_id: int,
    db: Session = Depends(get_db)
):
    """获取秘境分布详情"""
    try:
        distribution = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.id == distribution_id
        ).first()

        if not distribution:
            raise HTTPException(status_code=404, detail="秘境分布不存在")

        return distribution.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取秘境分布详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取秘境分布详情失败")


@router.put("/{distribution_id}", response_model=SecretRealmDistributionResponse)
async def update_secret_realm_distribution(
    distribution_id: int,
    distribution_data: SecretRealmDistributionUpdate,
    db: Session = Depends(get_db)
):
    """更新秘境分布"""
    try:
        distribution = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.id == distribution_id
        ).first()

        if not distribution:
            raise HTTPException(status_code=404, detail="秘境分布不存在")

        # 更新字段
        update_data = distribution_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(distribution, field, value)

        db.commit()
        db.refresh(distribution)

        logger.info(f"更新秘境分布成功: {distribution.name}")
        return distribution.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新秘境分布失败: {e}")
        raise HTTPException(status_code=500, detail="更新秘境分布失败")


@router.delete("/{distribution_id}")
async def delete_secret_realm_distribution(
    distribution_id: int,
    db: Session = Depends(get_db)
):
    """删除秘境分布"""
    try:
        distribution = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.id == distribution_id
        ).first()

        if not distribution:
            raise HTTPException(status_code=404, detail="秘境分布不存在")

        db.delete(distribution)
        db.commit()

        logger.info(f"删除秘境分布成功: {distribution.name}")
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除秘境分布失败: {e}")
        raise HTTPException(status_code=500, detail="删除秘境分布失败")


@router.get("/{distribution_id}/difficulty-score")
async def get_difficulty_score(
    distribution_id: int,
    db: Session = Depends(get_db)
):
    """获取秘境难度评分"""
    try:
        distribution = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.id == distribution_id
        ).first()

        if not distribution:
            raise HTTPException(status_code=404, detail="秘境分布不存在")

        score = distribution.calculate_difficulty_score()
        return {"difficulty_score": score}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取难度评分失败: {e}")
        raise HTTPException(status_code=500, detail="获取难度评分失败")


@router.get("/{distribution_id}/validate")
async def validate_distribution(
    distribution_id: int,
    db: Session = Depends(get_db)
):
    """验证秘境分布一致性"""
    try:
        distribution = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.id == distribution_id
        ).first()

        if not distribution:
            raise HTTPException(status_code=404, detail="秘境分布不存在")

        issues = distribution.validate_consistency()
        return {
            "is_valid": len(issues) == 0,
            "issues": issues
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"验证秘境分布失败: {e}")
        raise HTTPException(status_code=500, detail="验证秘境分布失败")


@router.post("/{distribution_id}/add-treasure")
async def add_treasure(
    distribution_id: int,
    treasure_data: dict,
    db: Session = Depends(get_db)
):
    """添加宝藏"""
    try:
        distribution = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.id == distribution_id
        ).first()

        if not distribution:
            raise HTTPException(status_code=404, detail="秘境分布不存在")

        distribution.add_treasure(treasure_data)
        db.commit()

        return {"message": "添加宝藏成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"添加宝藏失败: {e}")
        raise HTTPException(status_code=500, detail="添加宝藏失败")


@router.post("/{distribution_id}/add-guardian")
async def add_guardian_creature(
    distribution_id: int,
    creature_data: dict,
    db: Session = Depends(get_db)
):
    """添加守护生物"""
    try:
        distribution = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.id == distribution_id
        ).first()

        if not distribution:
            raise HTTPException(status_code=404, detail="秘境分布不存在")

        distribution.add_guardian_creature(creature_data)
        db.commit()

        return {"message": "添加守护生物成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"添加守护生物失败: {e}")
        raise HTTPException(status_code=500, detail="添加守护生物失败")


@router.post("/{distribution_id}/add-trap")
async def add_trap_system(
    distribution_id: int,
    trap_data: dict,
    db: Session = Depends(get_db)
):
    """添加陷阱系统"""
    try:
        distribution = db.query(SecretRealmDistribution).filter(
            SecretRealmDistribution.id == distribution_id
        ).first()

        if not distribution:
            raise HTTPException(status_code=404, detail="秘境分布不存在")

        distribution.add_trap_system(trap_data)
        db.commit()

        return {"message": "添加陷阱系统成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"添加陷阱系统失败: {e}")
        raise HTTPException(status_code=500, detail="添加陷阱系统失败")
