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


class CreateModelRequest(BaseModel):
    name: str
    group_name: str
    variant: str = "base"
    description: str = ""

@router.post("/models")
async def create_model(
    body: CreateModelRequest,
    uid: int = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    m = Model(
        name=body.name, 
        group_name=body.group_name,
        variant=body.variant,
        description=body.description,
        created_by=uid
    )
    db.add(m)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Model exists")
    return {"ok": True}

@router.get("/models")
async def list_models(db: Session = Depends(get_db)):
    models = (await db.execute(select(Model))).scalars().all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "group_name": m.group_name,
            "variant": m.variant,
            "description": m.description,
            "created_by": m.created_by,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in models
    ]

@router.get("/models/groups")
async def list_model_groups(db: Session = Depends(get_db)):
    """Get models grouped by group_name with their variants and latest aliases"""
    from sqlalchemy import func
    
    
    models_query = select(Model).order_by(Model.group_name, Model.variant)
    models = (await db.execute(models_query)).scalars().all()
    
    
    groups = {}
    for model in models:
        group_name = model.group_name
        if group_name not in groups:
            groups[group_name] = {
                "group_name": group_name,
                "variants": []
            }
        
        
        latest_alias_query = select(ModelAlias).where(
            ModelAlias.model_id == model.id
        ).order_by(ModelAlias.updated_at.desc()).limit(1)
        latest_alias = (await db.execute(latest_alias_query)).scalar_one_or_none()
        
        
        version_count_query = select(func.count(ModelVersion.id)).where(
            ModelVersion.model_id == model.id
        )
        version_count = (await db.execute(version_count_query)).scalar()
        
        groups[group_name]["variants"].append({
            "id": model.id,
            "name": model.name,
            "variant": model.variant,
            "description": model.description,
            "latest_alias": latest_alias.alias if latest_alias else None,
            "version_count": version_count or 0,
            "created_at": model.created_at.isoformat() if model.created_at else None,
        })
    
    return list(groups.values())

@router.get("/models/{name}")
async def get_model(name: str, db: Session = Depends(get_db)):
    """Get detailed information about a specific model"""
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")
    
    return {
        "id": m.id,
        "name": m.name,
        "group_name": m.group_name,
        "variant": m.variant,
        "description": m.description,
        "created_by": m.created_by,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    }

@router.get("/models/{name}/versions")
async def get_model_versions(name: str, db: Session = Depends(get_db)):
    """Get all versions for a specific model"""
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")
    
    versions = (await db.execute(
        select(ModelVersion).where(ModelVersion.model_id == m.id).order_by(ModelVersion.version.desc())
    )).scalars().all()
    
    return [
        {
            "id": v.id,
            "version": v.version,
            "s3_prefix": v.s3_prefix,
            "tags": v.tags,
            "created_at": v.created_at.isoformat() if v.created_at else None,
        }
        for v in versions
    ]

@router.delete("/models/{name}")
async def delete_model(
    name: str,
    uid: int = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    """Delete a model and all its versions and aliases"""
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")
    
    
    aliases = (await db.execute(
        select(ModelAlias).where(ModelAlias.model_id == m.id)
    )).scalars().all()
    for alias in aliases:
        await db.delete(alias)
    
    
    versions = (await db.execute(
        select(ModelVersion).where(ModelVersion.model_id == m.id)
    )).scalars().all()
    for version in versions:
        await db.delete(version)
    
    # Flush to ensure foreign key references are removed before deleting the model
    await db.flush()
    
    
    await db.delete(m)
    await db.commit()
    
    return {"ok": True, "message": f"Model {name} deleted successfully"}

@router.delete("/models/groups/{group_name}")
async def delete_model_group(
    group_name: str,
    uid: int = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    """Delete an entire model group and all its variants, versions, and aliases"""
    models = (await db.execute(select(Model).where(Model.group_name == group_name))).scalars().all()
    if not models:
        raise HTTPException(404, "Model group not found")
    
    deleted_models = []
    
    # Process each model in the group
    for model in models:
        # Delete aliases for this model
        aliases = (await db.execute(
            select(ModelAlias).where(ModelAlias.model_id == model.id)
        )).scalars().all()
        for alias in aliases:
            await db.delete(alias)
        
        # Delete versions for this model
        versions = (await db.execute(
            select(ModelVersion).where(ModelVersion.model_id == model.id)
        )).scalars().all()
        for version in versions:
            await db.delete(version)
        
        # Flush to ensure foreign key references are removed
        await db.flush()
        
        # Now delete the model itself
        await db.delete(model)
        deleted_models.append(f"{model.group_name}:{model.variant}")
    
    # Final commit for all changes
    await db.commit()
    
    return {
        "ok": True, 
        "message": f"Model group {group_name} deleted successfully",
        "deleted_models": deleted_models,
        "count": len(deleted_models)
    }