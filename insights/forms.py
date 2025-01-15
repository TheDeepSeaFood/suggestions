from django import forms
from insights.models import Insight


class InsightForm(forms.ModelForm):
    class Meta:
        model = Insight
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        if "feedback_or_suggestion" in self.fields:
            self.fields["feedback_or_suggestion"].widget.attrs.update({"rows": 4})
