# coding: utf-8
from django.db import models
from .middleware import get_current_user
from django.conf import settings

TENANT_FILTER = getattr(settings, 'TENANT_FILTER')
TENANT_USER_OBJ_NAME = TENANT_FILTER['TENANT_USER_MODEL'].split('.')[-1].lower()
TENANT_OBJ_NAME = TENANT_FILTER['TENANT_MODEL'].split('.')[-1].lower()

def mk_permissions(**kwargs):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission

    ct = ContentType.objects.get_or_create(
        app_label='tenant_filter',
        model='TenantPermissions')[0]
    no_tenant_required = Permission.objects.get_or_create(
        name='no tenant required',
        content_type=ct,
        codename='no_tenant_required')

class TenantFilterManager(models.Manager):
    def get_queryset(self):
        """
        Filter the default queryset by the tenant ID found in the local thread. It requires
        'middleware.GlobalRequestMiddleware' to be activated in settings.py
        """
        qs = super(TenantFilterManager, self).get_queryset()
        user = get_current_user()
        if user and user.is_authenticated and not user.has_perm('tenant_filter.no_tenant_required'):
            tenant_user_obj = getattr(user, TENANT_USER_OBJ_NAME, None)
            if tenant_user_obj is None:
                raise ValueError("No tenant defined for user")
            tenant_obj = getattr(tenant_user_obj, TENANT_OBJ_NAME)
            filter_dict = {TENANT_FILTER['TENANT_FK_NAME']: tenant_obj.pk}
            qs = qs.filter(**filter_dict)
        return qs
