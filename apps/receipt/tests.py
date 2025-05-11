"""receipt 앱의 API 테스트"""

from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.receipt.models import Receipt


@pytest.fixture
def api_client():
    """API 클라이언트 픽스처"""
    return APIClient()


@pytest.fixture
def test_user():
    """테스트용 사용자 픽스처"""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(username="test_user_123", email="test@example.com")


@pytest.fixture
def authenticated_client(api_client, test_user):
    """인증된 API 클라이언트 픽스처"""
    with patch("firebase_admin.auth.verify_id_token") as mock_verify_token:
        mock_verify_token.return_value = {
            "uid": test_user.username,
            "email": test_user.email,
        }
        api_client.force_authenticate(user=test_user)
        api_client.credentials(HTTP_AUTHORIZATION="Bearer test_token")
        return api_client


@pytest.fixture
def sample_receipt_data():
    return {
        "contents": [
            {"task": "테스트 작업 1", "duration": 30},
            {"task": "테스트 작업 2", "duration": 45},
        ],
        "famous_saying": "테스트 명언",
        "receipt_name": "테스트 영수증",
    }


@pytest.mark.django_db
def test_receipt_create_success(authenticated_client, sample_receipt_data):
    """영수증 생성 API 테스트 - 성공 케이스"""
    url = reverse("receipt-create")
    response = authenticated_client.post(url, sample_receipt_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["contents"] == sample_receipt_data["contents"]
    assert response.data["famous_saying"] == sample_receipt_data["famous_saying"]
    assert response.data["receipt_name"] == sample_receipt_data["receipt_name"]
    assert response.data["pinned"] is False
    assert Receipt.objects.count() == 1


@pytest.mark.django_db
def test_receipt_create_missing_fields(authenticated_client):
    """영수증 생성 API 테스트 - 필수 필드 누락 케이스"""
    url = reverse("receipt-create")
    invalid_data = {
        "contents": [{"task": "테스트 작업", "duration": 30}],
        # famous_saying과 receipt_name 필드 누락
    }
    response = authenticated_client.post(url, invalid_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_pinned_receipt_list(authenticated_client):
    """핀된 영수증 목록 조회 API 테스트"""
    url = reverse("pinned-receipt-list")
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
