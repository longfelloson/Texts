from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4

from auth.utils import CurrentUserDependency, get_current_user
from database import SessionWithCommit, SessionWithoutCommit
from texts import service
from texts.schemas import CreateText, Text
from users.schemas import User


router = APIRouter(prefix='/api/texts', tags=["Texts"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_text(
    data: CreateText, 
    session: SessionWithCommit,
    user: CurrentUserDependency,
):
    await service.create(data=data, created_by=user.id, session=session)

    return {"msg": "The text has been created."}
    

@router.get("", response_model=list[Text])
async def get_texts(
    session: SessionWithoutCommit,
    offset: int = 0,
    limit: int = 25,
    created_by: UUID4 = None,
    user: User = Depends(get_current_user),
):  
    if not user.is_admin:
        created_by = user.id

    texts = await service.get_all(
        limit=limit, 
        offset=offset, 
        session=session, 
        created_by=created_by
    )
    return texts


@router.get("/{text_id}", response_model=Text)
async def get_text(text_id: UUID4, session: SessionWithoutCommit):
    text = await service.get(text_id=text_id, session=session)
    if not text: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A text with this id does not exist."}],
        )
    
    if datetime.now(timezone.utc) >= text.expires_at:
        await service.delete(text_id=text_id, session=session)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The text has expired and deleted."}],
        )
    
    return text


@router.delete("/{text_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_text(text_id: UUID4, session: SessionWithCommit):
    await service.delete(text_id=text_id, session=session)
