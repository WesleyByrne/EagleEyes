from django import forms

class MyForm(forms.ModelForm):
    class Meta:
    widgets = {'myDateField': forms.DateInput(attrs={'id': 'datetimepicker12'})}
