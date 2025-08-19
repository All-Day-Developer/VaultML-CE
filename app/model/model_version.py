from app.model.base import Base
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from typing import Dict

class ModelVersion(Base):
    __tablename__ = "model_versions"
    __table_args__ = (UniqueConstraint("model_id", "version"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"))
    version: Mapped[int] = mapped_column(Integer)
    s3_prefix: Mapped[str] = mapped_column(String(1024))
    tags: Mapped[Dict] = mapped_column(JSON, default={})
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())