from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(select(User).where(User.username == username))

    def get_by_email_or_username(self, identifier: str) -> User | None:
        return self.db.scalar(
            select(User).where(
                (User.email == identifier) | (User.username == identifier)
            )
        )

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return list(self.db.scalars(select(User).offset(skip).limit(limit)).all())

    def create(
        self,
        *,
        username: str,
        email: str,
        hashed_password: str,
        role: str = "user",
    ) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_refresh_token_hash(
        self,
        user: User,
        refresh_token_hash: str | None,
    ) -> User:
        user.refresh_token_hash = refresh_token_hash
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
