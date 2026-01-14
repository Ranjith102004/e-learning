from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def instructor_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('accounts:login')

        if not user.is_instructor:
            return HttpResponseForbidden(
                "You are not allowed to access this page."
            )

        return view_func(request, *args, **kwargs)

    return wrapper
