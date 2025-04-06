"""receipt 앱의 API 테스트"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Receipt


@pytest.fixture
def api_client():
    return APIClient()


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
def test_receipt_create_success(api_client, sample_receipt_data):
    """영수증 생성 API 테스트 - 성공 케이스"""
    url = reverse("receipt-create")
    response = api_client.post(url, sample_receipt_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["contents"] == sample_receipt_data["contents"]
    assert response.data["famous_saying"] == sample_receipt_data["famous_saying"]
    assert response.data["receipt_name"] == sample_receipt_data["receipt_name"]
    assert response.data["pinned"] is False


@pytest.mark.django_db
def test_receipt_create_missing_fields(api_client):
    """영수증 생성 API 테스트 - 필수 필드 누락 케이스"""
    url = reverse("receipt-create")
    invalid_data = {
        "contents": [{"task": "테스트 작업", "duration": 30}],
        # famous_saying과 receipt_name 필드 누락
    }
    response = api_client.post(url, invalid_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_pinned_receipt_list(api_client, sample_receipt_data):
    """핀된 영수증 목록 조회 API 테스트"""
    # 핀된 영수증 생성
    Receipt.objects.create(
        contents=sample_receipt_data["contents"],
        famous_saying=sample_receipt_data["famous_saying"],
        receipt_name=sample_receipt_data["receipt_name"],
        pinned=True,
    )

    url = reverse("pinned-receipt-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["pinned"] is True
