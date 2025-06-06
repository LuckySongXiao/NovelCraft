"""
基础数据模型
"""
from sqlalchemy import Column, Integer, DateTime, String, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from typing import Any, Dict

from ..core.database import Base


class BaseModel(Base):
    """基础模型类，包含通用字段"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )
    is_deleted = Column(Boolean, default=False, comment="是否删除")

    @declared_attr
    def __tablename__(cls) -> str:
        """自动生成表名"""
        return cls.__name__.lower()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """从字典更新属性"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"


class ProjectBaseModel(BaseModel):
    """项目相关模型的基类"""

    __abstract__ = True

    project_id = Column(Integer, index=True, comment="项目ID")
    name = Column(String(255), nullable=False, comment="名称")
    description = Column(Text, comment="描述")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"


class VersionedMixin:
    """支持版本控制的混入类"""

    version = Column(Integer, default=1, comment="版本号")
    version_note = Column(Text, comment="版本说明")
    parent_version_id = Column(Integer, comment="父版本ID")

    def create_new_version(self, note: str = None) -> 'VersionedMixin':
        """创建新版本"""
        # 这里需要在子类中实现具体的版本创建逻辑
        pass


class TaggedMixin:
    """支持标签的混入类"""

    tags = Column(Text, comment="标签，JSON格式存储")

    def get_tags(self) -> list:
        """获取标签列表"""
        import json
        if self.tags:
            try:
                return json.loads(self.tags)
            except json.JSONDecodeError:
                return []
        return []

    def set_tags(self, tags: list) -> None:
        """设置标签列表"""
        import json
        self.tags = json.dumps(tags, ensure_ascii=False)

    def add_tag(self, tag: str) -> None:
        """添加标签"""
        tags = self.get_tags()
        if tag not in tags:
            tags.append(tag)
            self.set_tags(tags)

    def remove_tag(self, tag: str) -> None:
        """移除标签"""
        tags = self.get_tags()
        if tag in tags:
            tags.remove(tag)
            self.set_tags(tags)
