from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Логін', max_length=150)

    def confirm_login_allowed(self, user):
        # Залишити стандартну перевірку Django або додати свою
        if not user.is_active:
            raise forms.ValidationError("Цей обліковий запис деактивовано.", code='inactive')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=13)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'address']
