from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser, get_active_user

router = APIRouter(tags=["me"])


@router.get("/me")
def me(user: CurrentUser = Depends(get_active_user)) -> dict:
    return {"id": user.id, "email": user.email, "active": user.is_active}
