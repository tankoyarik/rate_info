from django import forms


class AddRateForm(forms.Form):
    base = forms.CharField()
    target = forms.CharField()