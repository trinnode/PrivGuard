from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from accounts.models import User


class RegistrationForm(forms.ModelForm):
    """User registration with progressive disclosure and consent."""
    password1 = forms.CharField(
        label="Create password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    consent = forms.BooleanField(
        label="I consent to my anonymized data being used for privacy research purposes",
        required=False,
    )

    class Meta:
        model = User
        fields = ("email", "full_name", "institution")

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        if p1 and len(p1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if self.cleaned_data.get("consent"):
            from django.utils import timezone
            user.consent_granted = True
            user.consent_date = timezone.now()
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "institution", "anonymize_requested")
        widgets = {
            "anonymize_requested": forms.CheckboxInput(attrs={"class": "form-checkbox-input"}),
        }


class ConsentForm(forms.Form):
    consent = forms.BooleanField(
        label="I consent to my anonymized data being used for privacy research purposes",
        required=False,
    )
