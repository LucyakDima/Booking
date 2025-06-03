from django.urls import path
from booking import views


urlpatterns = [
   path("", views.index, name="index"),
   path("room-lisr/", views.room_list , name="rooms-list"),
   path("room/<int:location_id>/", views.book_room, name="book-room"),
   path("booking-details/<int:pk>/", views.booking_details, name="booking-details"),
   path("cancel-booking/<int:booking_id>/", views.cancel_booking, name="cancel-booking"),
]


