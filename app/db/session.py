from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # ← use central config

# Use DATABASE_URL from settings (Render env or local env)
DATABASE_URL = settings.DATABASE_URL

# Create Async Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Create Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
