from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def allowed_users(allowed_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            is_allowed = False
            if request.user.groups.exists():
                for group in request.user.groups.all():
                    if group.name in allowed_groups:
                        is_allowed = True
                        break
            if is_allowed:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('public_pages:index'))
        return wrapper_func
    return decorator