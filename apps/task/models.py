"""task 앱의 모델을 정의하는 파일입니다."""

from django.db import models


class Task(models.Model):
    """Task 모델 클래스"""

    objects = models.Manager()
    description = models.CharField(
        max_length=200, help_text="유저가 입력한 Task의의 내용"
    )
    duration = models.IntegerField(
        default=0, help_text="유저가 해당 항목에서 타이머를 재생시킨 시간(초)"
    )
    assigned_date = models.DateField(help_text="유저가 할당한 날짜 (YYYY-MM-DD)")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Task 항목이 만들어진 실제 시간"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Task 항목이 최근에 수정된 시간"
    )

    def __str__(self):
        return f"{self.description} ({self.assigned_date})"

    class Meta:
        """Task 모델 메타 클래스"""

        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
