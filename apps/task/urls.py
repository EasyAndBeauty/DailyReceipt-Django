"""urls.py"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("<int:pk>/", views.task_detail, name="task_detail"),
    path("count/", views.task_count, name="task_count"),
]
