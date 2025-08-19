from fastapi import APIRouter, Depends, HTTPException, Header, Response, Cookie, Request, UploadFile, File
from fastapi.responses import StreamingResponse
import tempfile
import os
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from app.main import Session, get_db
from app.model.model import Model
from app.model.model_alias import ModelAlias
from app.model.model_version import ModelVersion
from app.s3 import presign_put, upload_file, presign_get, create_multipart_upload, presign_upload_part, complete_multipart_upload, abort_multipart_upload, list_multipart_uploads
from app.api import router
from app.api.auth import current_user_id


@router.post("/models/{name}/aliases/{alias}")
async def set_alias(
    name: str, alias: str, version: int,
    uid: int = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")
    mv = (await db.execute(
        select(ModelVersion).where(
            ModelVersion.model_id == m.id, ModelVersion.version == version
        )
    )).scalar_one_or_none()
    if not mv:
        raise HTTPException(404, "Version not found")

    existing = (await db.execute(
        select(ModelAlias).where(
            ModelAlias.model_id == m.id, ModelAlias.alias == alias
        )
    )).scalar_one_or_none()
    if existing:
        existing.version_id = mv.id
    else:
        db.add(ModelAlias(model_id=m.id, alias=alias, version_id=mv.id))
    await db.commit()
    return {"ok": True}

@router.get("/models/{name}/aliases")
async def get_aliases(name: str, db: Session = Depends(get_db)):
    """Get all aliases for a model"""
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")
    
    aliases = (await db.execute(
        select(ModelAlias, ModelVersion).join(ModelVersion).where(
            ModelAlias.model_id == m.id
        ).order_by(ModelAlias.updated_at.desc())
    )).all()
    
    return [
        {
            "alias": alias.alias,
            "version": version.version,
            "updated_at": alias.updated_at.isoformat() if alias.updated_at else None,
        }
        for alias, version in aliases
    ]

@router.delete("/models/{name}/aliases/{alias}")
async def delete_alias(
    name: str, alias: str,
    uid: int = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    """Delete an alias"""
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")
    
    existing = (await db.execute(
        select(ModelAlias).where(
            ModelAlias.model_id == m.id, ModelAlias.alias == alias
        )
    )).scalar_one_or_none()
    
    if not existing:
        raise HTTPException(404, "Alias not found")
    
    await db.delete(existing)
    await db.commit()
    return {"ok": True}
