from fastapi import APIRouter, Depends

from app.dependencies.auth import require_role
from app.repository.user_repository import get_user_repository
from app.schemas.auth import UserOut

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut],
            dependencies=[Depends(require_role("admin"))])
def list_users():
    return [UserOut(id=u.id, email=u.email, roles=u.roles)
            for u in get_user_repository().list()]
