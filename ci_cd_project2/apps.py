from django.apps import AppConfig


class CiCdProject2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ci_cd_project2'

    def ready(self):
        import ci_cd_project2.signals
