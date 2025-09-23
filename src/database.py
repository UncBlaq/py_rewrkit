import os
import ssl
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
ENV = os.getenv("ENV", "development")

DATABASE_URL = os.getenv("DATABASE_URL")

ssl_context = ssl.create_default_context(cafile=None)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for SQLAlchemy engine")

if ENV == "production":
    ssl_context = ssl.create_default_context()
    connect_args = {"ssl": ssl_context}
else:
    connect_args = {"ssl": False}


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args
)


SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Use AsyncSession
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

# Dependency to provide the async session
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

db_dependency = Annotated[AsyncSession, Depends(get_db)]

