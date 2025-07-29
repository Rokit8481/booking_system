from django.core.exceptions import ValidationError
from .models import Booking, Room
from django.utils import timezone
from django import forms

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')
        room  = getattr(self.instance, 'room', None)

        if start and end:
            if end <= start:
                raise ValidationError("Кінцева дата має бути пізніше початкової.")

            overlapping = Booking.objects.filter(
                room=room,
                start_time__lt=end,
                end_time__gt=start,
            )
            if self.instance.pk:
                overlapping = overlapping.exclude(pk=self.instance.pk)

            if overlapping.exists():
                raise ValidationError("Вибрані дати перетинаються з існуючим бронюванням.")

        return cleaned

    def clean_start_time(self):
        value = self.cleaned_data['start_time']
        if value < timezone.now():
            raise ValidationError("Не можна бронювати на минуле")
        return value