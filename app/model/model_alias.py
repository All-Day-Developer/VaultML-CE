from app.model.base import Base
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from typing import Dict


class ModelAlias(Base):
    __tablename__ = "model_aliases"
    __table_args__ = (UniqueConstraint("model_id", "alias"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"))
    alias: Mapped[str] = mapped_column(String(64))
    version_id: Mapped[int] = mapped_column(ForeignKey("model_versions.id"))
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())