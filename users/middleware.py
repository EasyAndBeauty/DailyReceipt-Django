import logging
import firebase_admin
from firebase_admin import auth
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class FirebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # /api/로 시작하는 경로에만 인증 체크
        if request.path.startswith('/api/'):
            authorization = request.headers.get('Authorization')
            if not authorization:
                logger.warning("No Authorization header found")
                return JsonResponse({'error': 'No Authorization header'}, status=401)

            if not authorization.startswith('Bearer '):
                return JsonResponse({'error': 'Invalid Authorization header format'}, status=401)

            token = authorization.split('Bearer ')[1]
            try:
                # Firebase 토큰 검증
                decoded_token = auth.verify_id_token(token)
                firebase_uid = decoded_token['uid']
                
                user, created = User.objects.get_or_create(
                    firebase_uid=firebase_uid,
                    defaults={
                        'email': decoded_token.get('email', ''),
                        'display_name': decoded_token.get('name', '')
                    }
                )
                request.user = user
            except Exception as e:
                logger.error(f"Authentication error: {str(e)}")
                return JsonResponse({'error': str(e)}, status=401)

        return self.get_response(request)