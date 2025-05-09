from django.shortcuts import render, redirect
from booking.models import *
from django.http import HttpResponse

def index(request):
    context = {
        "render_string": "Hello world!"
    }
    # return HttpResponse(status=400)
    return render(request, template_name="booking/index.html", context=context)

def room_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, template_name="booking/rooms_list.html", context=context)

def book_room(request):
    if request.method == "POST":
        room_number = request.POST.get("room_number")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        try:
            room = Room.objects.get(number=room_number)
        except ValueError:
            return HttpResponse(
                "Wrong value for room number",
                status=400
            )
        except Room.DoesNotExist:
            return HttpResponse(
                "This booking doesn't exist",
                status=404
            )

        booking = Booking.objects.create(
            user = request.user,
            room=room,
            start_time=start_time,
            end_time=end_time
        )
        return redirect("booking-details", pk=booking.id)
    else:
        return render(request, template_name="booking/booking_form.html")

def booking_details(request, pk):
    try:
        booking = Booking.objects.get(id=pk)
        context = {
            "booking": booking
        },
        return render(request, template_name="booking/booking_details.html", context=context)
    except Booking.DoesNotExist:
        return HttpResponse(
            "This booking doesn't exist",
            status=404
        )