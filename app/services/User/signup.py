from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.db.models.User.user_core import User
from app.schemas.User.signup import SignupRequestOTP    


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(data: SignupRequestOTP, db: AsyncSession) -> User:

    stmt = select(User).where(
        (User.phone == data.phone) 
    )
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ValueError("User with this phone number already exists")
    
    

