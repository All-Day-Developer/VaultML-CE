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

import uvicorn, asyncio
from fastapi import FastAPI
from app.api import router
from .main import init_db

app = FastAPI(title="ModelHub")
app.include_router(router)

@app.on_event("startup")
async def _startup():
    await init_db()

if __name__ == "__main__":
    uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True)

