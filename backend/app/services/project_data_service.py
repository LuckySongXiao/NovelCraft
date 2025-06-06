"""
项目数据管理服务
负责项目级别的数据隔离、统一访问和AI助手数据权限管理
"""
from typing import List, Optional, Dict, Any, Type, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from sqlalchemy.inspection import inspect
import logging

from ..models.base import ProjectBaseModel
from ..models.project import Project
from ..models import *  # 导入所有模型

logger = logging.getLogger(__name__)


class ProjectDataService:
    """项目数据管理服务类"""

    def __init__(self, db: Session):
        self.db = db
        # 项目相关的所有模型类映射
        self.project_models = {
            'world_setting': WorldSetting,
            'cultivation_system': CultivationSystem,
            'character': Character,
            'faction': Faction,
            'plot': Plot,
            'chapter': Chapter,
            'volume': Volume,
            'timeline': Timeline,
            'character_relation': CharacterRelation,
            'faction_relation': FactionRelation,
            'event_association': EventAssociation,
            'political_system': PoliticalSystem,
            'currency_system': CurrencySystem,
            'commerce_system': CommerceSystem,
            'race_system': RaceSystem,
            'martial_arts_system': MartialArtsSystem,
            'equipment_system': EquipmentSystem,
            'pet_system': PetSystem,
            'map_structure': MapStructure,
            'dimension_structure': DimensionStructure,
            'resource_distribution': ResourceDistribution,
            'race_distribution': RaceDistribution,
            'secret_realm_distribution': SecretRealmDistribution,
            'spiritual_treasure_system': SpiritualTreasureSystem,
            'civilian_system': CivilianSystem,
            'judicial_system': JudicialSystem,
            'profession_system': ProfessionSystem
        }

    def get_project_data(self, project_id: int) -> Optional[Dict[str, Any]]:
        """获取项目的所有数据"""
        # 验证项目是否存在
        project = self.db.query(Project).filter(
            and_(Project.id == project_id, Project.is_deleted == False)
        ).first()

        if not project:
            return None

        project_data = {
            'project': project.to_dict(),
            'data': {}
        }

        # 获取所有相关数据
        for model_name, model_class in self.project_models.items():
            try:
                # 查询该项目的所有相关数据
                query = self.db.query(model_class).filter(
                    model_class.project_id == project_id
                )

                # 如果模型支持软删除，则过滤已删除的记录
                if hasattr(model_class, 'is_deleted'):
                    query = query.filter(model_class.is_deleted == False)

                items = query.all()

                project_data['data'][model_name] = [item.to_dict() for item in items]

            except Exception as e:
                logger.warning(f"获取 {model_name} 数据时出错: {e}")
                project_data['data'][model_name] = []

        return project_data

    def get_project_model_data(self, project_id: int, model_name: str) -> List[Dict[str, Any]]:
        """获取项目中指定模型的数据"""
        if model_name not in self.project_models:
            raise ValueError(f"未知的模型类型: {model_name}")

        model_class = self.project_models[model_name]

        try:
            query = self.db.query(model_class).filter(
                model_class.project_id == project_id
            )

            # 如果模型支持软删除，则过滤已删除的记录
            if hasattr(model_class, 'is_deleted'):
                query = query.filter(model_class.is_deleted == False)

            items = query.all()

            return [item.to_dict() for item in items]

        except Exception as e:
            logger.error(f"获取项目 {project_id} 的 {model_name} 数据时出错: {e}")
            return []

    def create_project_data(self, project_id: int, model_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """为项目创建新的数据记录"""
        if model_name not in self.project_models:
            raise ValueError(f"未知的模型类型: {model_name}")

        # 验证项目是否存在
        project = self.db.query(Project).filter(
            and_(Project.id == project_id, Project.is_deleted == False)
        ).first()

        if not project:
            raise ValueError(f"项目 {project_id} 不存在")

        model_class = self.project_models[model_name]

        try:
            # 确保数据包含项目ID
            data['project_id'] = project_id

            # 创建新实例
            instance = model_class(**data)

            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)

            return instance.to_dict()

        except Exception as e:
            self.db.rollback()
            logger.error(f"创建项目 {project_id} 的 {model_name} 数据时出错: {e}")
            raise

    def update_project_data(self, project_id: int, model_name: str, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新项目中的数据记录"""
        if model_name not in self.project_models:
            raise ValueError(f"未知的模型类型: {model_name}")

        model_class = self.project_models[model_name]

        try:
            # 查询记录，确保属于指定项目且未被删除
            query = self.db.query(model_class).filter(
                and_(
                    model_class.id == item_id,
                    model_class.project_id == project_id
                )
            )

            # 如果模型支持软删除，则过滤已删除的记录
            if hasattr(model_class, 'is_deleted'):
                query = query.filter(model_class.is_deleted == False)

            instance = query.first()

            if not instance:
                return None

            # 更新字段
            for field, value in data.items():
                if hasattr(instance, field) and field != 'id' and field != 'project_id':
                    setattr(instance, field, value)

            self.db.commit()
            self.db.refresh(instance)

            return instance.to_dict()

        except Exception as e:
            self.db.rollback()
            logger.error(f"更新项目 {project_id} 的 {model_name} 数据时出错: {e}")
            raise

    def delete_project_data(self, project_id: int, model_name: str, item_id: int) -> bool:
        """删除项目中的数据记录"""
        if model_name not in self.project_models:
            raise ValueError(f"未知的模型类型: {model_name}")

        model_class = self.project_models[model_name]

        try:
            # 查询记录，确保属于指定项目且未被删除
            query = self.db.query(model_class).filter(
                and_(
                    model_class.id == item_id,
                    model_class.project_id == project_id
                )
            )

            # 如果模型支持软删除，则过滤已删除的记录
            if hasattr(model_class, 'is_deleted'):
                query = query.filter(model_class.is_deleted == False)

            instance = query.first()

            if not instance:
                return False

            # 软删除或硬删除
            if hasattr(instance, 'is_deleted'):
                instance.is_deleted = True
            else:
                self.db.delete(instance)

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"删除项目 {project_id} 的 {model_name} 数据时出错: {e}")
            return False

    def get_project_statistics(self, project_id: int) -> Dict[str, Any]:
        """获取项目的详细统计信息"""
        stats = {}

        for model_name, model_class in self.project_models.items():
            try:
                query = self.db.query(model_class).filter(
                    model_class.project_id == project_id
                )

                # 如果模型支持软删除，则过滤已删除的记录
                if hasattr(model_class, 'is_deleted'):
                    query = query.filter(model_class.is_deleted == False)

                count = query.count()
                stats[f"{model_name}_count"] = count

            except Exception as e:
                logger.warning(f"统计 {model_name} 数量时出错: {e}")
                stats[f"{model_name}_count"] = 0

        return stats

    def clear_project_data(self, project_id: int, model_names: Optional[List[str]] = None) -> bool:
        """清空项目的数据（指定模型或全部）"""
        try:
            models_to_clear = model_names or list(self.project_models.keys())

            for model_name in models_to_clear:
                if model_name not in self.project_models:
                    continue

                model_class = self.project_models[model_name]

                # 删除该项目的所有相关数据
                self.db.query(model_class).filter(
                    model_class.project_id == project_id
                ).delete()

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"清空项目 {project_id} 数据时出错: {e}")
            return False

    def copy_project_data(self, source_project_id: int, target_project_id: int, model_names: Optional[List[str]] = None) -> bool:
        """复制项目数据到另一个项目"""
        try:
            models_to_copy = model_names or list(self.project_models.keys())

            for model_name in models_to_copy:
                if model_name not in self.project_models:
                    continue

                model_class = self.project_models[model_name]

                # 获取源项目的数据
                query = self.db.query(model_class).filter(
                    model_class.project_id == source_project_id
                )

                # 如果模型支持软删除，则过滤已删除的记录
                if hasattr(model_class, 'is_deleted'):
                    query = query.filter(model_class.is_deleted == False)

                source_items = query.all()

                # 复制到目标项目
                for item in source_items:
                    # 获取所有字段值
                    item_dict = item.to_dict()

                    # 移除ID和时间戳字段，更新项目ID
                    item_dict.pop('id', None)
                    item_dict.pop('created_at', None)
                    item_dict.pop('updated_at', None)
                    item_dict['project_id'] = target_project_id

                    # 创建新实例
                    new_item = model_class(**item_dict)
                    self.db.add(new_item)

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"复制项目数据时出错: {e}")
            return False

    def validate_project_data_integrity(self, project_id: int) -> Dict[str, Any]:
        """验证项目数据的完整性和一致性"""
        validation_result = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'statistics': {}
        }

        try:
            # 获取项目统计
            validation_result['statistics'] = self.get_project_statistics(project_id)

            # TODO: 添加具体的数据一致性检查逻辑
            # 例如：检查人物关系的双向一致性、时间线的逻辑性等

        except Exception as e:
            validation_result['is_valid'] = False
            validation_result['issues'].append(f"数据验证时出错: {e}")

        return validation_result
