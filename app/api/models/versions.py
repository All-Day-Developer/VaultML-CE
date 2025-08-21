from fastapi import APIRouter, Depends, HTTPException, Header, Response, Cookie, Request, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
import tempfile
import os
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from app.main import Session, get_db, settings
from app.model.model import Model
from app.model.model_version import ModelVersion
from app.s3 import presign_put, upload_file, presign_get, create_multipart_upload, presign_upload_part, complete_multipart_upload, abort_multipart_upload, list_multipart_uploads
from app.api import router
from app.api.auth import current_user_id

@router.post("/models/{name}/versions/declare")
async def declare_version(
    name: str,
    uid: int = Depends(current_user_id),
    db = Depends(get_db),
):
    """Declare a new version for a model"""
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

    return {
        "version": ver,
        "s3_prefix": prefix,
        "message": f"Declared new version {ver} for model {name}"
    }

@router.post("/models/{name}/versions/new")
async def create_version(
    name: str,
    version_query: Optional[int] = Query(None),
    version_form: Optional[int] = Form(None),
    files: List[UploadFile] = File(...),
    uid: int = Depends(current_user_id),
    db = Depends(get_db),
):
    """Create a new version by uploading files directly to the backend"""

    version = version_query if version_query is not None else version_form
    if version is None:
        raise HTTPException(400, "Version not provided")

    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")

    # Require that the client previously declared this version
    mv = (await db.execute(
        select(ModelVersion).where(
            ModelVersion.model_id == m.id,
            ModelVersion.version == version
        )
    )).scalar_one_or_none()
    if not mv:
        raise HTTPException(404, "Version not declared")

    
    uploaded_files = []
    try:
        prefix = mv.s3_prefix
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
        "version": version,
        "s3_prefix": mv.s3_prefix,
        "uploaded_files": uploaded_files,
        "message": f"Successfully uploaded {len(uploaded_files)} files for version {version}"
    }


class InitiateMultipartRequest(BaseModel):
    filename: str
    content_type: str = "application/octet-stream"


@router.post("/models/{name}/versions/{version}/chunked/initiate")
async def initiate_chunked_upload(
    name: str,
    version: int,
    body: InitiateMultipartRequest,
    uid: int = Depends(current_user_id),
    db = Depends(get_db)
):
    """Initiate chunked upload for a new version"""
    m = (await db.execute(select(Model).where(Model.name == name))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Model not found")
    # The version must already be declared by the client. Update its tags to mark chunked upload.
    mv = (await db.execute(
        select(ModelVersion).where(
            ModelVersion.model_id == m.id,
            ModelVersion.version == version
        )
    )).scalar_one_or_none()
    if not mv:
        raise HTTPException(404, "Version not declared")

    try:
        prefix = mv.s3_prefix
        # Update tags on the existing ModelVersion to indicate a chunked upload is in progress
        tags = mv.tags.copy() if mv.tags else {}
        tags.update({
            "chunked_upload": True,
            "filename": body.filename,
            "content_type": body.content_type,
            "status": "uploading"
        })
        mv.tags = tags
        await db.commit()

        return {
            "s3_prefix": prefix,
            "chunk_size": 100 * 1024 * 1024,  # 100MB recommended
            "max_chunks": 10000
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to initiate chunked upload: {str(e)}")

@router.put("/models/{name}/versions/{version}/chunks/{chunk_number}")
async def upload_chunk(
    name: str,
    version: int,
    chunk_number: int,
    chunk: UploadFile = File(...),
    uid: int = Depends(current_user_id),
    db = Depends(get_db),
):
    """Upload a file chunk to be stored temporarily and combined later"""
    if chunk_number < 1 or chunk_number > 10000:
        raise HTTPException(400, "Chunk number must be between 1 and 10000")
    
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
    
    if not mv.tags.get("chunked_upload"):
        raise HTTPException(400, "Invalid chunked upload")
    
    try:
        # Create a directory for storing chunks for this upload
        chunks_dir = f"/tmp/vaultml_chunks/{name}_v{version}"
        os.makedirs(chunks_dir, exist_ok=True)
        
        chunk_file_path = f"{chunks_dir}/chunk_{chunk_number:06d}"
        
        # Save chunk to temporary file
        with open(chunk_file_path, 'wb') as chunk_file:
            chunk_size = 8192  # 8KB chunks for streaming
            total_size = 0
            
            while chunk_data := await chunk.read(chunk_size):
                chunk_file.write(chunk_data)
                total_size += len(chunk_data)
        
        # Store chunk info in the model version tags
        # Need to reassign the entire tags dict for SQLAlchemy to detect changes
        tags = mv.tags.copy()
        if 'uploaded_chunks' not in tags:
            tags['uploaded_chunks'] = {}
        tags['uploaded_chunks'][str(chunk_number)] = {
            'file_path': chunk_file_path,
            'size': total_size
        }
        mv.tags = tags
        await db.commit()
        
        return {
            "chunk_number": chunk_number,
            "size": total_size,
            "message": f"Chunk {chunk_number} uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to upload chunk {chunk_number}: {str(e)}")

@router.post("/models/{name}/versions/{version}/chunked/complete")
async def complete_chunked_upload(
    name: str,
    version: int,
    uid: int = Depends(current_user_id),
    db = Depends(get_db),
):
    """Combine all uploaded chunks and upload complete file to S3"""
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
    
    if not mv.tags.get("chunked_upload"):
        raise HTTPException(400, "Invalid chunked upload")
    
    filename = mv.tags.get("filename")
    content_type = mv.tags.get("content_type", "application/octet-stream")
    key = f"{mv.s3_prefix}/{filename}"
    uploaded_chunks = mv.tags.get("uploaded_chunks", {})
    
    if not uploaded_chunks:
        raise HTTPException(400, "No chunks uploaded yet")
    
    try:
        # Sort chunks by chunk number
        chunk_numbers = sorted([int(num) for num in uploaded_chunks.keys()])
        
        # Create temporary file to combine all chunks
        with tempfile.NamedTemporaryFile(delete=False) as combined_file:
            try:
                total_size = 0
                
                # Combine all chunks into one file
                for chunk_num in chunk_numbers:
                    chunk_info = uploaded_chunks[str(chunk_num)]
                    chunk_file_path = chunk_info['file_path']
                    
                    if not os.path.exists(chunk_file_path):
                        raise HTTPException(500, f"Chunk {chunk_num} file not found")
                    
                    # Copy chunk data to combined file
                    with open(chunk_file_path, 'rb') as chunk_file:
                        while chunk_data := chunk_file.read(8192):
                            combined_file.write(chunk_data)
                            total_size += len(chunk_data)
                
                combined_file.flush()
                
                # Upload the complete file to S3
                from app.s3 import upload_file
                
                with open(combined_file.name, 'rb') as complete_file:
                    file_content = complete_file.read()
                    s3_url = upload_file(
                        file_content=file_content,
                        key=key,
                        content_type=content_type
                    )
                
                # Clean up chunk files and directory
                chunks_dir = f"/tmp/vaultml_chunks/{name}_v{version}"
                try:
                    # First, remove all chunk files
                    for chunk_num in chunk_numbers:
                        chunk_info = uploaded_chunks[str(chunk_num)]
                        chunk_file_path = chunk_info['file_path']
                        if os.path.exists(chunk_file_path):
                            os.unlink(chunk_file_path)
                    
                    # Then remove any remaining files in the directory
                    if os.path.exists(chunks_dir):
                        import shutil
                        shutil.rmtree(chunks_dir)
                        
                except Exception as cleanup_error:
                    # Log cleanup error but don't fail the upload
                    print(f"Warning: Failed to cleanup chunks directory: {cleanup_error}")
                    # Continue with the upload completion
                
                # Update model version status
                # Need to reassign the entire tags dict for SQLAlchemy to detect changes
                tags = mv.tags.copy()
                tags.update({
                    "status": "completed",
                    "s3_url": s3_url,
                    "total_size": total_size,
                    "total_chunks": len(chunk_numbers)
                })
                # Clear chunk info since we don't need it anymore
                if 'uploaded_chunks' in tags:
                    del tags['uploaded_chunks']
                mv.tags = tags
                await db.commit()
                
                return {
                    "version": version,
                    "s3_key": key,
                    "s3_prefix": mv.s3_prefix,
                    "s3_url": s3_url,
                    "total_size": total_size,
                    "total_chunks": len(chunk_numbers),
                    "message": f"Successfully combined {len(chunk_numbers)} chunks and uploaded to S3"
                }
                
            finally:
                # Clean up combined temp file
                if os.path.exists(combined_file.name):
                    os.unlink(combined_file.name)
        
    except Exception as e:
        raise HTTPException(500, f"Failed to complete chunked upload: {str(e)}")

@router.delete("/models/{name}/versions/{version}/chunked/abort")
async def abort_chunked_upload(
    name: str,
    version: int,
    uid: int = Depends(current_user_id),
    db = Depends(get_db),
):
    """Abort chunked upload and clean up temporary files"""
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
    
    if not mv.tags.get("chunked_upload"):
        raise HTTPException(400, "Invalid chunked upload")
    
    try:
        # Clean up any uploaded chunks
        uploaded_chunks = mv.tags.get("uploaded_chunks", {})
        chunks_dir = f"/tmp/vaultml_chunks/{name}_v{version}"
        
        try:
            # Remove individual chunk files first
            for chunk_num, chunk_info in uploaded_chunks.items():
                chunk_file_path = chunk_info['file_path']
                if os.path.exists(chunk_file_path):
                    os.unlink(chunk_file_path)
            
            # Remove entire directory and any remaining files
            if os.path.exists(chunks_dir):
                import shutil
                shutil.rmtree(chunks_dir)
                
        except Exception as cleanup_error:
            # Log cleanup error but don't fail the abort
            print(f"Warning: Failed to cleanup chunks during abort: {cleanup_error}")
        
        # Delete the model version record
        await db.delete(mv)
        await db.commit()
        
        return {"message": "Chunked upload aborted successfully"}
    except Exception as e:
        raise HTTPException(500, f"Failed to abort chunked upload: {str(e)}")

@router.get("/multipart/uploads")
async def list_ongoing_uploads(uid: int = Depends(current_user_id)):
    """List ongoing multipart uploads"""
    try:
        uploads = list_multipart_uploads()
        return uploads
    except Exception as e:
        raise HTTPException(500, f"Failed to list uploads: {str(e)}")
    

@router.get("/models/{name}/versions/{version}/download")
async def list_version_files(
    name: str,
    version: int,
    db = Depends(get_db),
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
    from app.s3 import s3_client
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
    db = Depends(get_db),
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
    from app.s3 import s3_client
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
    
