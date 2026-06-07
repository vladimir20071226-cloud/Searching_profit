from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
import logging
from functools import wraps
from django.urls import path
logger=logging.getLogger(__name__)
def verified_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect ("login")
        if not request.user.email_verified:
            messages.warning(request, "Подтвердите email, чтобы продолжить")
            return redirect("verify_email")
        return func(request, *args, **kwargs)
    return wrapper

def log_action(action_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user=request.user if request.user.is_authenticated else "Anonymous"
            url=request.path
            timestamp=timezone.now()
            logger.info(
                f"[{timestamp}] User={user} | Action={action_name} | URL={url}"
            )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator