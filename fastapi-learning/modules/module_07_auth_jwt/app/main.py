from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.repository.user_repository import get_user_repository
from app.routes import admin, auth, me
from app.services.auth_service import AuthService, EmailAlreadyUsed


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed an admin user (dev only)
    svc = AuthService(get_user_repository())
    try:
        svc.register(email="admin@example.com", password="Admin!Pass1", roles=["user", "admin"])
    except EmailAlreadyUsed:
        pass
    yield


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version, lifespan=lifespan)
    app.include_router(auth.router)
    app.include_router(me.router)
    app.include_router(admin.router)
    return app


app = create_app()
