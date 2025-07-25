from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Booking
from django.http import HttpRequest
from django.utils import timezone


def room_list(request: HttpRequest):
    rooms = Room.objects.all().order_by('-number')
    return render(request, 'booking/room_list.html', {
        'rooms': rooms
    })

def room(request: HttpRequest, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'room.html', {
        'room': room,
    })

@login_required
def book_room(request: HttpRequest, pk):
    room = get_object_or_404(Room, pk = pk)
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if not start_time or not end_time:
            return render(request, 'book_room.html', {
                'room': room,
                'error': 'Потрібно вказати початок і кінець бронювання.'
            })
        Booking.objects.create(
            user = request.user , 
            room=room,
            start_time=start_time,
            end_time=end_time
        )
        return redirect('my_bookings')  

@login_required
def cancel_booking(request: HttpRequest, pk: int):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('my_bookings')
    return render(request, 'cancel_booking.html', {'booking': booking})


@login_required
def my_bookings(request: HttpRequest):
    user = request.user
    now = timezone.now()
    future_bookings = Booking.objects.filter(user = user, start_time__gte=now).order_by('start_time')
    past_bookings = Booking.objects.filter(user = user, end_time__lt=now).order_by('-start_time')
    return render(request, 'my_bookings.html', {
        'future_bookings': future_bookings,
        'past_bookings': past_bookings
    })

def login_view(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('room_list')
        else:
            return render(request, 'login.html', {'error': 'Неправильні дані для входу'})
    return render(request, 'login.html')


def logout_view(request: HttpRequest):
    logout(request)
    return redirect('login')

def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
