from fastapi import APIRouter, Depends, HTTPException, Header, Response, Cookie, Request, UploadFile, File
from fastapi.responses import StreamingResponse
import tempfile
import os
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from app.main import Session, get_db, settings
from app.model.model import Model
from app.model.model_alias import ModelAlias
from app.model.model_version import ModelVersion
from app.s3 import presign_put, upload_file, presign_get, create_multipart_upload, presign_upload_part, complete_multipart_upload, abort_multipart_upload, list_multipart_uploads
from app.api import router
from app.api.auth import current_user_id

@router.get("/models/{name}/resolve")
async def resolve(name: str, version: Optional[int] = None, alias: Optional[str] = None,
                  db: Session = Depends(get_db)):
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")

    if version is not None:
        mv = (await db.execute(
            select(ModelVersion).where(
                ModelVersion.model_id == m.id, ModelVersion.version == version
            )
        )).scalar_one_or_none()
    elif alias:
        a = (await db.execute(
            select(ModelAlias).where(
                ModelAlias.model_id == m.id, ModelAlias.alias == alias
            )
        )).scalar_one_or_none()
        if not a:
            raise HTTPException(404, "Alias not found")
        mv = (await db.execute(
            select(ModelVersion).where(ModelVersion.id == a.version_id)
        )).scalar_one()
    else:
        raise HTTPException(400, "Provide version or alias")

    if not mv:
        raise HTTPException(404, "Version not found")

    return {
        "name": name,
        "group_name": m.group_name,
        "variant": m.variant,
        "version": mv.version,
        "s3_prefix": f"s3://{settings.S3_BUCKET}/{mv.s3_prefix}",
        "endpoint": settings.S3_ENDPOINT,
        "display_name": f"{m.group_name}:{m.variant}@{alias}" if alias else f"{m.group_name}:{m.variant}@v{mv.version}",
    }

@router.get("/resolve/{group_name}/{variant}")
async def resolve_by_group_variant(
    group_name: str, 
    variant: str,
    alias: Optional[str] = None,
    version: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Resolve model by group:variant@alias format (e.g., Bielik:7b@Prod)"""
    
    
    model_name = f"{group_name}:{variant}"
    m = (await db.execute(
        select(Model).where(
            Model.group_name == group_name, 
            Model.variant == variant
        )
    )).scalar_one_or_none()
    
    if not m:
        raise HTTPException(404, f"Model {group_name}:{variant} not found")

    
    if alias:
        a = (await db.execute(
            select(ModelAlias).where(
                ModelAlias.model_id == m.id, ModelAlias.alias == alias
            )
        )).scalar_one_or_none()
        if not a:
            raise HTTPException(404, f"Alias '{alias}' not found for {group_name}:{variant}")
        mv = (await db.execute(
            select(ModelVersion).where(ModelVersion.id == a.version_id)
        )).scalar_one()
    elif version is not None:
        mv = (await db.execute(
            select(ModelVersion).where(
                ModelVersion.model_id == m.id, ModelVersion.version == version
            )
        )).scalar_one_or_none()
        if not mv:
            raise HTTPException(404, f"Version {version} not found for {group_name}:{variant}")
    else:
        
        mv = (await db.execute(
            select(ModelVersion).where(
                ModelVersion.model_id == m.id
            ).order_by(ModelVersion.version.desc()).limit(1)
        )).scalar_one_or_none()
        if not mv:
            raise HTTPException(404, f"No versions found for {group_name}:{variant}")

    return {
        "name": m.name,
        "group_name": m.group_name,
        "variant": m.variant,
        "version": mv.version,
        "s3_prefix": f"s3://{settings.S3_BUCKET}/{mv.s3_prefix}",
        "endpoint": settings.S3_ENDPOINT,
        "display_name": f"{group_name}:{variant}@{alias}" if alias else f"{group_name}:{variant}@v{mv.version}",
    }