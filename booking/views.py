# Booking/booking/views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Room, Booking
from django.http import HttpResponse
from datetime import datetime
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


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

        now = datetime.now()
        if start_time < now or end_time < now:
            messages.error(request, "Не можна шукати кімнати у минулому.")
            return redirect("rooms-list")

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

from datetime import datetime

def book_room(request, location_id):
    room = get_object_or_404(Room, pk=location_id)
    message = None
    if request.method == "POST":
        start_time_str = request.POST.get("start_time")
        end_time_str = request.POST.get("end_time")
        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
            now = datetime.now()
            if start_time < now or end_time < now:
                message = "Неможливо забронювати на час, який уже минув."
            elif end_time <= start_time:
                message = "Дата закінчення бронювання не може бути раніше або рівна даті початку."
            else:
                existing_bookings = Booking.objects.filter(
                    room=room,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )
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

        except ValueError:
            message = "Неправильний формат дати й часу."

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

def booking_rooms_list(request):
    bookings = Booking.objects.filter(user=request.user).select_related("room")
    return render(request, "booking_pages/booking_list.html", {"bookings": bookings})


def send_confirmation_link(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    token = default_token_generator.make_token(booking.user)
    uid = urlsafe_base64_encode(force_bytes(booking.pk))
    confirm_url = request.build_absolute_uri(reverse('confirm-booking', kwargs={'uidb64': uid, 'token': token}))
    send_mail(
        'Підтвердження бронювання',
        f'Натисніть для підтвердження бронювання: {confirm_url}',
        settings.EMAIL_HOST_USER,
        [booking.email],
        fail_silently=False,
    )

    messages.success(request, 'Посилання для підтвердження надіслано на пошту.')
    return redirect('booking-details', pk=booking_id)

def confirm_booking(request, uidb64, token):
    try:
        booking_id = force_str(urlsafe_base64_decode(uidb64))
        booking = Booking.objects.get(pk=booking_id)
    except (TypeError, ValueError, OverflowError, Booking.DoesNotExist):
        booking = None

    if booking and default_token_generator.check_token(booking.user, token):
        booking.is_confirm = True
        booking.save()
        messages.success(request, 'Бронювання підтверджено.')
        return redirect('booking-list')
    else:
        messages.error(request, 'Посилання недійсне або протерміноване.')
        return redirect('booking-details', pk=booking_id if booking else 1)