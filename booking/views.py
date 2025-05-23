# Booking/booking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Room, Booking
from django.http import HttpResponse
from datetime import datetime

def index(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, template_name="booking_pages/index.html", context=context)

def room_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, template_name="booking_pages/rooms_list.html", context=context)

def book_room(request, location_id):
    room = get_object_or_404(Room, pk=location_id)
    if request.method == "POST":
        start_time_str = request.POST.get("start_time")
        end_time_str = request.POST.get("end_time")

        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            start_time=start_time,
            end_time=end_time
        )
        return redirect("booking-details", pk=booking.id)
    else:
        context = {
            "room": room
        }
        return render(request, template_name="booking_pages/booking_form.html", context=context)

def booking_details(request, pk):
    try:
        booking = Booking.objects.get(id=pk)
        context = {
            "booking": booking
        }
        return render(request, template_name="booking_pages/booking_details.html", context=context)
    except Booking.DoesNotExist:
        return HttpResponse("This booking doesn't exist", status=404)

def custom_404_view(request, exception):
    return render(request, 'booking_pages/404.html', status=404)