from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from firebase_admin import auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return (AnonymousUser(), None)

        id_token = auth_header.split(" ").pop()
        try:
            decoded_token = auth.verify_id_token(id_token)
            user_id = decoded_token.get("uid")

            # Firebase 사용자 ID로 Django 사용자 조회 또는 생성
            try:
                user = User.objects.get(username=user_id)
            except User.DoesNotExist:
                # 새 사용자 생성
                user = User.objects.create_user(
                    username=user_id,
                    email=decoded_token.get("email", ""),
                    password=None,  # Firebase에서 인증하므로 비밀번호 불필요
                )

            return (user, None)
        except Exception:
            raise AuthenticationFailed("Invalid token")
