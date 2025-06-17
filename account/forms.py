from django import forms

class LoginForm(forms.Form):
    """
    Форма для авторизации пользователей.
    """
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    