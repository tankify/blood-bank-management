from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BloodRequest, Donor

class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

class DonorForm(StyledModelForm):
    class Meta:
        model = Donor
        fields = ["name", "blood_group", "city", "contact"]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Your name"}),
                   "contact": forms.TextInput(attrs={"placeholder": "00000 00000"})}

class BloodRequestForm(StyledModelForm):
    class Meta:
        model = BloodRequest
        fields = ["requester_name", "blood_group", "city", "contact", "units_needed"]
        widgets = {"requester_name": forms.TextInput(attrs={"placeholder": "Your name"}),
                   "contact": forms.TextInput(attrs={"placeholder": "00000 00000"}),
                   "units_needed": forms.NumberInput(attrs={"min": 1, "max": 10})}

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
