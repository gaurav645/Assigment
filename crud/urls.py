from django.urls import path
from django.contrib import admin
from .views import BlogView

urlpatterns = [
   path('blog/', BlogView.as_view()),
]