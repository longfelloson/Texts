from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from auth.token import decode_access_token
from database import SessionWithoutCommit
from users import service
from users.schemas import User as UserSchema


async def get_current_user(
    request: Request, session: SessionWithoutCommit
) -> UserSchema:
    payload = decode_access_token(token=request.cookies.get("token"))
    user = await service.get_by_email(email=payload["sub"], session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserSchema(**user.__dict__)


CurrentUserDependency = Annotated[UserSchema, Depends(get_current_user)]
