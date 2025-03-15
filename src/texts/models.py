from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from database import Base


class Text(Base):
    __tablename__ = "texts"

    id = Column(UUID(), primary_key=True)
    body = Column(String, nullable=False)
    header = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(UUID(), ForeignKey("users.id"), nullable=False)
    