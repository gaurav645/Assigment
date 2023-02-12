from django.contrib import admin
from django.urls import include, path
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    # path('change-password/', ChangePassword.as_view()),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]