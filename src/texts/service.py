from datetime import datetime, timezone
from typing import Optional
from pydantic import UUID4
from sqlalchemy import (
    and_, 
    desc, 
    insert, 
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
    stmt = select(Text).where(Text.expires_at > datetime.now(timezone.utc))
    if created_by:
        stmt = stmt.where(
            and_(
                Text.created_by == created_by, 
                Text.expires_at > datetime.now(timezone.utc),
            )
        )

    texts = await session.execute(
        stmt
        .order_by(desc(Text.created_at))
        .limit(limit)
        .offset(offset)
    )
    return texts.scalars().all()


async def delete(*, text_id: UUID4, session: AsyncSession) -> None:
    await session.execute(delete_(Text).where(Text.id == text_id))
