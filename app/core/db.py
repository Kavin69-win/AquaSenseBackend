from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Create the Async Engine
# We use settings.DATABASE_URL here to match the config.py definition
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,          # Log SQL queries to the console (great for debugging)
    future=True         # Use SQLAlchemy 2.0 style
)

# 2. Create the Session Factory
# This generates new database sessions for every request
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# 3. Create the Base Class
# All your models (SensorReading, User, etc.) will inherit from this
Base = declarative_base()

# 4. Dependency Injection Helper
# This is what you use in your API endpoints (def get_db...)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()