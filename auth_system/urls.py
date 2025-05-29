from django.urls import path
from auth_system import views

urlpatterns = [
    path("register/", views.register, name="register")
]