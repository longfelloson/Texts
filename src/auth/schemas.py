from pydantic import BaseModel


class AccessToken(BaseModel):
    type: str = "Bearer"
    access_token: str
