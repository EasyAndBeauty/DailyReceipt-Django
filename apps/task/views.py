"""views.py"""

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


@swagger_auto_schema(
    method="get",
    operation_description="모든 태스크 목록을 조회합니다",
    security=[{"Bearer": []}],
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
    security=[{"Bearer": []}],
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
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=201)
        return Response(serializer.errors, status=400)


@swagger_auto_schema(
    method="get",
    operation_description="특정 태스크의 상세 정보를 조회합니다",
    manual_parameters=[
        openapi.Parameter(
            "pk", openapi.IN_PATH, description="태스크 ID", type=openapi.TYPE_INTEGER
        )
    ],
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
@swagger_auto_schema(
    method="delete",
    operation_description="태스크를 삭제합니다",
    manual_parameters=[
        openapi.Parameter(
            "pk", openapi.IN_PATH, description="태스크 ID", type=openapi.TYPE_INTEGER
        )
    ],
    responses={
        204: openapi.Response("태스크가 성공적으로 삭제됨"),
        404: openapi.Response("태스크를 찾을 수 없음"),
    },
    tags=["Task"],
)
@api_view(["GET", "PUT", "DELETE"])
@csrf_exempt
def task_detail(request, pk):
    """상세 조회, 수정, 삭제"""

    try:
        task = Task.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({"error": "찾을 수 없음"}, status=404)

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        task.delete()
        return Response(status=204)
