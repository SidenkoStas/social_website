from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm

def user_login(request):
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

@login_required
def dashboard(request):
    return render(
        request, "account/dashboard.html",
        {"section": "dashboard"}
    )