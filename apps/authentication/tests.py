"""authentication 앱의 API 테스트"""

from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """API 클라이언트 픽스처"""
    return APIClient()


@pytest.fixture
def mock_firebase_auth(mocker):
    """Firebase 인증을 모킹하는 fixture"""
    mock_auth = mocker.patch("apps.authentication.views.auth")
    mock_auth.create_custom_token.return_value = b"test_custom_token"
    mock_auth.verify_id_token.return_value = {
        "uid": "test_uid",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "http://example.com/picture.jpg",
        "firebase": {"sign_in_provider": "google.com"},
    }
    return mock_auth


@pytest.fixture
def mock_requests(mocker):
    """HTTP 요청을 모킹하는 fixture"""
    mock_requests = mocker.patch("apps.authentication.views.requests")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"idToken": "test_id_token"}
    mock_requests.post.return_value = mock_response
    return mock_requests


@pytest.fixture
def debug_setting(settings):
    """테스트 중 DEBUG 설정을 True로 변경"""
    settings.DEBUG = True
    settings.FIREBASE_WEB_API_KEY = "test_api_key"
    return settings


@pytest.mark.django_db
def test_test_token_success(
    api_client, mock_firebase_auth, mock_requests, debug_setting
):
    """테스트 토큰 생성 API 테스트 - 성공 케이스"""
    url = reverse("authentication:test-token")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "custom_token" in response.data
    assert "id_token" in response.data
    assert "user" in response.data


@pytest.mark.django_db
def test_validate_token_success(api_client, mock_firebase_auth):
    """토큰 검증 API 테스트 - 성공 케이스"""
    # Firebase 토큰 검증 모의 설정
    mock_decoded_token = {
        "uid": "test_user_123",
        "email": "test@example.com",
        "name": "Test User",
    }
    mock_firebase_auth.verify_id_token.return_value = mock_decoded_token

    url = reverse("authentication:validate-token")
    response = api_client.post(url, {"id_token": "test_token"})
    assert response.status_code == status.HTTP_200_OK
    assert "decoded_token" in response.data


@pytest.mark.django_db
def test_validate_token_missing_token(api_client):
    """토큰 검증 API 테스트 - 토큰 누락 케이스"""
    url = reverse("authentication:validate-token")
    response = api_client.post(url, {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_validate_token_invalid_token(api_client, mock_firebase_auth):
    """토큰 검증 API 테스트 - 잘못된 토큰 케이스"""
    # Firebase 토큰 검증 실패 모의 설정
    mock_firebase_auth.verify_id_token.side_effect = Exception("Invalid token")

    url = reverse("authentication:validate-token")
    response = api_client.post(url, {"id_token": "invalid_token"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_social_auth_success(api_client, mock_firebase_auth):
    """소셜 로그인 API 테스트 - 성공 케이스"""
    # Firebase 토큰 검증 모의 설정
    mock_decoded_token = {
        "uid": "test_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "https://example.com/photo.jpg",
        "provider": "google.com",
    }
    mock_firebase_auth.verify_id_token.return_value = mock_decoded_token

    url = reverse("authentication:social-auth")
    response = api_client.post(url, {"id_token": "mock_token"})
    assert response.status_code == status.HTTP_200_OK
    assert "user" in response.data
