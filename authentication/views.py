from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests

@swagger_auto_schema(
    method='get',
    operation_description="""
    Generate a test Firebase token for development purposes.

    This API is for testing the token issuance process in the flutter client.
    
    This endpoint is only available in DEBUG mode and provides:
    - A Firebase custom token
    - An ID token exchanged from the custom token
    - Test user information
    
    Use the returned id_token for testing other authenticated endpoints.
    """,
    responses={
        200: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Success message",
                        example="Test tokens generated successfully"
                    ),
                    'id_token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Firebase ID token to use for authentication",
                        example="eyJhbGciOiJSUzI1NiIs..."
                    ),
                    'custom_token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Firebase custom token (for reference only)",
                        example="eyJhbGciOiJSUzI1NiIs..."
                    ),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'uid': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Test user ID",
                                example="test_user_123"
                            )
                        }
                    )
                }
            )
        ),
        403: openapi.Response(
            description="Not available in production mode",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Only available in debug mode"
                    )
                }
            )
        ),
        500: "Internal server error"
    },
    tags=['Authentication']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def test_token(request):
    """
    Generate a test Firebase token for development purposes.
    This endpoint is only available in DEBUG mode and provides:
    - A Firebase custom token
    - An ID token exchanged from the custom token
    - Test user information
    """

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
    
@swagger_auto_schema(
    method='post',
    operation_description="""
    Validate a Firebase ID token and return decoded information.
    
    Steps to test:
    1. First call /api/auth/test-token/ to get an ID token
    2. Use that ID token in this endpoint's request body
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id_token'],
        properties={
            'id_token': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Firebase ID token to validate",
                example="eyJhbGciOiJSUzI1NiIs..."
            )
        }
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Success message",
                    example="Token is valid"
                ),
                'uid': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Firebase user ID",
                    example="test_user_123"
                ),
                'decoded_token': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Full decoded token information",
                    example={
                        "iss": "https://securetoken.google.com/project-id",
                        "aud": "project-id",
                        "auth_time": 1621459200,
                        "user_id": "test_user_123",
                        "sub": "test_user_123",
                        "iat": 1621459200,
                        "exp": 1621462800,
                        "email": "test@example.com"
                    }
                )
            }
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'error': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Invalid token provided"
                )
            }
        )
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def validate_token(request):
    """
    Validate a Firebase ID token and return the decoded information.
    
    Requires:
    - id_token: The Firebase ID token to validate
    
    Returns:
    - Decoded token information if valid
    - Error message if invalid
    """
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

@swagger_auto_schema(
    method='post',
    operation_description="""
    Verify Firebase ID token from social login and return user info.
    
    This endpoint should be called after successful social login (Google/Apple) from the client.
    The client should send the Firebase ID token received after social authentication.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id_token'],
        properties={
            'id_token': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Firebase ID token from social login",
                example="eyJhbGciOiJSUzI1NiIs..."
            )
        }
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'picture': openapi.Schema(type=openapi.TYPE_STRING),
                'provider': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        400: "Invalid token",
        401: "Unauthorized"
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def social_auth(request):
    """Handle social authentication verification"""
    try:
        id_token = request.data.get('id_token')
        if not id_token:
            return Response(
                {"error": "No token provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        
        # Extract user info from token
        user_info = {
            'uid': decoded_token.get('uid'),
            'email': decoded_token.get('email', ''),
            'name': decoded_token.get('name', ''),
            'picture': decoded_token.get('picture', ''),
            'provider': decoded_token.get('firebase', {}).get('sign_in_provider', '')
        }
        
        return Response(user_info)
        
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_401_UNAUTHORIZED
        )