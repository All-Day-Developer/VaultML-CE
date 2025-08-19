
from fastapi import APIRouter

router = APIRouter(prefix="/api")
 
# Import api submodules so their route decorators run and register handlers on `router`
from . import auth  # noqa: F401  (imports for side-effects)
from .models import (
    aliases,
    dashboard, 
    management, 
    resolve, 
    versions
)