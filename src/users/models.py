from sqlalchemy import UUID, Column, DateTime, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(), primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    