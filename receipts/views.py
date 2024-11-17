# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Receipt


@csrf_exempt
def pinned_receipt_list(request):
    """핀된 영수증 목록 조회 및 생성"""
    if request.method == "GET":
        # pinned=True인 영수증만 조회
        receipts = Receipt.objects.filter(pinned=True)
        data = list(receipts.values())
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            receipt = Receipt.objects.create(
                todos=data["todos"],
                pinned=data.get("pinned", True),
                famous_saying=data["famous_saying"],
                receipt_name=data["receipt_name"],
            )

            return JsonResponse({"id": receipt.id}, status=201)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def pinned_receipt_detail(request, receipt_id):
    """특정 영수증 수정"""
    try:
        receipt = Receipt.objects.get(id=receipt_id)
    except Receipt.DoesNotExist:
        return JsonResponse({"error": "영수증을 찾을 수 없습니다"}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)

            if "pinned" in data:
                receipt.pinned = data["pinned"]
            if "famous_saying" in data:
                receipt.famous_saying = data["famous_saying"]
            if "receipt_name" in data:
                receipt.receipt_name = data["receipt_name"]

            receipt.save()

            return JsonResponse(
                {
                    "id": receipt.id,
                    "todos": receipt.todos,
                    "pinned": receipt.pinned,
                    "famous_saying": receipt.famous_saying,
                    "receipt_name": receipt.receipt_name,
                    "created_at": str(receipt.created_at),
                    "updated_at": str(receipt.updated_at),
                }
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 데이터 형식입니다"}, status=400)
