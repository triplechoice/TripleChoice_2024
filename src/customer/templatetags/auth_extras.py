from django import template
from order.models.order import OrderInfo
from authentication.mixins import get_all_permissions

register = template.Library()


@register.filter(name='has_permission')
def has_permission(user, permission_name):
    if user.is_superuser:
        return True
    permissions = get_all_permissions(user)
    if permission_name in permissions:
        return True


@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='is_ordered')
def is_ordered(user, request_id):
    return OrderInfo.objects.filter(request_id=request_id).exists()
