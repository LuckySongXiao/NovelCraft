"""
章节管理 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ...core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_chapters(
    project_id: int = Query(..., description="项目ID"),
    db: Session = Depends(get_db)
):
    """获取章节列表"""
    return {"message": "章节列表功能待实现", "project_id": project_id}


@router.post("/")
async def create_chapter(
    chapter_data: dict,
    db: Session = Depends(get_db)
):
    """创建新章节"""
    return {"message": "创建章节功能待实现"}
