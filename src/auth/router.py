from fastapi import APIRouter, HTTPException, status

from auth.password import get_hashed_password, verify_password
from auth.schemas import AccessToken
from auth.token import create_access_token
from database import SessionWithoutCommit
from users import service
from users.schemas import UserCredentials


router = APIRouter(prefix="/api")


@router.post("/token", response_model=AccessToken)
async def get_access_token(
    credentials: UserCredentials, session: SessionWithoutCommit
):
    user = await service.get_by_email(email=credentials.email, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email doesn't exists"
        )
    
    hashed_password = get_hashed_password(credentials.password)
    if not verify_password(credentials.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect password"
        )
    
    access_token: AccessToken = create_access_token(data={"sub": user.email})
    return access_token
