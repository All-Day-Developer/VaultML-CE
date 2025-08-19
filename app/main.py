
# Copyright (C) 2025 All-Day Developer Marcin Wawrzków
# contributor: Marcin Wawrzków
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from pydantic_settings import BaseSettings
from sqlalchemy import (
    String, Integer, JSON, DateTime, UniqueConstraint, ForeignKey, func
)
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from typing import Dict
import time, jwt
from fastapi import HTTPException

from app.model.base import Base

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    S3_ENDPOINT: str
    S3_REGION: str = "us-east-1"
    S3_BUCKET: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    DOMAIN_NAME: str

settings = Settings()


engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def make_jwt(user_id: int):
    payload = {"sub": str(user_id), "iat": int(time.time())}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def read_jwt(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return int(payload["sub"])
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_db():
    async with Session() as s:
        yield s

