from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.schemas.auth import UserCreate, UserResponse
from app.models.user import User, Village
from app.core.i18n import get_message

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    accept_language: str = Header("en", alias="Accept-Language"),
    db: AsyncSession = Depends(get_db)
):
    # 1. Look up the Village
    stmt = select(Village).where(Village.name.ilike(user_in.village))
    result = await db.execute(stmt)
    village = result.scalars().first()

    if not village:
        raise HTTPException(
            status_code=404,
            detail=f"Village '{user_in.village}' not found in supported regions."
        )

    # 2. NEW: Check for existing phone number
    # This prevents the database from throwing an unhandled IntegrityError
    existing_user_stmt = select(User).where(User.phone_number == user_in.phone_number)
    existing_user_result = await db.execute(existing_user_stmt)
    if existing_user_result.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="This phone number is already registered."
        )

    # 3. Create the User (Updated with phone_number)
    new_user = User(
        full_name=user_in.name,
        role=user_in.role,
        phone_number=user_in.phone_number,  # <--- THE MISSING LINK IS NOW HERE
        village_id=village.id
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # 4. Generate Localized Response
    msg_text = get_message("welcome", lang=accept_language, id=new_user.id)

    # Return the response (UserResponse schema will now show the phone number too)
    return UserResponse(
        id=new_user.id, 
        phone_number=new_user.phone_number, 
        msg=msg_text
    )