from datetime import datetime, timezone
from typing import Optional
from pydantic import UUID4
from sqlalchemy import (
    desc, 
    insert,
    or_,
    select, 
    delete as delete_, 
)
from sqlalchemy.ext.asyncio import AsyncSession

from texts.schemas import CreateText
from texts.models import Text


async def create(
    *, 
    data: CreateText, 
    session: AsyncSession,
    created_by: UUID4,
) -> None:
    await session.execute(
        insert(Text).values(**data.model_dump(), created_by=created_by)
    )


async def get(*, text_id: UUID4, session: AsyncSession) -> Optional[Text]:
    text = await session.execute(select(Text).where(Text.id == text_id))
    return text.scalar_one_or_none()


async def get_all(
    *, 
    offset: int, 
    limit: int, 
    session: AsyncSession,
    created_by: UUID4 = None,
) -> list[Text]:
    stmt = select(Text).where(
        or_(
            Text.expires_at > datetime.now(timezone.utc), 
            Text.expires_at.is_(None),
        ),
        Text.created_by == created_by,
    )
    if created_by:
        stmt = stmt.where(Text.created_by == created_by)

    texts = await session.execute(
        stmt
        .order_by(desc(Text.created_at))
        .limit(limit)
        .offset(offset)
    )
    return texts.scalars().all()


async def delete(*, text_id: UUID4, session: AsyncSession) -> None:
    await session.execute(delete_(Text).where(Text.id == text_id))
