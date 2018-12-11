from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator


class StaffPermissionMixin(View):
    """
    Permission mixin for vendor user (also allows staff)
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().dispatch(*args, **kwargs)
        else:
            raise PermissionDenied