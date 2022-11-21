from django.apps import AppConfig
from django.contrib.admin import apps


class MyblogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myblog'


class BlogAdminConf(apps.AdminConfig):
    default_site= 'myblog.admin.BlogAdmin'