from django.urls import path
from booking import views

urlpatterns = [
   path("", views.index, name="index"),
   path("room-lisr/", views.room_list , name="rooms-list"),
   path("book-room/<int:location_id>/", views.book_room, name="book-room"),
   path("booking-details/<int:pk>/", views.booking_details, name="booking-details"),
]