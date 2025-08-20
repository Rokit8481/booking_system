from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Booking
from room_booking.settings import MEDIA_URL

@receiver(pre_save, sender=Booking)
def send_status_change_email(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_instance = Booking.objects.get(pk=instance.pk)

    if old_instance.status != instance.status:
        subject = "Зміна статусу бронювання"
        context = {
            "user": instance.user,
            "booking": instance,
            "room": instance.room,
            "old_status": old_instance.get_status_display(),
            "static_url": MEDIA_URL,
        }

        text_message = render_to_string("emails/booking_status.txt", context)
        html_message = render_to_string("emails/booking_status.html", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.user.email],  # правильно беремо email користувача
        )
        email.attach_alternative(html_message, "text/html")
        email.send()