from typing import Optional

from pydantic import UUID4, EmailStr
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemas import CreateUser


async def create(*, data: CreateUser, session: AsyncSession) -> None:
    await session.execute(insert(User).values(**data.model_dump()))


async def get(*, user_id: UUID4, session: AsyncSession) -> Optional[User]:
    user = await session.execute(select(User).where(User.id == user_id))
    return user.scalar_one_or_none()


async def get_by_email(
    *, email: EmailStr, session: AsyncSession
    ) -> Optional[User]:
    user = await session.execute(select(User).where(User.email == email))
    return user.scalar_one_or_none()
