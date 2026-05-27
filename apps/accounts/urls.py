from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.RateLimitedLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
