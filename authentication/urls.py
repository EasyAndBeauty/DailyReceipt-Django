from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('test-token/', views.test_token, name='test-token'),
    path('validate-token/', views.validate_token, name='validate-token'),
    path('social-auth/', views.social_auth, name='social-auth'),
]