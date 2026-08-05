from hashlib import sha256
from hmac import compare_digest

from app.models.user import User
from app.security.jwt import (
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_token_type,
)


class TokenService:
    def create_token_pair(self, user: User) -> tuple[str, str]:
        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role},
        )
        refresh_token = create_refresh_token(subject=str(user.id))
        return access_token, refresh_token

    def hash_refresh_token(self, refresh_token: str) -> str:
        return sha256(refresh_token.encode("utf-8")).hexdigest()

    def verify_refresh_token(self, refresh_token: str, token_hash: str | None) -> bool:
        if token_hash is None:
            return False
        return compare_digest(self.hash_refresh_token(refresh_token), token_hash)

    def get_refresh_subject(self, refresh_token: str) -> int:
        payload = decode_token(refresh_token)
        validate_token_type(payload, REFRESH_TOKEN_TYPE)
        return int(payload["sub"])
