from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from auth_system.forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from .forms import EmailLoginForm


User = get_user_model()

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # send_email(user, request)
            login(request, user)
            return redirect("index")
        # else:
        #     messages.error(request, "some error")
    else:
        form = CustomUserCreationForm()
        messages.error(request, "some error")

    return render(
        request,
        template_name="auth_system/register.html",
        context={"form": form},
    )


def logout_view(request):
    logout(request)
    return redirect("index")


def login_request_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                login_url = request.build_absolute_uri(
                    reverse('login_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                send_mail(
                    'Ваш лінк для входу',
                    f'Натисніть на посилання для входу: {login_url}',
                    'super_patscan@ukr.net',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Лист із посиланням для входу надіслано.')
            except User.DoesNotExist:
                messages.error(request, 'Користувача з такою поштою не знайдено.')
    else:
        form = EmailLoginForm()

    return render(request, 'auth_system/login_request.html', {'form': form})


def login_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, 'Посилання недійсне або протерміноване.')
        return redirect('login_request')