from django.db import models

class User(models.Model):
    # Firebase 식별자
    firebase_uid = models.CharField(max_length=128, unique=True)
    
    # Firebase에서 가져오는 기본 정보
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=100)
    photo_url = models.URLField(null=True, blank=True)
    
    # 추가 사용자 정보
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    # 메타 데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)

    def __str__(self):
        return self.email