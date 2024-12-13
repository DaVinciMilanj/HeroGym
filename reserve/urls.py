from django.urls import path
from . import views

app_name = 'reserve'
urlpatterns = [
    path('reservation' , views.WeekDateView.as_view() , name='week-date'),
    path('reservation/<int:time_slot_id>/', views.ReservationCreateView.as_view(), name='reserve')

]
