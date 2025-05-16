from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Room, Booking
from django.http import HttpResponse

def index(request):
    rooms = Room.objects.all()  # Отримати всі кімнати
    context = {
        "rooms": rooms,
    }
    return render(request, template_name="booking/index.html", context=context)

def room_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, template_name="booking/rooms_list.html", context=context)

def book_room(request, location_id):
    room = get_object_or_404(Room, pk=location_id)
    if request.method == "POST":

        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        # Створюємо бронювання
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            start_time=start_time,
            end_time=end_time
        )
        return redirect("booking-details", pk=booking.id)
    else:
        # Повертаємо назву кімнати в контекст
        context = {
            "room": room  # Додаємо назву кімнати в контекст
        }
        return render(request, template_name="booking/booking_form.html", context=context)


def booking_details(request, pk):
    try:
        booking = Booking.objects.get(id=pk)
        context = {
            "booking": booking
        }
        return render(request, template_name="booking/booking_details.html", context=context)
    except Booking.DoesNotExist:
        return HttpResponse("This booking doesn't exist", status=404)
