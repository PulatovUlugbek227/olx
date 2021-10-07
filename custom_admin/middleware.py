from django.shortcuts import reverse
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class RestrictStaffToAdminMiddleware(MiddlewareMixin):
    """
    A middleware that restricts staff members access to administration panels.
    """
    def process_request(self, request):
        if request.path.startswith(reverse('admin')):
            if request.user.is_authenticated:
                if not request.user.is_superuser:
                    raise Http404
            else:
                raise Http404