"""
AI助手项目数据访问服务
为AI助手提供统一的项目数据读写接口，确保数据安全和一致性
"""
from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
import logging
import json
from datetime import datetime

from .project_data_service import ProjectDataService
from .ai_service import ai_manager
from ..models.project import Project

logger = logging.getLogger(__name__)


class AIProjectService:
    """AI助手项目数据访问服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.project_data_service = ProjectDataService(db)
        self.ai_manager = ai_manager
        self.current_project_id = None
        self.ai_operation_log = []

    def set_current_project(self, project_id: int) -> bool:
        """设置当前操作的项目"""
        project = self.db.query(Project).filter(
            Project.id == project_id,
            Project.is_deleted == False
        ).first()

        if not project:
            logger.error(f"项目 {project_id} 不存在")
            return False

        self.current_project_id = project_id
        logger.info(f"AI助手当前操作项目设置为: {project.name} (ID: {project_id})")
        return True

    def get_current_project_id(self) -> Optional[int]:
        """获取当前操作的项目ID"""
        return self.current_project_id

    def read_project_data(self, data_type: Optional[str] = None) -> Dict[str, Any]:
        """AI助手读取项目数据"""
        if not self.current_project_id:
            raise ValueError("未设置当前操作项目")

        try:
            if data_type:
                # 读取指定类型的数据
                data = self.project_data_service.get_project_model_data(
                    self.current_project_id, data_type
                )
                result = {data_type: data}
            else:
                # 读取所有项目数据
                result = self.project_data_service.get_project_data(self.current_project_id)

            # 记录AI操作日志
            self._log_ai_operation("read", data_type or "all_data", success=True)

            return result

        except Exception as e:
            self._log_ai_operation("read", data_type or "all_data", success=False, error=str(e))
            logger.error(f"AI读取项目数据失败: {e}")
            raise

    def write_project_data(self, data_type: str, data: Dict[str, Any], operation: str = "create") -> Dict[str, Any]:
        """AI助手写入项目数据"""
        if not self.current_project_id:
            raise ValueError("未设置当前操作项目")

        try:
            if operation == "create":
                result = self.project_data_service.create_project_data(
                    self.current_project_id, data_type, data
                )
            elif operation == "update":
                item_id = data.pop('id', None)
                if not item_id:
                    raise ValueError("更新操作需要提供记录ID")
                result = self.project_data_service.update_project_data(
                    self.current_project_id, data_type, item_id, data
                )
            else:
                raise ValueError(f"不支持的操作类型: {operation}")

            # 记录AI操作日志
            self._log_ai_operation("write", data_type, success=True, operation=operation)

            return result

        except Exception as e:
            self._log_ai_operation("write", data_type, success=False, error=str(e), operation=operation)
            logger.error(f"AI写入项目数据失败: {e}")
            raise

    def delete_project_data(self, data_type: str, item_id: int) -> bool:
        """AI助手删除项目数据"""
        if not self.current_project_id:
            raise ValueError("未设置当前操作项目")

        try:
            result = self.project_data_service.delete_project_data(
                self.current_project_id, data_type, item_id
            )

            # 记录AI操作日志
            self._log_ai_operation("delete", data_type, success=result, item_id=item_id)

            return result

        except Exception as e:
            self._log_ai_operation("delete", data_type, success=False, error=str(e), item_id=item_id)
            logger.error(f"AI删除项目数据失败: {e}")
            raise

    def batch_write_project_data(self, batch_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """AI助手批量写入项目数据"""
        if not self.current_project_id:
            raise ValueError("未设置当前操作项目")

        results = {}
        errors = {}

        for data_type, items in batch_data.items():
            results[data_type] = []
            errors[data_type] = []

            for item_data in items:
                try:
                    operation = "update" if "id" in item_data else "create"
                    result = self.write_project_data(data_type, item_data.copy(), operation)
                    results[data_type].append(result)
                except Exception as e:
                    errors[data_type].append({
                        "data": item_data,
                        "error": str(e)
                    })

        # 记录批量操作日志
        total_success = sum(len(items) for items in results.values())
        total_errors = sum(len(items) for items in errors.values())

        self._log_ai_operation(
            "batch_write",
            "multiple",
            success=total_errors == 0,
            batch_info=f"成功: {total_success}, 失败: {total_errors}"
        )

        return {
            "results": results,
            "errors": errors,
            "summary": {
                "total_success": total_success,
                "total_errors": total_errors
            }
        }

    def search_project_data(self, query: str, data_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """AI助手搜索项目数据"""
        if not self.current_project_id:
            raise ValueError("未设置当前操作项目")

        search_results = {}

        # 确定搜索范围
        search_types = data_types or list(self.project_data_service.project_models.keys())

        for data_type in search_types:
            try:
                # 获取该类型的所有数据
                data = self.project_data_service.get_project_model_data(
                    self.current_project_id, data_type
                )

                # 简单的文本搜索（可以后续优化为更智能的搜索）
                matches = []
                for item in data:
                    item_str = json.dumps(item, ensure_ascii=False).lower()
                    if query.lower() in item_str:
                        matches.append(item)

                if matches:
                    search_results[data_type] = matches

            except Exception as e:
                logger.warning(f"搜索 {data_type} 时出错: {e}")

        # 记录搜索操作
        self._log_ai_operation("search", "multiple", success=True, query=query)

        return search_results

    def get_project_context(self) -> Dict[str, Any]:
        """获取项目上下文信息，供AI助手理解当前项目状态"""
        if not self.current_project_id:
            raise ValueError("未设置当前操作项目")

        try:
            # 获取项目基本信息
            project = self.db.query(Project).filter(Project.id == self.current_project_id).first()

            # 获取项目统计
            statistics = self.project_data_service.get_project_statistics(self.current_project_id)

            # 获取最近的AI操作记录
            recent_operations = self.ai_operation_log[-10:] if self.ai_operation_log else []

            context = {
                "project_info": project.to_dict() if project else {},
                "statistics": statistics,
                "recent_ai_operations": recent_operations,
                "available_data_types": list(self.project_data_service.project_models.keys()),
                "current_time": datetime.now().isoformat()
            }

            return context

        except Exception as e:
            logger.error(f"获取项目上下文失败: {e}")
            raise

    def validate_ai_operation(self, operation: str, data_type: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """验证AI操作的合法性"""
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": []
        }

        # 检查项目是否设置
        if not self.current_project_id:
            validation_result["is_valid"] = False
            validation_result["errors"].append("未设置当前操作项目")
            return validation_result

        # 检查数据类型是否支持
        if data_type not in self.project_data_service.project_models:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"不支持的数据类型: {data_type}")
            return validation_result

        # 检查操作类型
        valid_operations = ["create", "read", "update", "delete", "search", "batch_write"]
        if operation not in valid_operations:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"不支持的操作类型: {operation}")
            return validation_result

        # TODO: 添加更多业务逻辑验证

        return validation_result

    def _log_ai_operation(self, operation: str, data_type: str, success: bool, **kwargs):
        """记录AI操作日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "project_id": self.current_project_id,
            "operation": operation,
            "data_type": data_type,
            "success": success,
            **kwargs
        }

        self.ai_operation_log.append(log_entry)

        # 保持日志数量在合理范围内
        if len(self.ai_operation_log) > 1000:
            self.ai_operation_log = self.ai_operation_log[-500:]

        # 记录到系统日志
        if success:
            logger.info(f"AI操作成功: {operation} {data_type} in project {self.current_project_id}")
        else:
            logger.warning(f"AI操作失败: {operation} {data_type} in project {self.current_project_id}")

    def get_ai_operation_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取AI操作日志"""
        return self.ai_operation_log[-limit:] if self.ai_operation_log else []

    def clear_ai_operation_log(self):
        """清空AI操作日志"""
        self.ai_operation_log.clear()
        logger.info("AI操作日志已清空")
