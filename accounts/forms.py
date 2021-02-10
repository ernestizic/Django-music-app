from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            'placeholder': 'Username'
        }))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ''
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ''
    }))

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('password Mismatch')
        return confirm_password
