"""
智能对话API端点
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...services.conversation_service import ConversationService

router = APIRouter()


class StartConversationRequest(BaseModel):
    """开始对话请求模型"""
    user_id: str
    project_id: Optional[int] = None


class UserInputRequest(BaseModel):
    """用户输入请求模型"""
    user_id: str
    user_input: str
    additional_data: Optional[Dict[str, Any]] = None


@router.post("/start")
async def start_conversation(
    request: StartConversationRequest,
    db: Session = Depends(get_db)
):
    """开始智能对话"""
    service = ConversationService(db)

    try:
        result = service.start_conversation(request.user_id, request.project_id)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"开始对话失败: {str(e)}")


@router.post("/input")
async def process_user_input(
    request: UserInputRequest,
    db: Session = Depends(get_db)
):
    """处理用户输入"""
    service = ConversationService(db)

    try:
        result = await service.process_user_input(
            request.user_id,
            request.user_input,
            request.additional_data
        )
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理用户输入失败: {str(e)}")


@router.get("/summary/{user_id}")
async def get_conversation_summary(
    user_id: str,
    db: Session = Depends(get_db)
):
    """获取对话总结"""
    service = ConversationService(db)

    try:
        summary = service.get_conversation_summary(user_id)
        if summary is None:
            raise HTTPException(status_code=404, detail="对话会话不存在")
        return {"success": True, "data": summary}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取对话总结失败: {str(e)}")


@router.delete("/end/{user_id}")
async def end_conversation(
    user_id: str,
    db: Session = Depends(get_db)
):
    """结束对话"""
    service = ConversationService(db)

    try:
        success = service.end_conversation(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="对话会话不存在")
        return {"success": True, "message": "对话已结束"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"结束对话失败: {str(e)}")
