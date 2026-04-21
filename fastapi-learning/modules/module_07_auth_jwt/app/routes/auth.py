from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.repository.user_repository import get_user_repository
from app.schemas.auth import RegisterIn, TokenOut, UserOut
from app.services.auth_service import AuthService, EmailAlreadyUsed, InvalidCredentials

router = APIRouter(prefix="/auth", tags=["auth"])


def _service() -> AuthService:
    return AuthService(get_user_repository())


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, svc: AuthService = Depends(_service)):
    try:
        user = svc.register(email=payload.email, password=payload.password)
    except EmailAlreadyUsed:
        raise HTTPException(status.HTTP_409_CONFLICT, "email already used")
    return UserOut(id=user.id, email=user.email, roles=user.roles)


@router.post("/token", response_model=TokenOut)
def issue_token(form: OAuth2PasswordRequestForm = Depends(), svc: AuthService = Depends(_service)):
    try:
        user = svc.authenticate(email=form.username, password=form.password)
    except InvalidCredentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    token, expires_in = create_access_token(sub=str(user.id), roles=user.roles)
    return TokenOut(access_token=token, expires_in=expires_in)
