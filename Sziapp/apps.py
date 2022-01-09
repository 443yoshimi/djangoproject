from django.apps import AppConfig


class TestAppConfig(AppConfig):
    name = 'app'
    
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Sziapp'
