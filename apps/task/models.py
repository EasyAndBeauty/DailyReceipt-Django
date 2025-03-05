"""task 앱의 모델을 정의하는 파일입니다."""

from django.db import models


class Task(models.Model):
    """Task 모델 클래스"""

    description = models.CharField(
        max_length=255, verbose_name="작업 설명", help_text="수행할 작업에 대한 설명"
    )
    assigned_date = models.DateField(
        verbose_name="할당된 날짜",
        help_text="작업이 할당된 날짜",
        null=True,
        blank=True,
    )
    duration = models.PositiveIntegerField(
        default=0,
        verbose_name="소요 시간(분)",
        help_text="작업 완료에 소요된 시간(분 단위)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="생성 시간", help_text="작업이 생성된 시간"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정 시간",
        help_text="작업이 마지막으로 수정된 시간",
    )

    def __str__(self):
        return f"{self.description} ({self.assigned_date})"

    class Meta:
        """Task 모델 메타 클래스"""

        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
