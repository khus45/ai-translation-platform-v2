from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, TokenResponse
from app.schemas.user import UserCreate
from app.security.hashing import verify_password
from app.services.token_service import TokenService
from app.services.user_service import UserService


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.user_service = UserService(db)
        self.token_service = TokenService()

    def register(self, user_in: UserCreate) -> AuthResponse:
        user = self.user_service.create_user(user_in)
        access_token, refresh_token = self._issue_token_pair(user)
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user,
        )

    def login(self, username: str, password: str) -> AuthResponse:
        user = self.repository.get_by_email_or_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        access_token, refresh_token = self._issue_token_pair(user)
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user,
        )

    def refresh(self, refresh_token: str) -> TokenResponse:
        user = self._get_user_from_refresh_token(refresh_token)
        if not self.token_service.verify_refresh_token(
            refresh_token,
            user.refresh_token_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        access_token, new_refresh_token = self._issue_token_pair(user)
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

    def logout(self, current_user: User) -> None:
        self.repository.update_refresh_token_hash(current_user, None)

    def _issue_token_pair(self, user: User) -> tuple[str, str]:
        access_token, refresh_token = self.token_service.create_token_pair(user)
        self.repository.update_refresh_token_hash(
            user,
            self.token_service.hash_refresh_token(refresh_token),
        )
        return access_token, refresh_token

    def _get_user_from_refresh_token(self, refresh_token: str) -> User:
        try:
            user_id = self.token_service.get_refresh_subject(refresh_token)
        except (KeyError, TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            ) from None

        user = self.repository.get_by_id(user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        return user
