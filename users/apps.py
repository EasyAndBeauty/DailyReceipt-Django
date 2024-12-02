from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials
import os

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH'))
                firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase initialization error: {str(e)}")