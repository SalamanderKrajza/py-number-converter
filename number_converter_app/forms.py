from django import forms

class ConverterForm(forms.Form):
    given_number = forms.IntegerField(label='Your number')
    given_number.widget.attrs['placeholder'] = 'Give the number to convert'
    given_number.widget.attrs['name'] = 'given_number'