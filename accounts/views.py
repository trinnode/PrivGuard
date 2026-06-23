from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from accounts.forms import (
    RegistrationForm,
    LoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    ProfileForm,
    ConsentForm,
)
from accounts.models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect("dashboard:home")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password. Please try again.")
        return super().form_invalid(form)


def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


@login_required
@require_POST
def toggle_anonymize(request):
    user = request.user
    user.anonymize_requested = not user.anonymize_requested
    user.save(update_fields=["anonymize_requested"])
    if user.anonymize_requested:
        messages.success(request, "Identity concealment has been enabled for future exports.")
    else:
        messages.info(request, "Identity concealment has been disabled.")
    return redirect("accounts:profile")


@login_required
@require_POST
def toggle_consent(request):
    if request.user.consent_granted:
        request.user.revoke_consent()
        messages.info(request, "Research consent has been revoked.")
    else:
        request.user.record_consent()
        messages.success(request, "Research consent has been granted.")
    return redirect("accounts:profile")


@login_required
@require_POST
def delete_account(request):
    """Permanently deletes the user account and all related data."""
    password = request.POST.get("password", "")
    if not request.user.check_password(password):
        messages.error(request, "Incorrect password. Account not deleted.")
        return redirect("accounts:profile")
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Your account and all associated data have been permanently deleted.")
    return redirect("landing")


def csrf_failure(request, reason=""):
    return render(request, "accounts/csrf_failure.html", {"reason": reason})
