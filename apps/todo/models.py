from django.db import models


class Todo(models.Model):
    task = models.CharField(max_length=200, help_text="유저가 입력한 Todo 내용")
    timer = models.IntegerField(
        default=0, help_text="유저가 해당 항목에서 타이머를 재생시킨 시간(초)"
    )
    assigned_date = models.DateField(help_text="유저가 할당한 날짜 (YYYY-MM-DD)")
    is_done = models.BooleanField(
        default=False, help_text="유저의 해당 항목에 대한 완료 상태"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="todo 항목이 만들어진 실제 시간"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="todo 항목이 최근에 수정된 시간"
    )

    class Meta:
        ordering = ["-created_at"]  # 최신 항목이 먼저 오도록 정렬
        verbose_name = "Todo"
        verbose_name_plural = "Todos"

    def __str__(self):
        return f"{self.task} ({self.assigned_date})"
