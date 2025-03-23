"""urls.py"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.receipt_create, name="receipt_create"),
    path("list/", views.pinned_receipt_list, name="pinned_receipt_list"),
]
