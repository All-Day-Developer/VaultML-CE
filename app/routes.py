
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
from fastapi.responses import StreamingResponse
import tempfile
import os
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from .s3 import presign_put, upload_file, presign_get, create_multipart_upload, presign_upload_part, complete_multipart_upload, abort_multipart_upload, list_multipart_uploads
from app.api import router
@router.get("/health")
async def health():
    return "OK"

