from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.common import get_user_service
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED,
             response_model_by_alias=True)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
