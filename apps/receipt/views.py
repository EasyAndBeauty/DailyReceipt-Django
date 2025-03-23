"""views.py"""

import json

from django.core.exceptions import ValidationError
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
            },
            status=201,
        )
    except KeyError:
        return Response({"error": "필수 필드가 누락되었습니다"}, status=400)
    except (ValidationError, json.JSONDecodeError) as e:
        return Response({"error": "잘못된 데이터", "detail": str(e)}, status=400)


@swagger_auto_schema(
    method="get",
    operation_description="핀된 영수증 목록을 조회합니다",
    responses={
        200: openapi.Response(
            "핀된 영수증 목록",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "contents": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "task": openapi.Schema(type=openapi.TYPE_STRING),
                                    "duration": openapi.Schema(
                                        type=openapi.TYPE_INTEGER
                                    ),
                                },
                            ),
                        ),
                        "pinned": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "famous_saying": openapi.Schema(type=openapi.TYPE_STRING),
                        "receipt_name": openapi.Schema(type=openapi.TYPE_STRING),
                        "created_at": openapi.Schema(
                            type=openapi.TYPE_STRING, format="date-time"
                        ),
                    },
                ),
            ),
        )
    },
)
def pinned_receipt_list(request):
    """핀된 영수증 목록 조회"""
    if request.method == "GET":
        # pinned=True인 영수증만 조회
        receipts = Receipt.objects.filter(pinned=True)
        data = list(receipts.values())
        return Response(data)
