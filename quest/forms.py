from django import forms

from .models import DailyEntry


class DailyEntryForm(forms.ModelForm):
    class Meta:
        model = DailyEntry
        exclude = ["user", "date"]
        widgets = {
            "notes": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Anything worth remembering about today..."}
            ),
        }
