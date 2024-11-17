# models.py
from django.db import models


class Receipt(models.Model):
    # JSONField를 사용하여 Todo 목록을 저장 (PostgreSQL 사용 시)
    todos = models.JSONField(help_text="영수증을 핀했을 때의 todo 목록")
    pinned = models.BooleanField(default=True, help_text="현재 핀의 상태")
    famous_saying = models.CharField(
        max_length=500, help_text="영수증과 함께 만들어진 명언"
    )
    receipt_name = models.CharField(
        max_length=100, help_text="영수증을 핀했을 당시의 유저 닉네임"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="영수증 항목이 만들어진 실제 시간"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="영수증 항목이 최근에 수정된 시간"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"

    def __str__(self):
        return f"Receipt by {self.receipt_name} ({self.created_at})"
