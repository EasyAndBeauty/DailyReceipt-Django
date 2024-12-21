from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from django.conf import settings
import requests

@api_view(['GET'])
@permission_classes([AllowAny])
def test_token(request):
    """테스트용 Firebase 토큰을 생성하는 엔드포인트"""
    if not settings.DEBUG:
        return Response({"error": "Only available in debug mode"}, status=403)
    
    try:
        # 테스트용 토큰 생성
        test_uid = 'test_user_123'
        custom_token = auth.create_custom_token(test_uid).decode('utf-8')
        
        # 커스텀 토큰을 ID 토큰으로 교환
        firebase_api_key = settings.FIREBASE_WEB_API_KEY
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={firebase_api_key}'
        
        response = requests.post(url, json={
            'token': custom_token,
            'returnSecureToken': True
        })
        
        if response.status_code != 200:
            raise Exception("Failed to exchange token")
            
        id_token = response.json()['idToken']
        
        return Response({
            "message": "Test tokens generated successfully",
            "custom_token": custom_token,  # 참고용
            "id_token": id_token,  # 실제 사용할 토큰
            "user": {
                "uid": test_uid
            }
        })
            
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['POST'])
@permission_classes([AllowAny])
def validate_token(request):
    """ID 토큰의 유효성을 검증하는 엔드포인트"""
    try:
        id_token = request.data.get('id_token')
        if not id_token:
            return Response(
                {"error": "No token provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Firebase로 토큰 검증
        decoded_token = auth.verify_id_token(id_token)
        
        return Response({
            "message": "Token is valid",
            "uid": decoded_token['uid'],
            "decoded_token": decoded_token
        })
        
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )