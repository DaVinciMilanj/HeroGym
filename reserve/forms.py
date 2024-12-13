from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation, TimeSlot
from datetime import datetime, timedelta
from django.utils import timezone


class ReservationForm(forms.ModelForm):
    reservation_time = forms.ChoiceField(choices=[])  # بازنویسی فیلد برای گزینه‌های انتخابی

    class Meta:
        model = Reservation
        fields = ['time_slot', 'reservation_time', 'name', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # بررسی مقداردهی time_slot
        time_slot = self.initial.get('time_slot') or self.instance.time_slot
        if time_slot:
            self.fields['reservation_time'].choices = self.generate_half_hour_slots(time_slot)

    def clean_phone(self):
        """
        بررسی شماره تلفن تکراری در همان روز و برای همان time_slot
        """
        time_slot = self.cleaned_data.get('time_slot')
        reservation_time = self.cleaned_data.get('reservation_time')
        phone = self.cleaned_data.get('phone')

        # دریافت تاریخ امروز
        today = timezone.now().date()

        # بررسی اینکه شماره تلفن در همان روز برای این time_slot رزرو شده باشد
        if Reservation.objects.filter(time_slot=time_slot, reservation_time=reservation_time, phone=phone,
                                      reserved_at__date=today).exists():
            raise ValidationError("این شماره تلفن قبلاً برای این بازه زمانی در امروز رزرو شده است.")

        return phone

    @staticmethod
    def generate_half_hour_slots(time_slot):
        """
        تولید بازه‌های نیم‌ساعته برای یک time_slot
        و علامت‌گذاری بازه‌های رزرو شده
        """
        slots = []
        current_time = datetime.combine(datetime.today(), time_slot.start_time)
        end_time = datetime.combine(datetime.today(), time_slot.end_time)

        # دریافت زمان‌های رزرو شده
        reserved_times = Reservation.objects.filter(time_slot=time_slot).values_list('reservation_time', flat=True)

        while current_time < end_time:
            time_str = current_time.time().strftime("%H:%M")
            if current_time.time() in reserved_times:
                # اگر بازه رزرو شده بود
                slots.append((time_str, f"{time_str} - رزرو شده"))
            else:
                slots.append((time_str, time_str))
            current_time += timedelta(minutes=30)

        return slots

