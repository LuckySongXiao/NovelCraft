"""
API 路由包
"""
from fastapi import APIRouter
from .endpoints import (
    projects,
    characters,
    factions,
    plots,
    chapters,
    volumes,
    world_settings,
    cultivation_systems,
    timelines,
    relations,
    ai_assistant,
    civilian_systems,
    judicial_systems,
    profession_systems,
    project_data,
    conversation,
    secret_realm_distribution
)

# 创建主路由器
api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"]
)

api_router.include_router(
    characters.router,
    prefix="/characters",
    tags=["characters"]
)

api_router.include_router(
    factions.router,
    prefix="/factions",
    tags=["factions"]
)

api_router.include_router(
    plots.router,
    prefix="/plots",
    tags=["plots"]
)

api_router.include_router(
    chapters.router,
    prefix="/chapters",
    tags=["chapters"]
)

api_router.include_router(
    volumes.router,
    prefix="/volumes",
    tags=["volumes"]
)

api_router.include_router(
    world_settings.router,
    prefix="/world-settings",
    tags=["world-settings"]
)

api_router.include_router(
    cultivation_systems.router,
    prefix="/cultivation-systems",
    tags=["cultivation-systems"]
)

api_router.include_router(
    timelines.router,
    prefix="/timelines",
    tags=["timelines"]
)

api_router.include_router(
    relations.router,
    prefix="/relations",
    tags=["relations"]
)

api_router.include_router(
    ai_assistant.router,
    prefix="/ai",
    tags=["ai-assistant"]
)

api_router.include_router(
    civilian_systems.router,
    prefix="/civilian-systems",
    tags=["civilian-systems"]
)

api_router.include_router(
    judicial_systems.router,
    prefix="/judicial-systems",
    tags=["judicial-systems"]
)

api_router.include_router(
    profession_systems.router,
    prefix="/profession-systems",
    tags=["profession-systems"]
)

api_router.include_router(
    project_data.router,
    prefix="/project-data",
    tags=["project-data"]
)

api_router.include_router(
    conversation.router,
    prefix="/conversation",
    tags=["conversation"]
)

api_router.include_router(
    secret_realm_distribution.router,
    prefix="/secret-realm-distributions",
    tags=["secret-realm-distributions"]
)
