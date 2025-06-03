# Booking/booking/views.py
from django.contrib import messages
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

    capacity_min = request.GET.get('capacity_min')
    capacity_max = request.GET.get('capacity_max')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    start_time_str = request.GET.get('start_time')
    end_time_str = request.GET.get('end_time')

    if start_time_str and end_time_str:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)

        booked_rooms = Booking.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        ).values_list('room', flat=True)
        rooms = rooms.exclude(id__in=booked_rooms)

    if capacity_min:
        rooms = rooms.filter(capacity__gte=capacity_min)
    if capacity_max:
        rooms = rooms.filter(capacity__lte=capacity_max)
    if min_price:
        rooms = rooms.filter(price__gte=min_price)
    if max_price:
        rooms = rooms.filter(price__lte=max_price)

    context = {
        "rooms": rooms,
    }
    return render(request, template_name="booking_pages/rooms_list.html", context=context)

def book_room(request, location_id):
    room = get_object_or_404(Room, pk=location_id)
    message = None
    if request.method == "POST":
        start_time_str = request.POST.get("start_time")
        end_time_str = request.POST.get("end_time")

        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)

        if end_time < start_time:
            message = "Дата закінчення бронювання не може бути раніше дати початку."
        else:
            existing_bookings = Booking.objects.filter(room=room, start_time__lt=end_time, end_time__gt=start_time)
            if existing_bookings.exists():
                next_available_date = existing_bookings.order_by('end_time').first().end_time
                message = f"Кімната вже заброньована. Вона звільниться {next_available_date}."
            else:
                duration = (end_time - start_time).total_seconds() / 3600
                total_price = room.price * duration

                booking = Booking.objects.create(
                    user=request.user,
                    room=room,
                    start_time=start_time,
                    end_time=end_time
                )
                return redirect("booking-details", pk=booking.id)

    context = {
        "room": room,
        "message": message
    }
    return render(request, template_name="booking_pages/booking_form.html", context=context)


def booking_details(request, pk):
    try:
        booking = Booking.objects.get(id=pk)
        total_price = booking.room.price * (booking.end_time - booking.start_time).total_seconds() / 3600

        context = {
            "booking": booking,
            "total_price": total_price,
        }
        return render(request, template_name="booking_pages/booking_details.html", context=context)
    except Booking.DoesNotExist:
        return HttpResponse("This booking doesn't exist", status=404)


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect("rooms-list")
