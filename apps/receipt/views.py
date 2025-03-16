# views.py

import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Receipt


@swagger_auto_schema(
    method="post",
    operation_description="영수증을 생성합니다.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["contents", "famous_saying", "receipt_name"],
        properties={
            "contents": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "task": openapi.Schema(type=openapi.TYPE_STRING),
                        "duration": openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                    required=["task", "duration"],
                ),
            ),
            "famous_saying": openapi.Schema(type=openapi.TYPE_STRING),
            "receipt_name": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={
        201: openapi.Response(
            "생성된 영수증",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "contents": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "task": openapi.Schema(type=openapi.TYPE_STRING),
                                "duration": openapi.Schema(type=openapi.TYPE_INTEGER),
                            },
                        ),
                    ),
                    "pinned": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "famous_saying": openapi.Schema(type=openapi.TYPE_STRING),
                    "receipt_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "created_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format="date-time"
                    ),
                    "updated_at": openapi.Schema(
                        type=openapi.TYPE_STRING, format="date-time"
                    ),
                },
            ),
        ),
        400: openapi.Response("잘못된 요청 데이터"),
    },
    tags=["Receipt"],
)
@api_view(["POST"])
@csrf_exempt
def receipt_create(request):
    """영수증 생성"""
    try:
        data = request.data
        receipt = Receipt.objects.create(
            contents=data["contents"],
            famous_saying=data["famous_saying"],
            receipt_name=data["receipt_name"],
        )
        return Response(
            {
                "id": receipt.id,
                "contents": receipt.contents,
                "pinned": receipt.pinned,
                "famous_saying": receipt.famous_saying,
                "receipt_name": receipt.receipt_name,
                "created_at": receipt.created_at,
                "updated_at": receipt.updated_at,
            },
            status=201,
        )
    except KeyError:
        return Response({"error": "필수 필드가 누락되었습니다"}, status=400)
    except (ValidationError, json.JSONDecodeError) as e:
        return Response({"error": "잘못된 데이터", "detail": str(e)}, status=400)


def pinned_receipt_list(request):
    """핀된 영수증 목록 조회"""
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
