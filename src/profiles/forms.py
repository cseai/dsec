from django import forms

from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        if commit:
            profile.save()
        return profile
