# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Todo


# 목록 조회
@csrf_exempt  # POST 요청을 받기 위해 필요
def todo_list():
    todos = Todo.objects.all()
    data = list(todos.values())  # QuerySet을 list로 변환
    return JsonResponse(data, safe=False)


# 상세 조회, 수정, 삭제
@csrf_exempt
def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return JsonResponse({"error": "찾을 수 없음"}, status=404)

    if request.method == "GET":
        data = {
            "id": todo.id,
            "task": todo.task,
            "assigned_date": str(todo.assigned_date),
            "timer": todo.timer,
            "is_done": todo.is_done,
            "created_at": str(todo.created_at),
            "updated_at": str(todo.updated_at),
        }
        return JsonResponse(data)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            todo.task = data.get("task", todo.task)
            todo.assigned_date = data.get("assigned_date", todo.assigned_date)
            todo.timer = data.get("timer", todo.timer)
            todo.is_done = data.get("is_done", todo.is_done)
            todo.save()
            return JsonResponse(
                {
                    "id": todo.id,
                    "task": todo.task,
                    "assigned_date": str(todo.assigned_date),
                    "timer": todo.timer,
                    "is_done": todo.is_done,
                    "created_at": str(todo.created_at),
                    "updated_at": str(todo.updated_at),
                }
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 데이터"}, status=400)

    elif request.method == "DELETE":
        todo.delete()
        return JsonResponse({}, status=204)


# HTTP 메소드 제한하기
@require_http_methods(["GET"])
def todo_count(request):
    count = Todo.objects.count()
    return JsonResponse({"total": count})
