from django.shortcuts import redirect
from django.contrib import messages
def verified_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect ("login")
        if not request.user.profile.email_verified:
            messages.warning(request, "Подтвердите email, чтобы продолжить")
            return redirect("verify_email")
        return func(request, *args, **kwargs)
    return wrapper
