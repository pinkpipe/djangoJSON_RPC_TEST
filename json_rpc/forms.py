from django import forms

class RPCForm(forms.Form):
    method = forms.CharField(label='Метод', initial='auth.check')
    params = forms.CharField(label='Параметры (через запятую)', required=False)