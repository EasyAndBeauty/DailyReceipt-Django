import pytest

"""task 앱의 API 테스트"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_task_data():
    return {
        "description": "테스트 태스크",
        "assigned_date": "2024-03-23",
        "duration": 60,
    }


@pytest.mark.django_db
def test_task_list_get(api_client, sample_task_data):
    """태스크 목록 조회 API 테스트"""
    # 테스트 데이터 생성
    Task.objects.create(**sample_task_data)

    url = reverse("task-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["description"] == sample_task_data["description"]


@pytest.mark.django_db
def test_task_create_success(api_client, sample_task_data):
    """태스크 생성 API 테스트 - 성공 케이스"""
    url = reverse("task-list")
    response = api_client.post(url, sample_task_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["description"] == sample_task_data["description"]
    assert response.data["assigned_date"] == sample_task_data["assigned_date"]
    assert response.data["duration"] == sample_task_data["duration"]


@pytest.mark.django_db
def test_task_create_missing_fields(api_client):
    """태스크 생성 API 테스트 - 필수 필드 누락 케이스"""
    url = reverse("task-list")
    invalid_data = {
        # description 필드 누락
        "assigned_date": "2024-03-23",
        "duration": 60,
    }
    response = api_client.post(url, invalid_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_task_detail_get(api_client, sample_task_data):
    """태스크 상세 조회 API 테스트"""
    task = Task.objects.create(**sample_task_data)
    url = reverse("task-detail", kwargs={"pk": task.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == task.id
    assert response.data["description"] == sample_task_data["description"]


@pytest.mark.django_db
def test_task_detail_not_found(api_client):
    """존재하지 않는 태스크 조회 API 테스트"""
    url = reverse("task-detail", kwargs={"pk": 999})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "error" in response.data


@pytest.mark.django_db
def test_task_update(api_client, sample_task_data):
    """태스크 수정 API 테스트"""
    task = Task.objects.create(**sample_task_data)
    url = reverse("task-detail", kwargs={"pk": task.id})
    update_data = {
        "description": "수정된 태스크",
        "duration": 90,
    }
    response = api_client.put(url, update_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["description"] == update_data["description"]
    assert response.data["duration"] == update_data["duration"]
