import jwt
from .models import User
from .serializers import UserValidationError
from datetime import datetime, timedelta
from django.conf import settings

class AuthService:
    JWT_ALGORITHM = "HS256"
    JWT_AUDIENCE = "hammer:auth"
    JWT_TOKEN_PREFIX = "Bearer"
    JWT_EXPIRES = 5

    def create_access_token_for_user(self, user: User):
        token_payload = {
            "aud": self.JWT_AUDIENCE,
            "iat": datetime.timestamp(datetime.utcnow()),
            "exp": datetime.timestamp(datetime.utcnow() + timedelta(minutes=self.JWT_EXPIRES)),
            "phone_number": user.phone_number, 
            "identifier": user.identifier,
            "id": user.id
        }
        access_token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm=self.JWT_ALGORITHM)
        return access_token

    def create_refresh_token_for_user(self, user: User, expires_in: int = 60 * 24 * 365):
        token_payload = {
            "aud": self.JWT_AUDIENCE,
            "iat": datetime.timestamp(datetime.utcnow()),
            "exp": datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
            "phone_number": user.phone_number, 
            "identifier": user.identifier,
            "id": user.id
        }

        refresh_token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm=self.JWT_ALGORITHM)
        return refresh_token

    def get_user_from_token(self, *, token: str):
        """Takes in JWT token. Returns user (encoded in token) || 401"""
        try:
            decoded_token = jwt.decode(token, str(settings.SECRET_KEY), audience=self.JWT_AUDIENCE, algorithms=[self.JWT_ALGORITHM])
            payload = User(id=decoded_token["id"], phone_number=decoded_token["phone_number"], identifier=decoded_token["identifier"])
        except Exception as e:
            raise UserValidationError()
        return payload