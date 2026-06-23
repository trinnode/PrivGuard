from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect


class SessionTimeoutMiddleware:
    """Logs out inactive users after 15 minutes of inactivity."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get("last_activity")
            now = timezone.now().timestamp()
            if last_activity and (now - last_activity) > 900:
                logout(request)
                return redirect("accounts:login")
            request.session["last_activity"] = now
        return self.get_response(request)
