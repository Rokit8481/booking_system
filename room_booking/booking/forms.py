from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['email', 'birth_date', 'start_time', 'end_time']
        widgets = {
            'email': forms.EmailInput(attrs = {'placeholder': 'youremail@example.com'}),
            'birth_date': forms.DateInput(attrs = {'type': 'date'}),
            'start_time': forms.DateTimeInput(attrs = {'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs = {'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)

        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['birth_date'].input_formats = ['%Y-%m-%d']

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if not birth_date:
            raise ValidationError("Дата народження потрібна.")
        
        today = timezone.now().date() 
        if birth_date >= today:
            raise ValidationError("Ваша дата народження не є можливою!")
        
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise ValidationError("Ви занадто молодий!")
        
        return birth_date

    def clean_start_time(self):
        start = self.cleaned_data.get('start_time')
        if start and start < timezone.now():
            raise ValidationError("Не можна бронювати на минуле.")
        
        return start

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')

        if start and end:
            if end <= start:
                self.add_error('end_time', ValidationError("Кінцева дата має бути пізніше початкової."))
            room = self.room or getattr(self.instance, 'room', None)
            if not room:
                raise ValidationError("Не вказана кімната для перевірки доступності.")
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
