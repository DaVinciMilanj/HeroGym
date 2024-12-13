from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import ReservationForm
from .models import Reservation, TimeSlot


# Create your views here.
class WeekDateView(generic.ListView):
    model = TimeSlot
    template_name = 'reserve/week-date.html'
    context_object_name = 'week'

    def get_queryset(self):
        return TimeSlot.objects.all()


class ReservationCreateView(generic.CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reserve/reserve-time.html'

    def get_initial(self):
        initial = super().get_initial()
        time_slot_id = self.kwargs.get('time_slot_id')
        time_slot = get_object_or_404(TimeSlot, id=time_slot_id)
        initial['time_slot'] = time_slot
        return initial

    def get_context_data(self, **kwargs):
        """
        ارسال داده‌های اضافی به قالب
        """
        context = super().get_context_data(**kwargs)
        time_slot_id = self.kwargs.get('time_slot_id')
        time_slot = get_object_or_404(TimeSlot, id=time_slot_id)

        # تولید گزینه‌ها برای reservation_time
        form = context.get('form')
        if form:
            form.fields['reservation_time'].choices = ReservationForm.generate_half_hour_slots(time_slot)

        # بازه‌های زمانی رزرو شده
        reserved_times = Reservation.objects.filter(time_slot=time_slot).values_list('reservation_time', flat=True)
        context['reserved_times'] = reserved_times
        return context

    def form_valid(self, form):
        """
        اعتبارسنجی فرم قبل از ذخیره
        """
        time_slot_id = self.kwargs.get('time_slot_id')
        time_slot = get_object_or_404(TimeSlot, id=time_slot_id)
        form.instance.time_slot = time_slot

        # بررسی ظرفیت
        if Reservation.objects.filter(time_slot=time_slot,
                                      reservation_time=form.cleaned_data['reservation_time']).count() >= 10:
            messages.error(self.request, 'ظرفیت این بازه زمانی پر شده است.')
            return self.form_invalid(form)

        messages.success(self.request, 'رزرو با موفقیت انجام شد!')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(self.request.POST)  # چاپ داده‌های ارسال‌شده به سرور
        print(form.errors)  # چاپ خطاهای فرم
        return super().form_invalid(form)

    def get_success_url(self):
        """
        آدرس صفحه‌ای که بعد از موفقیت در ذخیره نمایش داده می‌شود
        """
        time_slot_id = self.kwargs.get('time_slot_id')  # دریافت ID بازه زمانی
        return reverse_lazy('home:home')
