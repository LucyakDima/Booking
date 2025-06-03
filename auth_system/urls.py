from django.urls import path
from auth_system import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_request_view, name="login_request"),
    path("login/confirm/<uidb64>/<token>/", views.login_confirm_view, name="login_confirm"),
    # path('send-booking-email/<int:booking_id>/', views.send_booking_confirmation_email, name='send-booking-email'),
    # path('activation/<int:pk>/<str:token>/', views.ActivationView.as_view(), name='activation'),
]