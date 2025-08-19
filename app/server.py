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

import uvicorn
from fastapi import FastAPI
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from passlib.hash import bcrypt
from sqlalchemy import select
from fastapi import FastAPI, Request
from colorama import Fore, Style, init as colorama_init
from app.api import router
from app.main import Session, init_db
from app.model.user import User
colorama_init(autoreset=True)

_BANNER_PRINTED = False
def print_agpl_banner():
    global _BANNER_PRINTED
    if _BANNER_PRINTED:
        return
    _BANNER_PRINTED = True

    print(
        f"\n{Fore.CYAN}{Style.BRIGHT}VaultML CE{Style.RESET_ALL}  "
        f"{Fore.MAGENTA}•{Style.RESET_ALL}  "
        f"{Fore.YELLOW}AGPL-3.0-or-later{Style.RESET_ALL}\n"
        f"{Fore.WHITE}Copyright (C) 2025  "
        f"{Fore.GREEN}All-Day Developer Marcin Wawrzków{Style.RESET_ALL}\n"
        f"{Fore.BLUE}Source:{Style.RESET_ALL} "
        f"{Fore.CYAN}https://github.com/All-Day-Developer/VaultML-CE{Style.RESET_ALL}\n"
        f"{Fore.BLUE}License:{Style.RESET_ALL} "
        f"{Fore.CYAN}https://www.gnu.org/licenses/agpl-3.0.txt{Style.RESET_ALL}\n"
    )


print_agpl_banner()
app = FastAPI(title="VaultML")
app.include_router(router)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "VaultML CE"}

@app.get("/license")
async def license_info():
    return JSONResponse({
        "name": "VaultML CE",
        "license": "AGPL-3.0-or-later",
        "source": "https://github.com/All-Day-Developer/VaultML-CE"
    })
@app.middleware("http")
async def license_header_mw(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "VaultML-CE"
    response.headers["X-App-License"] = "AGPL-3.0-or-later"
    response.headers["X-App-Source"] = "https://github.com/All-Day-Developer/VaultML-CE"
    return response

# In production (Docker), static files are copied to /app/static/
# In development, they're in ../frontend/.output/public
static_dir = os.path.join(os.path.dirname(__file__), "../static")
if not os.path.exists(static_dir):
    static_dir = os.path.join(os.path.dirname(__file__), "../frontend/.output/public")

nuxt_build_dir = static_dir


app.mount("/", StaticFiles(directory=nuxt_build_dir, html=True), name="nuxt")

@app.on_event("startup")
async def startup_event():
    await init_db()
    await create_default_user()


async def create_default_user():
    async with Session() as db:
        existing = (await db.execute(select(User).where(User.username == "default"))).scalar_one_or_none()
        if not existing:
            user = User(
                username="default",
                email="default@default",
                password_hash=bcrypt.hash("default")
            )
            db.add(user)
            await db.commit()
            print("✅ Created default user (default/default)")
        else:
            print("ℹ️ Default user already exists")


@app.get("/{full_path:path}")
async def spa_handler(full_path: str):
    return FileResponse(os.path.join(nuxt_build_dir, "index.html"))

if __name__ == "__main__":
    uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True)

