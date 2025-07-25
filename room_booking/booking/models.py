from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.IntegerField(unique = True)
    description = models.TextField(blank = True)
    capacity = models.IntegerField()
    price_per_hour = models.DecimalField(max_digits = 6, decimal_places = 2)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"Кімната {self.number}"
    
    class Meta:
        verbose_name = "Кімната"
        verbose_name_plural = "Кімнати"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete = models.CASCADE, related_name = 'bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(
        max_length = 20, 
        choices = [
            ('pending', 'Очікує підтвердження'),
            ('confirmed', 'Підтверджено'),
            ('cancelled', 'Скасовано')
        ],
        default = 'pending'
    )

    def __str__(self):
        return f"{self.user.username} | Кімната {self.room.number} | {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"