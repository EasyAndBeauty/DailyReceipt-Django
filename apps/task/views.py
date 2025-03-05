# views.py
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task


@swagger_auto_schema(
    method="get",
    operation_description="모든 태스크 목록을 조회합니다",
    responses={
        200: openapi.Response(
            "태스크 목록",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "description": openapi.Schema(type=openapi.TYPE_STRING),
                        "assigned_date": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date"
                        ),
                        "duration": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "created_at": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date-time"
                        ),
                        "updated_at": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date-time"
                        ),
                    },
                ),
            ),
        )
    },
    tags=["Task"],
)
@swagger_auto_schema(
    method="post",
    operation_description="새로운 태스크를 생성합니다",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["description"],
        properties={
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "assigned_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
            "duration": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
    responses={
        201: openapi.Response("생성된 태스크 정보"),
        400: openapi.Response("잘못된 요청 데이터"),
    },
    tags=["Task"],
)
@api_view(["GET", "POST"])
@csrf_exempt
def task_list(request):
    """모든 태스크 목록을 조회하거나 새 태스크를 생성합니다."""
    if request.method == "GET":
        tasks = Task.objects.all()
        data = list(tasks.values())
        return Response(data)

    elif request.method == "POST":
        try:
            data = request.data
            task = Task.objects.create(
                description=data["description"],
                assigned_date=data.get("assigned_date"),
                duration=data.get("duration", 0),
            )
            return Response(
                {
                    "id": task.id,
                    "description": task.description,
                    "assigned_date": str(task.assigned_date),
                    "duration": task.duration,
                    "created_at": str(task.created_at),
                    "updated_at": str(task.updated_at),
                },
                status=201,
            )
        except KeyError:
            return Response({"error": "필수 필드가 누락되었습니다"}, status=400)
        except Exception as e:
            return Response({"error": "잘못된 데이터", "detail": str(e)}, status=400)


@swagger_auto_schema(
    method="get",
    operation_description="특정 태스크의 상세 정보를 조회합니다",
    responses={
        200: openapi.Response(
            "태스크 상세 정보",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "assigned_date": openapi.Schema(
                        type=openapi.TYPE_STRING, format="date"
                    ),
                    "duration": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "created_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format="date-time"
                    ),
                    "updated_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format="date-time"
                    ),
                },
            ),
        ),
        404: openapi.Response("태스크를 찾을 수 없음"),
    },
    tags=["Task"],
)
@swagger_auto_schema(
    method="put",
    operation_description="태스크 정보를 수정합니다",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "assigned_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
            "duration": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
    responses={
        200: openapi.Response("수정된 태스크 정보"),
        400: openapi.Response("잘못된 요청 데이터"),
        404: openapi.Response("태스크를 찾을 수 없음"),
    },
    tags=["Task"],
)
@api_view(
    [
        "GET",
        "PUT",
    ]
)
@csrf_exempt
def task_detail(request, pk):
    """상세 조회, 수정, 삭제"""

    try:
        task = Task.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "찾을 수 없음"}, status=404)

    if request.method == "GET":
        data = {
            "id": task.id,
            "description": task.description,
            "assigned_date": task.assigned_date.strftime("%Y-%m-%d"),
            "duration": task.duration,
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JsonResponse(data)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            task.description = data.get("description", task.description)
            task.assigned_date = data.get("assigned_date", task.assigned_date)
            task.duration = data.get("duration", task.duration)
            task.save()
            return JsonResponse(
                {
                    "id": task.id,
                    "description": task.description,
                    "assigned_date": task.assigned_date.strftime("%Y-%m-%d"),
                    "duration": task.duration,
                    "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 데이터"}, status=400)

    elif request.method == "DELETE":
        task.delete()
        return JsonResponse({}, status=204)
