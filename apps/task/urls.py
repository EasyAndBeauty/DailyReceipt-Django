"""urls.py"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task-list"),
    path("<int:pk>/", views.task_detail, name="task-detail"),
]
