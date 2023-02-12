from django.urls import path, include

urlpatterns = [
   path('user/', include('User.urls')),
   path('crud/', include('crud.urls')),
]