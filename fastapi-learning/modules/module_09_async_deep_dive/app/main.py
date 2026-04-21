from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import cpu, fanout, timeout


@asynccontextmanager
async def lifespan(app: FastAPI):
    s = get_settings()
    app.state.cpu_pool = ProcessPoolExecutor(max_workers=s.cpu_workers)
    try:
        yield
    finally:
        app.state.cpu_pool.shutdown(wait=False, cancel_futures=True)


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title=s.app_name, version=s.version, lifespan=lifespan)
    app.include_router(fanout.router)
    app.include_router(timeout.router)
    app.include_router(cpu.router)
    return app


app = create_app()
