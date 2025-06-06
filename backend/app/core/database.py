"""
数据库连接和会话管理模块
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os

from .config import settings


# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
    # SQLite特定配置
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False,
        "timeout": 20
    } if "sqlite" in settings.database_url else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建基础模型类
Base = declarative_base()

# 元数据
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    用于依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """创建所有表"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """删除所有表"""
    Base.metadata.drop_all(bind=engine)


def init_db():
    """初始化数据库"""
    # 确保数据库目录存在
    db_dir = os.path.dirname(settings.database_url.replace("sqlite:///", ""))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # 创建表
    create_tables()
    
    print("数据库初始化完成")


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def get_session(self) -> Session:
        """获取数据库会话"""
        return SessionLocal()
    
    def close_session(self, session: Session):
        """关闭数据库会话"""
        session.close()
    
    def create_all_tables(self):
        """创建所有表"""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_all_tables(self):
        """删除所有表"""
        Base.metadata.drop_all(bind=self.engine)
    
    def execute_sql(self, sql: str):
        """执行SQL语句"""
        with self.engine.connect() as conn:
            return conn.execute(sql)


# 创建数据库管理器实例
db_manager = DatabaseManager()
