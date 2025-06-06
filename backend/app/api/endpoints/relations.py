"""
关系管理 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ...core.database import get_db
from ...models.relations import CharacterRelation, FactionRelation, RelationStatus

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/character-relations")
async def get_character_relations(
    project_id: int = Query(..., description="项目ID"),
    character_id: Optional[int] = Query(None, description="特定角色ID"),
    relation_type: Optional[str] = Query(None, description="关系类型"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取人物关系列表"""
    try:
        query = db.query(CharacterRelation).filter(
            CharacterRelation.project_id == project_id
        )

        if character_id is not None:
            query = query.filter(
                (CharacterRelation.character_a_id == character_id) |
                (CharacterRelation.character_b_id == character_id)
            )

        if relation_type is not None:
            query = query.filter(CharacterRelation.relation_type == relation_type)

        relations = query.offset(skip).limit(limit).all()

        return [relation.to_dict() for relation in relations]
    except Exception as e:
        logger.error(f"获取人物关系列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取人物关系列表失败")


@router.get("/faction-relations")
async def get_faction_relations(
    project_id: int = Query(..., description="项目ID"),
    faction_id: Optional[int] = Query(None, description="特定势力ID"),
    relation_type: Optional[str] = Query(None, description="关系类型"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="限制数量"),
    db: Session = Depends(get_db)
):
    """获取势力关系列表"""
    try:
        query = db.query(FactionRelation).filter(
            FactionRelation.project_id == project_id
        )

        if faction_id is not None:
            query = query.filter(
                (FactionRelation.faction_a_id == faction_id) |
                (FactionRelation.faction_b_id == faction_id)
            )

        if relation_type is not None:
            query = query.filter(FactionRelation.relation_type == relation_type)

        relations = query.offset(skip).limit(limit).all()

        return [relation.to_dict() for relation in relations]
    except Exception as e:
        logger.error(f"获取势力关系列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取势力关系列表失败")


@router.post("/character-relations")
async def create_character_relation(
    relation_data: dict,
    db: Session = Depends(get_db)
):
    """创建人物关系"""
    try:
        relation = CharacterRelation(**relation_data)
        db.add(relation)
        db.commit()
        db.refresh(relation)

        logger.info(f"创建人物关系成功: {relation.id}")
        return relation.to_dict()
    except Exception as e:
        db.rollback()
        logger.error(f"创建人物关系失败: {e}")
        raise HTTPException(status_code=500, detail="创建人物关系失败")


@router.post("/faction-relations")
async def create_faction_relation(
    relation_data: dict,
    db: Session = Depends(get_db)
):
    """创建势力关系"""
    try:
        relation = FactionRelation(**relation_data)
        db.add(relation)
        db.commit()
        db.refresh(relation)

        logger.info(f"创建势力关系成功: {relation.id}")
        return relation.to_dict()
    except Exception as e:
        db.rollback()
        logger.error(f"创建势力关系失败: {e}")
        raise HTTPException(status_code=500, detail="创建势力关系失败")


@router.put("/character-relations/{relation_id}")
async def update_character_relation(
    relation_id: int,
    relation_data: dict,
    db: Session = Depends(get_db)
):
    """更新人物关系"""
    try:
        relation = db.query(CharacterRelation).filter(
            CharacterRelation.id == relation_id
        ).first()

        if not relation:
            raise HTTPException(status_code=404, detail="人物关系不存在")

        # 更新字段
        for field, value in relation_data.items():
            if hasattr(relation, field):
                setattr(relation, field, value)

        db.commit()
        db.refresh(relation)

        logger.info(f"更新人物关系成功: {relation.id}")
        return relation.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新人物关系失败: {e}")
        raise HTTPException(status_code=500, detail="更新人物关系失败")


@router.delete("/character-relations/{relation_id}")
async def delete_character_relation(
    relation_id: int,
    db: Session = Depends(get_db)
):
    """删除人物关系"""
    try:
        relation = db.query(CharacterRelation).filter(
            CharacterRelation.id == relation_id
        ).first()

        if not relation:
            raise HTTPException(status_code=404, detail="人物关系不存在")

        db.delete(relation)
        db.commit()

        logger.info(f"删除人物关系成功: {relation_id}")
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除人物关系失败: {e}")
        raise HTTPException(status_code=500, detail="删除人物关系失败")


@router.get("/character-relations/{relation_id}/score")
async def get_relation_score(
    relation_id: int,
    db: Session = Depends(get_db)
):
    """获取关系评分"""
    try:
        relation = db.query(CharacterRelation).filter(
            CharacterRelation.id == relation_id
        ).first()

        if not relation:
            raise HTTPException(status_code=404, detail="人物关系不存在")

        score = relation.calculate_relationship_score()
        return {"relationship_score": score}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取关系评分失败: {e}")
        raise HTTPException(status_code=500, detail="获取关系评分失败")


@router.post("/character-relations/{relation_id}/update-trust")
async def update_trust_level(
    relation_id: int,
    trust_change: float,
    reason: str = "",
    db: Session = Depends(get_db)
):
    """更新信任度"""
    try:
        relation = db.query(CharacterRelation).filter(
            CharacterRelation.id == relation_id
        ).first()

        if not relation:
            raise HTTPException(status_code=404, detail="人物关系不存在")

        relation.update_trust(trust_change, reason)
        db.commit()

        return {"message": "信任度更新成功", "new_trust_level": relation.trust_level}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新信任度失败: {e}")
        raise HTTPException(status_code=500, detail="更新信任度失败")


@router.get("/network-analysis")
async def get_network_analysis(
    project_id: int = Query(..., description="项目ID"),
    db: Session = Depends(get_db)
):
    """获取关系网络分析"""
    try:
        # 获取所有人物关系
        character_relations = db.query(CharacterRelation).filter(
            CharacterRelation.project_id == project_id
        ).all()

        # 获取所有势力关系
        faction_relations = db.query(FactionRelation).filter(
            FactionRelation.project_id == project_id
        ).all()

        # 统计分析
        total_relations = len(character_relations) + len(faction_relations)

        # 按关系类型统计
        relation_types = {}
        for relation in character_relations:
            relation_type = relation.relation_type
            relation_types[relation_type] = relation_types.get(relation_type, 0) + 1

        # 按状态统计
        status_counts = {}
        for relation in character_relations:
            status = relation.status
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "total_relations": total_relations,
            "character_relations_count": len(character_relations),
            "faction_relations_count": len(faction_relations),
            "relation_types": relation_types,
            "status_counts": status_counts
        }
    except Exception as e:
        logger.error(f"获取关系网络分析失败: {e}")
        raise HTTPException(status_code=500, detail="获取关系网络分析失败")
