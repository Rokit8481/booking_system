from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@receiver(pre_save, sender=Booking)
def send_status_change_email(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_instance = Booking.objects.get(pk=instance.pk)

    if old_instance.status != instance.status:
        subject = "Зміна статусу бронювання"
        message = (
            f"Вітаємо, {instance.user.username}!\n\n"
            f"Статус вашого бронювання кімнати №{instance.room.number} змінився.\n"
            f"Новий статус: {instance.get_status_display()}\n\n"
            f"Дата та час початку: {instance.start_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"Дата та час завершення: {instance.end_time.strftime('%Y-%m-%d %H:%M')}\n\n"
            f"Дякуємо, що обрали нас!"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
