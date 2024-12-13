from django.db import models
from datetime import datetime, time, timedelta
from django.utils import timezone


# Create your models here.
class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('saturday', 'شنبه'),
        ('sunday', 'یکشنبه'),
        ('monday', 'دوشنبه'),
        ('tuesday', 'سه‌شنبه'),
        ('wednesday', 'چهارشنبه'),
        ('thursday', 'پنج‌شنبه'),
        ('friday', 'جمعه'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} ({self.start_time} - {self.end_time})"




class Reservation(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reservation_time = models.TimeField()
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    reserved_at = models.DateTimeField(auto_now_add=True)
    user = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('time_slot', 'reservation_time')

    def __str__(self):
        return f"{self.time_slot.day} {self.reservation_time} - {self.name}"

    @property
    def user_count(self):
        return Reservation.objects.filter(time_slot=self.time_slot, reservation_time=self.reservation_time).count()

    def reset_user_count(self):
        midnight = datetime.combine(timezone.now().date(), time(0, 0))
        if timezone.now() >= midnight:
            self.user = 0
            self.save()
