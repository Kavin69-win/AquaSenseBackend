from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Updated with your specific credentials:
# User: postgres
# Password: kavinsharma
# Host: localhost:5432
# Database: AquaSense
DATABASE_URL = "postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense"

# Create the Async Engine
# echo=True is great for debugging—it shows the SQL in your terminal
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the Session Factory
# This 'SessionLocal' is what deps.py uses to talk to the DB
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)