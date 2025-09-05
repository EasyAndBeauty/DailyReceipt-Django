"""apps.py"""

from django.apps import AppConfig


class TaskConfig(AppConfig):
    """Task 앱 설정 클래스"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.task"
