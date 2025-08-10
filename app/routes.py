
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

from fastapi import APIRouter, Depends, HTTPException, Header, Response, Cookie, Request, UploadFile, File
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from .main import (
    Session, get_db, make_jwt, read_jwt,
    User, Model, ModelVersion, ModelAlias, settings
)
from .s3 import presign_put, upload_file, presign_get

router = APIRouter(prefix="/api")

JWT_COOKIE_NAME = "vaultml_token"

def user_from_auth(auth_header: Optional[str] = None, jwt_cookie: Optional[str] = None) -> int:
    token = None
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
    elif jwt_cookie:
        token = jwt_cookie
    if not token:
        raise HTTPException(401, "Missing token")
    return read_jwt(token)


def read_token(authorization: Optional[str], jwt_cookie: Optional[str]) -> str:
    """Pick token from Authorization: Bearer ... or from cookie."""
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ", 1)[1]
    if jwt_cookie:
        return jwt_cookie
    raise HTTPException(401, "Missing token")

def current_user_id(
    authorization: Optional[str] = Header(None),
    jwt_cookie: Optional[str] = Cookie(default=None, alias=JWT_COOKIE_NAME),
) -> int:
    token = read_token(authorization, jwt_cookie)
    return read_jwt(token)


class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/signup")
async def signup(body: SignupRequest, db: Session = Depends(get_db)):
    from passlib.hash import bcrypt
    u = User(email=body.email, username=body.email, password_hash=bcrypt.hash(body.password))
    db.add(u)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Email exists")
    return {"token": make_jwt(u.id)}  

@router.post("/auth/login")
async def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    from passlib.hash import bcrypt
    u = (await db.execute(select(User).where(User.username == body.username))).scalar_one_or_none()
    if not u or not bcrypt.verify(body.password, u.password_hash):
        raise HTTPException(401, "Bad credentials")

    token = make_jwt(u.id)
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,      
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/",
        domain="localhost",
    )
    return {"ok": True}

@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(JWT_COOKIE_NAME, path="/", domain="localhost")
    return {"ok": True}


@router.get("/auth/me")
async def me(
    authorization: Optional[str] = Header(None),
    jwt: Optional[str] = Cookie(default=None, alias=JWT_COOKIE_NAME),
):
    uid = user_from_auth(authorization, jwt)
    return {"user_id": uid}
@router.get("/debug/cookies")
async def debug_cookies(request: Request):
    return {"cookies": request.cookies}



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

@router.post("/models/{name}/versions/new")
async def create_version(
    name: str,
    files: List[UploadFile] = File(...),
    uid: int = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    """Create a new version by uploading files directly to the backend"""
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")

    
    last = (await db.execute(
        select(ModelVersion)
        .where(ModelVersion.model_id == m.id)
        .order_by(ModelVersion.version.desc())
    )).scalars().first()
    ver = (last.version + 1) if last else 1

    
    prefix = f"{name}/versions/{ver}"
    mv = ModelVersion(model_id=m.id, version=ver, s3_prefix=prefix, tags={})
    db.add(mv)
    await db.commit()

    
    uploaded_files = []
    try:
        for file in files:
            
            file_content = await file.read()
            
            
            key = f"{prefix}/{file.filename}"
            
            
            s3_url = upload_file(
                file_content=file_content,
                key=key,
                content_type=file.content_type or "application/octet-stream"
            )
            
            uploaded_files.append({
                "filename": file.filename,
                "size": len(file_content),
                "s3_key": key,
                "s3_url": s3_url,
                "content_type": file.content_type
            })
    
    except Exception as e:
        
        await db.delete(mv)
        await db.commit()
        raise HTTPException(500, f"File upload failed: {str(e)}")

    return {
        "version": ver,
        "s3_prefix": prefix,
        "uploaded_files": uploaded_files,
        "message": f"Successfully uploaded {len(uploaded_files)} files for version {ver}"
    }

@router.get("/models/{name}/versions/{version}/download")
async def list_version_files(
    name: str,
    version: int,
    db: Session = Depends(get_db),
):
    """List files in a version for download"""
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")

    mv = (await db.execute(
        select(ModelVersion).where(
            ModelVersion.model_id == m.id,
            ModelVersion.version == version
        )
    )).scalar_one_or_none()
    if not mv:
        raise HTTPException(404, "Version not found")

    
    from botocore.exceptions import ClientError
    from .s3 import s3_client
    s3 = s3_client()
    
    try:
        response = s3.list_objects_v2(
            Bucket=settings.S3_BUCKET,
            Prefix=f"{mv.s3_prefix}/"
        )
        
        if 'Contents' not in response:
            return {
                "version": version,
                "s3_prefix": mv.s3_prefix,
                "files": [],
                "message": "No files found for this version"
            }
        
        files = []
        for obj in response['Contents']:
            key = obj['Key']
            filename = key.split('/')[-1]  
            if filename:  
                files.append({
                    "filename": filename,
                    "size": obj['Size'],
                    "last_modified": obj['LastModified'].isoformat(),
                    "s3_key": key,
                    "download_url": f"/api/models/{name}/versions/{version}/download/{filename}"
                })
        
        return {
            "version": version,
            "s3_prefix": mv.s3_prefix,
            "files": files,
            "message": f"Found {len(files)} files for download"
        }
        
    except ClientError as e:
        raise HTTPException(500, f"Failed to list files: {str(e)}")

@router.get("/models/{name}/versions/{version}/download/{filename}")
async def download_file(
    name: str,
    version: int,
    filename: str,
    db: Session = Depends(get_db),
):
    """Download a specific file from a version"""
    from fastapi.responses import StreamingResponse
    import io
    
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")

    mv = (await db.execute(
        select(ModelVersion).where(
            ModelVersion.model_id == m.id,
            ModelVersion.version == version
        )
    )).scalar_one_or_none()
    if not mv:
        raise HTTPException(404, "Version not found")

    
    from botocore.exceptions import ClientError
    from .s3 import s3_client
    s3 = s3_client()
    
    try:
        key = f"{mv.s3_prefix}/{filename}"
        response = s3.get_object(Bucket=settings.S3_BUCKET, Key=key)
        
        
        def generate():
            for chunk in response['Body'].iter_chunks(chunk_size=8192):
                yield chunk
        
        return StreamingResponse(
            generate(),
            media_type=response.get('ContentType', 'application/octet-stream'),
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(404, f"File {filename} not found")
        raise HTTPException(500, f"Failed to download file: {str(e)}")

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

@router.get("/health")
async def health():
    return "OK"

