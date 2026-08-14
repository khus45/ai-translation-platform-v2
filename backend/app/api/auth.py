from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.auth import AuthResponse, RefreshTokenRequest, TokenResponse
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> AuthResponse:
    return AuthService(db).register(user_in)


@router.post("/login", response_model=AuthResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> AuthResponse:
    return AuthService(db).login(form_data.username, form_data.password)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    token_in: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return AuthService(db).refresh(token_in.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Response:
    AuthService(db).logout(current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/oauth/google")
def google_oauth_placeholder():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Google OAuth connector placeholder. "
            "Configure OAuth client secrets before production use."
        ),
    )


@router.get("/oauth/microsoft")
def microsoft_oauth_placeholder():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Microsoft OAuth connector placeholder. "
            "Configure OAuth client secrets before production use."
        ),
    )
