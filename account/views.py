from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm

def user_login(request):
    """
    Представление для входа на сайт.
    Если предоставленны данные - они проверяются и происходит вход на сайт,
    иначе отображается пустая форма.
    Выдаёт сообщения об ошибке при неправильных данных пользователя
    и отсутствия пользователя в базе данных.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                return HttpResponse("Успешная авторизация.")
            else:
                return HttpResponse("Такого пользователя не существует!")
        else:
            return HttpResponse("Не правильный логин или пароль!")
    else:
        form = LoginForm()
    return render(
        request, "account/login.html", {"form": form}
    )

def register(request):
    """
    Представленкие для регистрации пользователей. Если переданы данные из формы,
    они проверяются и создаётся запись пользователя в БД, или отображается
    пустая форма для регистрации.
    """
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            context = {"new_user": new_user}
            return render(
                request, "account/register_done.html", context
                )
    else:
        user_form = UserRegistrationForm()
        return render(
            request, "account/register.html",
            {"user_form": user_form}
            )
        

@login_required
def dashboard(request):
    """
    Страница профиля.
    Только если пользователь авторизоваался.
    """
    return render(
        request, "account/dashboard.html",
        {"section": "dashboard"}
    )