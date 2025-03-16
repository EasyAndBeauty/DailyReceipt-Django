"""Receipt models.py"""

from django.core.exceptions import ValidationError
from django.db import models


def validate_task_list(value):
    """영수증의 task 목록의 유효성 검사"""
    if not isinstance(value, list):
        raise ValidationError("값은 리스트 형태여야 합니다.")

    for item in value:
        if not isinstance(item, dict):
            raise ValidationError("리스트의 각 항목은 딕셔너리여야 합니다.")

        # 필수 키 확인
        if "task" not in item or "duration" not in item:
            raise ValidationError("각 항목은 'task'와 'duration' 키를 포함해야 합니다.")

        # 타입 확인
        if not isinstance(item["task"], str):
            raise ValidationError("'task' 값은 문자열이어야 합니다.")

        if not isinstance(item["duration"], (int, float)):
            raise ValidationError("'duration' 값은 숫자여야 합니다.")


class Receipt(models.Model):
    """Receipt 모델 클래스"""

    contents = models.JSONField(
        validators=[validate_task_list],
        default=list,
        null=False,
        blank=False,
        help_text="영수증을 핀했을 때의 todo 목록",
    )

    pinned = models.BooleanField(default=False, help_text="현재 핀의 상태")

    famous_saying = models.CharField(
        max_length=500, help_text="영수증과 함께 만들어진 명언"
    )

    # TODO: 필요한지 재검토
    receipt_name = models.CharField(
        max_length=100, help_text="영수증을 핀했을 당시의 유저 닉네임"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="영수증이 만들어진 실제 시간"
    )

    updated_at = models.DateTimeField(
        auto_now=True, help_text="영수증이 최근에 수정된 시간"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"

    def __str__(self):
        return f"Receipt by {self.receipt_name} ({self.created_at})"
