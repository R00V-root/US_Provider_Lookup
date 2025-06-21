from django import forms

class ProviderSearchForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    npi = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False, max_length=2)
    profession = forms.CharField(required=False, label='Profession/Specialty')
