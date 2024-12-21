from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('test-token/', views.test_token, name='test-token'),
    path('validate-token/', views.validate_token, name='validate-token'),
]