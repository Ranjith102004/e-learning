from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def instructor_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = getattr(request, 'user', None)

        # Not logged in
        if not user or not user.is_authenticated:
            return redirect('login')

        # Logged in but not instructor
        if not getattr(user, 'is_instructor', False):
            return HttpResponseForbidden(
                "You are not allowed to access this page."
            )

        return view_func(request, *args, **kwargs)

    return wrapper