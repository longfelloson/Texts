from fastapi import APIRouter, HTTPException, status

from auth.password import get_hashed_password
from auth.utils import CurrentUserDependency
from database import SessionWithCommit
from users import service
from users.schemas import CreateUser, User, UserCredentials


router = APIRouter(prefix="/api/users")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    credentials: UserCredentials, session: SessionWithCommit
):
    """Creates a user with given credentials"""
    user = await service.get_by_email(email=credentials.email, session=session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User with this email alredy exists"
        )
    
    hashed_password = get_hashed_password(credentials.password)
    user = CreateUser(email=credentials.email, hashed_password=hashed_password)

    await service.create(data=user, session= session)

    return {"msg": "User has been created"}


@router.get("/me", response_class=User)
async def read_users_me(user: CurrentUserDependency):
    return user
