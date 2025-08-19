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

@router.get("/dashboard/stats")
async def dashboard_stats(uid: int = Depends(current_user_id), db: Session = Depends(get_db)):
    """Get dashboard statistics for logged-in users"""
    from sqlalchemy import func, distinct
    
    
    total_models = (await db.execute(select(func.count(Model.id)))).scalar()
    
    
    total_groups = (await db.execute(select(func.count(distinct(Model.group_name))))).scalar()
    
    
    total_versions = (await db.execute(select(func.count(ModelVersion.id)))).scalar()
    
    
    total_aliases = (await db.execute(select(func.count(ModelAlias.id)))).scalar()
    
    
    from datetime import datetime, timedelta
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_models = (await db.execute(
        select(func.count(Model.id)).where(Model.created_at >= seven_days_ago)
    )).scalar()
    
    
    recent_versions = (await db.execute(
        select(func.count(ModelVersion.id)).where(ModelVersion.created_at >= seven_days_ago)
    )).scalar()
    
    
    top_groups = (await db.execute(
        select(
            Model.group_name,
            func.count(ModelVersion.id).label('version_count')
        )
        .join(ModelVersion)
        .group_by(Model.group_name)
        .order_by(func.count(ModelVersion.id).desc())
        .limit(5)
    )).all()
    
    
    latest_models = (await db.execute(
        select(Model)
        .order_by(Model.created_at.desc())
        .limit(5)
    )).scalars().all()
    
    
    latest_versions = (await db.execute(
        select(ModelVersion, Model)
        .join(Model)
        .order_by(ModelVersion.created_at.desc())
        .limit(5)
    )).all()
    
    return {
        "totals": {
            "models": total_models or 0,
            "groups": total_groups or 0,
            "versions": total_versions or 0,
            "aliases": total_aliases or 0,
        },
        "recent": {
            "models": recent_models or 0,
            "versions": recent_versions or 0,
        },
        "top_groups": [
            {
                "group_name": group.group_name,
                "version_count": group.version_count
            }
            for group in top_groups
        ],
        "latest_models": [
            {
                "name": m.name,
                "group_name": m.group_name,
                "variant": m.variant,
                "description": m.description,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in latest_models
        ],
        "latest_versions": [
            {
                "model_name": model.name,
                "group_name": model.group_name,
                "variant": model.variant,
                "version": version.version,
                "created_at": version.created_at.isoformat() if version.created_at else None,
            }
            for version, model in latest_versions
        ]
    }