from .models import Profile
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    """
    Форма для авторизации пользователей.
    """
    username = forms.CharField(label="Имя пользователя или email")
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
        model = User
        fields = ["username", "first_name", "email"]
    
    def clean_password2(self):
        """
        Проверка/валидация совпадения паролей.
        """
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd["password2"]
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже существует!")
        return email
    
class UserEditForm(forms.ModelForm):
    """
    Форма редактирования встроенной модели пользователя. 
    """
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.exclude(pk=self.instance.pk).filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Такой email уже существует!")
        return email

class ProfileEditForm(forms.ModelForm):
    """
    Форма редактирования дополнительной информации о пользователе. 
    """
    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")