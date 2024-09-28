from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def get_all_permissions(user):
    user_permissions = set()
    for group in user.groups.all():
        for permission in group.permissions.all():
            user_permissions.add(permission)
    for permission in user.user_permissions.all():
        user_permissions.add(permission)
    objects = []
    for permission in user_permissions:
        objects.append(permission.content_type.app_label + '.' + permission.codename)
    return objects


class PermissionMixin(object):
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(PermissionMixin, self).dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        else:
            for permission in get_all_permissions(request.user):
                if permission in self.permission_required:
                    return super(PermissionMixin, self).dispatch(request, *args, **kwargs)
            raise PermissionDenied
