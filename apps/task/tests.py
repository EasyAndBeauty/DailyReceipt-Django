import datetime
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.task.models import Task

"""task 앱의 API 테스트"""


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
def sample_task_data():
    return {
        "description": "테스트 태스크",
        "assigned_date": "2024-03-23",
        "duration": 60,
    }


@pytest.mark.django_db
def test_task_list_get(authenticated_client):
    """할 일 목록 조회 테스트"""
    url = reverse("task-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_task_create_success(authenticated_client):
    """할 일 생성 성공 테스트"""
    url = reverse("task-list")
    data = {
        "description": "테스트 할 일",
        "assigned_date": "2024-03-20",
        "duration": 60,
    }
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    assert Task.objects.get().description == "테스트 할 일"


@pytest.mark.django_db
def test_task_create_missing_fields(authenticated_client):
    """필수 필드 누락 테스트"""
    url = reverse("task-list")
    data = {"description": "테스트 할 일"}
    response = authenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_task_detail_get(authenticated_client):
    """할 일 상세 조회 테스트"""
    task = Task.objects.create(
        description="테스트 할 일", assigned_date="2024-03-20", duration=60
    )
    url = reverse("task-detail", kwargs={"pk": task.pk})
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_task_detail_not_found(authenticated_client):
    """존재하지 않는 할 일 조회 테스트"""
    url = reverse("task-detail", kwargs={"pk": 999})
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_task_update(authenticated_client):
    """할 일 수정 테스트"""
    task = Task.objects.create(
        description="테스트 할 일", assigned_date="2024-03-20", duration=60
    )
    url = reverse("task-detail", kwargs={"pk": task.pk})
    data = {
        "description": "수정된 할 일",
        "assigned_date": "2024-03-21",
        "duration": 90,
    }
    assigned_date = data.get("assigned_date", task.assigned_date)
    if isinstance(assigned_date, str):
        assigned_date = datetime.datetime.strptime(assigned_date, "%Y-%m-%d").date()
    task.assigned_date = assigned_date
    task.save()
    response = authenticated_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Task.objects.get(pk=task.pk).description == "수정된 할 일"


@pytest.mark.django_db
def test_task_delete(authenticated_client):
    """할 일 삭제 테스트"""
    task = Task.objects.create(
        description="삭제할 할 일", assigned_date="2024-03-20", duration=60
    )
    url = reverse("task-detail", kwargs={"pk": task.pk})
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(pk=task.pk).exists()


@pytest.mark.django_db
def test_task_delete_not_found(authenticated_client):
    """존재하지 않는 할 일 삭제 테스트"""
    url = reverse("task-detail", kwargs={"pk": 999})
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
