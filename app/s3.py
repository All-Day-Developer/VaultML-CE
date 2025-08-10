
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

import boto3
from .main import settings

def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
    )

def presign_put(key: str, content_type: str = "application/octet-stream", expires=3600):
    s3 = s3_client()
    return s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=expires,
    )

def ensure_bucket_exists():
    """Create bucket if it doesn't exist"""
    s3 = s3_client()
    try:
        s3.head_bucket(Bucket=settings.S3_BUCKET)
    except Exception:
        try:
            s3.create_bucket(Bucket=settings.S3_BUCKET)
        except Exception as e:
            print(f"Warning: Could not create bucket {settings.S3_BUCKET}: {e}")

def upload_file(file_content: bytes, key: str, content_type: str = "application/octet-stream"):
    """Upload file content directly to S3"""
    ensure_bucket_exists()
    s3 = s3_client()
    s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=file_content,
        ContentType=content_type
    )
    return f"s3://{settings.S3_BUCKET}/{key}"

def presign_get(key: str, expires=3600):
    """Generate presigned URL for downloading files"""
    s3 = s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": key},
        ExpiresIn=expires,
    )

