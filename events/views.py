import uuid
import qrcode

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.db import models
from django.db.models import Count, Q
from .models import Event, Registration, Profile
from .forms import UserRegisterForm

# -------------------------
# REGISTER USER
# -------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# -------------------------
# DASHBOARD
# -------------------------
@login_required
def dashboard(request):
    events = Event.objects.filter(registration_deadline__gt=timezone.now())
    profile = request.user.profile

    registrations = Registration.objects.filter(student=request.user)

    registered_event_ids = registrations.values_list('event_id', flat=True)

    context = {
        'events': events,
        'profile': profile,
        'registrations': registrations,
        'registered_event_ids': registered_event_ids
    }

    return render(request, 'dashboard.html', context)
# -------------------------
# REGISTER FOR EVENT + GENERATE QR
# -------------------------
@login_required
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Profile.objects.create(
                user=user,
                mobile_number=form.cleaned_data['mobile_number']
            )

            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, "register.html", {"form": form})
    # registration logic continues

    # Generate unique QR code string
    unique_code = str(uuid.uuid4())

    # Create registration entry
    registration = Registration.objects.create(
        event=event,
        student=request.user,
        qr_code=unique_code
    )

    # Generate QR image
    qr = qrcode.make(unique_code)

    # Ensure media folder exists (SAFE WAY)
    import os
    media_dir = os.path.join(settings.BASE_DIR, "media")
    os.makedirs(media_dir, exist_ok=True)

    # Save QR image
    qr_file_path = os.path.join(media_dir, f"{unique_code}.png")
    qr.save(qr_file_path)

    print("QR saved at:", qr_file_path)  # Debug line

    messages.success(request, "Registered successfully! QR generated.")
    return redirect('my_qr', reg_id=registration.id)

# -------------------------
# SHOW QR PAGE
# -------------------------
@login_required
def my_qr(request, reg_id):
    registration = get_object_or_404(
        Registration,
        id=reg_id,
        student=request.user
    )

    return render(request, 'qr_display.html', {
        'registration': registration
    })


# -------------------------
# LEADERBOARD
# -------------------------
def leaderboard(request):
    profiles = Profile.objects.order_by('-total_points')
    return render(request, 'leaderboard.html', {
        'profiles': profiles
    })
@login_required
def unregister_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    registration = Registration.objects.filter(
        event=event,
        student=request.user
    ).first()

    if registration:
        registration.delete()
        messages.success(request, "Unregistered successfully.")

    return redirect('dashboard')
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def mark_attendance(request, reg_id):
    registration = get_object_or_404(Registration, id=reg_id)

    if not registration.attended:
        registration.attended = True
        registration.save()

        profile = registration.student.profile
        profile.total_points += registration.event.points
        profile.update_badge()  # <-- IMPORTANT

        messages.success(request, "Attendance marked and points + badge updated!")
    else:
        messages.info(request, "Attendance already marked.")

    return redirect('admin:index')

@staff_member_required
def admin_dashboard(request):
    total_events = Event.objects.count()
    total_registrations = Registration.objects.count()
    total_attended = Registration.objects.filter(attended=True).count()

    attendance_rate = 0
    if total_registrations > 0:
        attendance_rate = round((total_attended / total_registrations) * 100, 2)

    # Event-wise analytics
    event_stats = Event.objects.annotate(
        total_registered=Count('registration'),
        total_attended=Count('registration', filter=models.Q(registration__attended=True))
    )

    return render(request, 'admin_dashboard.html', {
        'total_events': total_events,
        'total_registrations': total_registrations,
        'total_attended': total_attended,
        'attendance_rate': attendance_rate,
        'event_stats': event_stats,
    })
@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # prevent duplicate registration
    already_registered = Registration.objects.filter(
        student=request.user,
        event=event
    ).exists()

    if not already_registered:
        Registration.objects.create(
            student=request.user,
            event=event
        )

    return redirect('dashboard')