# views.py
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Task


# 목록 조회
@csrf_exempt
def task_list(request):
    tasks = Task.objects.all()
    data = list(tasks.values())
    return JsonResponse(data, safe=False)


# 상세 조회, 수정, 삭제
@csrf_exempt
def task_detail(request, pk):
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


@require_http_methods(["GET"])
def task_count(request):
    count = Task.objects.count()
    return JsonResponse({"total": count})
