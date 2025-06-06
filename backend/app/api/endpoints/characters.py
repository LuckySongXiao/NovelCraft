"""
人物管理 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ...core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_characters(
    project_id: int = Query(..., description="项目ID"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    """获取人物列表"""
    return {"message": "人物列表功能待实现", "project_id": project_id}


@router.post("/")
async def create_character(
    character_data: dict,
    db: Session = Depends(get_db)
):
    """创建新人物"""
    return {"message": "创建人物功能待实现"}


@router.get("/{character_id}")
async def get_character(
    character_id: int,
    db: Session = Depends(get_db)
):
    """获取人物详情"""
    return {"message": "获取人物详情功能待实现", "character_id": character_id}


@router.put("/{character_id}")
async def update_character(
    character_id: int,
    character_data: dict,
    db: Session = Depends(get_db)
):
    """更新人物"""
    return {"message": "更新人物功能待实现", "character_id": character_id}


@router.delete("/{character_id}")
async def delete_character(
    character_id: int,
    db: Session = Depends(get_db)
):
    """删除人物"""
    return {"message": "删除人物功能待实现", "character_id": character_id}
