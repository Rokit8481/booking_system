from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('room/<int:pk>/', views.room, name='room'),
    path('room/<int:pk>/book/', views.book_room, name='book_room'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/edit/', views.edit_booking, name='edit_booking'), 
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
