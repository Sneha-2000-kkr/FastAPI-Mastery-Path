from fastapi import APIRouter, Depends

from app.dependencies.db import FakeConn, get_conn

router = APIRouter(prefix="/db-demo", tags=["dependencies"])


@router.get("")
def run_query(conn: FakeConn = Depends(get_conn)) -> dict:
    return {"result": conn.query("SELECT 1")}
