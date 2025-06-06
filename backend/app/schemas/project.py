"""
项目数据模式定义
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

from ..models.project import ProjectType, ProjectStatus


class ProjectBase(BaseModel):
    """项目基础模式"""
    name: str = Field(..., min_length=1, max_length=255, description="项目名称")
    title: Optional[str] = Field(None, max_length=500, description="小说标题")
    subtitle: Optional[str] = Field(None, max_length=500, description="副标题")
    author: Optional[str] = Field(None, max_length=100, description="作者")
    project_type: ProjectType = Field(ProjectType.FANTASY, description="项目类型")
    status: ProjectStatus = Field(ProjectStatus.PLANNING, description="项目状态")
    summary: Optional[str] = Field(None, description="简介")
    description: Optional[str] = Field(None, description="详细描述")
    outline: Optional[str] = Field(None, description="大纲")
    tags: Optional[List[str]] = Field(default_factory=list, description="标签")
    is_preset: Optional[bool] = Field(False, description="是否为预置项目")


class ProjectCreate(ProjectBase):
    """创建项目模式"""
    template_id: Optional[int] = Field(None, description="模板ID")
    template_name: Optional[str] = Field(None, max_length=100, description="模板名称")
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict, description="项目设置")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="元数据")

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('项目名称不能为空')
        return v.strip()

    @validator('tags')
    def validate_tags(cls, v):
        if v:
            # 去重并过滤空标签
            return list(set(tag.strip() for tag in v if tag and tag.strip()))
        return []


class ProjectUpdate(BaseModel):
    """更新项目模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="项目名称")
    title: Optional[str] = Field(None, max_length=500, description="小说标题")
    subtitle: Optional[str] = Field(None, max_length=500, description="副标题")
    author: Optional[str] = Field(None, max_length=100, description="作者")
    project_type: Optional[ProjectType] = Field(None, description="项目类型")
    status: Optional[ProjectStatus] = Field(None, description="项目状态")
    summary: Optional[str] = Field(None, description="简介")
    description: Optional[str] = Field(None, description="详细描述")
    outline: Optional[str] = Field(None, description="大纲")
    tags: Optional[List[str]] = Field(None, description="标签")
    settings: Optional[Dict[str, Any]] = Field(None, description="项目设置")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('项目名称不能为空')
        return v.strip() if v else v

    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            return list(set(tag.strip() for tag in v if tag and tag.strip()))
        return v


class ProjectProgress(BaseModel):
    """项目进度模式"""
    word_progress: float = Field(description="字数进度百分比")
    chapter_progress: float = Field(description="章节进度百分比")
    status: str = Field(description="项目状态")
    completion_rate: float = Field(description="完成率")


class ProjectStatistics(BaseModel):
    """项目统计模式"""
    word_count: int = Field(description="总字数")
    chapter_count: int = Field(description="章节数量")
    character_count: int = Field(description="人物数量")
    faction_count: int = Field(description="势力数量")
    plot_count: int = Field(description="剧情数量")
    world_setting_count: int = Field(description="世界设定数量")
    cultivation_system_count: int = Field(description="修炼体系数量")
    timeline_count: int = Field(description="时间线数量")
    last_updated: datetime = Field(description="最后更新时间")


class ProjectResponse(ProjectBase):
    """项目响应模式"""
    id: int = Field(description="项目ID")
    word_count: int = Field(description="字数统计")
    chapter_count: int = Field(description="章节数量")
    character_count: int = Field(description="人物数量")
    version: int = Field(description="版本号")
    version_note: Optional[str] = Field(description="版本说明")
    settings: Dict[str, Any] = Field(description="项目设置")
    metadata: Dict[str, Any] = Field(description="元数据")
    progress: ProjectProgress = Field(description="项目进度")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")

    @validator('metadata', pre=True, always=True)
    def validate_metadata(cls, v, values):
        # 如果是Project对象，从project_metadata字段获取
        if hasattr(v, 'project_metadata'):
            return v.project_metadata or {}
        return v or {}

    @validator('progress', pre=True, always=True)
    def validate_progress(cls, v, values):
        # 如果是Project对象，调用get_progress方法
        if hasattr(v, 'get_progress'):
            return v.get_progress()
        return v

    @validator('tags', pre=True, always=True)
    def validate_tags(cls, v, values):
        # 如果是Project对象，调用get_tags方法
        if hasattr(v, 'get_tags'):
            return v.get_tags()
        # 如果是字符串格式的JSON，解析它
        if isinstance(v, str):
            try:
                import json
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v or []

    class Config:
        from_attributes = True


class ProjectListItem(BaseModel):
    """项目列表项模式"""
    id: int = Field(description="项目ID")
    name: str = Field(description="项目名称")
    title: Optional[str] = Field(description="小说标题")
    author: Optional[str] = Field(description="作者")
    project_type: ProjectType = Field(description="项目类型")
    status: ProjectStatus = Field(description="项目状态")
    word_count: int = Field(description="字数统计")
    chapter_count: int = Field(description="章节数量")
    progress: ProjectProgress = Field(description="项目进度")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")
    tags: List[str] = Field(description="标签")
    is_preset: bool = Field(description="是否为预置项目")

    @validator('progress', pre=True, always=True)
    def validate_progress(cls, v, values):
        # 如果传入的是整个Project对象，调用get_progress方法
        if hasattr(v, 'get_progress'):
            return v.get_progress()
        # 如果v是None或者缺失，尝试从values中获取Project对象
        if v is None and 'id' in values:
            # 这里需要从原始对象获取progress信息
            return {"word_progress": 0, "chapter_progress": 0, "status": "planning", "completion_rate": 0}
        return v

    @validator('tags', pre=True, always=True)
    def validate_tags(cls, v, values):
        # 如果传入的是整个Project对象，调用get_tags方法
        if hasattr(v, 'get_tags'):
            return v.get_tags()
        # 如果是字符串格式的JSON，解析它
        if isinstance(v, str):
            try:
                import json
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v or []

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """项目列表响应模式"""
    projects: List[ProjectListItem] = Field(description="项目列表")
    total: int = Field(description="总数量")
    skip: int = Field(description="跳过数量")
    limit: int = Field(description="限制数量")


class ProjectExport(BaseModel):
    """项目导出模式"""
    project: ProjectResponse = Field(description="项目信息")
    characters: List[Dict[str, Any]] = Field(description="人物数据")
    factions: List[Dict[str, Any]] = Field(description="势力数据")
    plots: List[Dict[str, Any]] = Field(description="剧情数据")
    chapters: List[Dict[str, Any]] = Field(description="章节数据")
    world_settings: List[Dict[str, Any]] = Field(description="世界设定数据")
    cultivation_systems: List[Dict[str, Any]] = Field(description="修炼体系数据")
    timelines: List[Dict[str, Any]] = Field(description="时间线数据")
    relations: List[Dict[str, Any]] = Field(description="关系数据")
    export_time: datetime = Field(description="导出时间")
    export_version: str = Field(description="导出版本")


class ProjectImport(BaseModel):
    """项目导入模式"""
    project_data: Dict[str, Any] = Field(description="项目数据")
    import_options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="导入选项")

    @validator('project_data')
    def validate_project_data(cls, v):
        if not v:
            raise ValueError('项目数据不能为空')

        # 检查必要字段
        required_fields = ['project', 'export_version']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'缺少必要字段: {field}')

        return v


class ProjectBackup(BaseModel):
    """项目备份模式"""
    backup_id: str = Field(description="备份ID")
    project_id: int = Field(description="项目ID")
    backup_time: datetime = Field(description="备份时间")
    backup_size: int = Field(description="备份大小(字节)")
    backup_path: str = Field(description="备份路径")
    description: Optional[str] = Field(description="备份描述")


class ProjectTemplate(BaseModel):
    """项目模板模式"""
    id: int = Field(description="模板ID")
    name: str = Field(description="模板名称")
    description: str = Field(description="模板描述")
    project_type: ProjectType = Field(description="项目类型")
    template_data: Dict[str, Any] = Field(description="模板数据")
    is_builtin: bool = Field(description="是否内置模板")
    created_at: datetime = Field(description="创建时间")

    class Config:
        from_attributes = True
