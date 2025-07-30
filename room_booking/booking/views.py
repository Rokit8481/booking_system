from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Room, Booking
from django.http import HttpRequest
from django.utils import timezone
from .forms import BookingForm


def room_list(request: HttpRequest):
    rooms = Room.objects.all().order_by('-number')
    return render(request, 'booking/room_list.html', {
        'rooms': rooms
    })

def room(request: HttpRequest, pk):
    room = get_object_or_404(Room, pk=pk)
    images = room.images.all()
    return render(request, 'booking/room.html', {
        'room': room,
        'images': images
    })

@login_required
def book_room(request: HttpRequest, pk: int):
    room = get_object_or_404(Room, pk=pk)
    booking = Booking(user=request.user, room=room)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/book_room.html', {
        'form': form,
        'room': room,
    })

@login_required
def cancel_booking(request: HttpRequest, pk: int):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('my_bookings')
    return render(request, 'booking/my_bookings.html', {'booking': booking})

@login_required
def edit_booking(request: HttpRequest, pk: int):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/edit_booking.html', {
        'form': form,
        'booking': booking
    })

@login_required
def my_bookings(request: HttpRequest):
    user = request.user
    now = timezone.now()
    future_bookings = Booking.objects.filter(user = user, start_time__gte=now).order_by('start_time')
    active_bookings = Booking.objects.filter(user=user, start_time__lte=now, end_time__gte=now).order_by('start_time')
    past_bookings = Booking.objects.filter(user = user, end_time__lt=now).order_by('-start_time')
    return render(request, 'booking/my_bookings.html', {
        'future_bookings': future_bookings,
        'past_bookings': past_bookings,
        'active_bookings': active_bookings
    })

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('room_list')
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')

def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
