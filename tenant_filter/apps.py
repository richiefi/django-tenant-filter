from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .models import mk_permissions

class TenantFilterConfig(AppConfig):
    name = 'tenant_filter'

    def ready(self):
        post_migrate.connect(mk_permissions)
