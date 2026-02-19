from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal

# 1. Database Dependency
# This opens a connection when a request starts and closes it when it ends
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# 2. User Identity Dependency (Real-World Mode)
# This looks for the 'X-User-ID' header in the incoming request
async def get_current_user_id(x_user_id: int = Header(..., description="The ID of the farmer")):
    """
    Extracts the Farmer ID from the 'X-User-ID' Header.
    If the header is missing, FastAPI will automatically return a 422 error.
    """
    if not x_user_id:
        raise HTTPException(
            status_code=401, 
            detail="User identity missing. Please provide X-User-ID in headers."
        )
    return x_user_id