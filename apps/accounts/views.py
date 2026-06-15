from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods, require_POST
from django_ratelimit.decorators import ratelimit

from apps.accounts.forms import LoginForm, RegisterForm


@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="5/m", method="POST")
def register(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    if request.method == "POST" and getattr(request, "limited", False):
        messages.error(request, "Слишком много попыток регистрации. Подождите минуту.")
        return render(request, "accounts/register.html", {"form": RegisterForm()})
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("core:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@method_decorator(ratelimit(key="ip", rate="20/m", method="POST"), name="dispatch")
class RateLimitedLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        if getattr(request, "limited", False):
            messages.error(request, "Слишком много попыток входа. Подождите минуту.")
            return redirect("accounts:login")
        return super().post(request, *args, **kwargs)


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("core:home")
