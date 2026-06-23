from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from accounts.views import (
    register,
    CustomLoginView,
    custom_logout,
    profile,
    toggle_consent,
    toggle_anonymize,
    delete_account,
)
from accounts.forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", custom_logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("consent/toggle/", toggle_consent, name="toggle_consent"),
    path("anonymize/toggle/", toggle_anonymize, name="toggle_anonymize"),
    path("delete/", delete_account, name="delete_account"),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            form_class=CustomPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            form_class=CustomSetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
