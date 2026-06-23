from django import forms
from incidents.models import Incident, Harm
from incidents.taxonomy import HARM_CATEGORIES


class IncidentForm(forms.ModelForm):
    """Main incident reporting form with guided taxonomy selection."""

    class Meta:
        model = Incident
        fields = [
            "platform_category",
            "platform_name",
            "date_of_occurrence",
            "incident_classification",
            "narrative",
            "actor_involvement",
            "actor_description",
            "severity_rating",
            "evidence_file",
            "is_anonymous",
        ]
        widgets = {
            "date_of_occurrence": forms.DateInput(
                attrs={"type": "date", "max": "", "placeholder": "Select date"}
            ),
            "narrative": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Describe what happened in your own words..."}
            ),
            "platform_name": forms.TextInput(
                attrs={"placeholder": "e.g. Instagram, Telegram"}
            ),
            "actor_description": forms.TextInput(
                attrs={"placeholder": "Optional details about the person involved"}
            ),
        }
        help_texts = {
            "narrative": "",
            "evidence_file": "Screenshot or document. Max 5MB. PNG, JPEG, or PDF only.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["platform_name"].required = False
        self.fields["actor_description"].required = False
        self.fields["evidence_file"].required = False
        self.fields["platform_category"].empty_label = "Select a platform..."
        self.fields["incident_classification"].empty_label = "Select the type of violation..."
        self.fields["actor_involvement"].empty_label = "Select who was involved..."
        self.fields["severity_rating"].empty_label = "Select severity level..."

    def clean_evidence_file(self, *args, **kwargs):
        file = self.cleaned_data.get("evidence_file")
        if file:
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be 5MB or less.")
            if file.content_type not in ["image/png", "image/jpeg", "application/pdf"]:
                raise forms.ValidationError("Only PNG, JPEG, and PDF files are allowed.")
        return file


class HarmForm(forms.ModelForm):
    """Form for classifying harms associated with an incident."""

    class Meta:
        model = Harm
        fields = ["harm_category", "severity_score", "duration", "elaboration"]
        widgets = {
            "elaboration": forms.Textarea(attrs={"rows": 3, "placeholder": "Tell us more about how this harm affected you..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["harm_category"].empty_label = "Select a harm category..."
        self.fields["severity_score"].empty_label = "Select severity..."
        self.fields["duration"].empty_label = "Select duration..."
        self.fields["elaboration"].required = False


class HarmFormSetHelper:
    """Manages multiple harm forms for a single incident."""
    @staticmethod
    def initial_harm_count():
        return 1

    @staticmethod
    def max_harm_forms():
        return len(HARM_CATEGORIES)
