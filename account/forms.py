from .models import Profile
from django import forms
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    """
    Форма для авторизации пользователей.
    """
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

class UserRegistrationForm(forms.ModelForm):
    """
    Форма для регистрации пользователей.
    """
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Повтор пароля", widget=forms.PasswordInput
        )

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "email"]
    
    def clean_password2(self):
        """
        Проверка/валидация совпадения паролей.
        """
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd["password2"]
    
class UserEditForm(forms.ModelForm):
    """
    Форма редактирования встроенной модели пользователя. 
    """
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")

class ProfileEditForm(forms.ModelForm):
    """
    Форма редактирования дополнительной информации о пользователе. 
    """
    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")