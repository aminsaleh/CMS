from django.urls import path

from .views import *

urlpatterns = [
    path('ride/', RideView.as_view()),
    path('courier/', CourierView.as_view()),
    path('customer/', CustomerView.as_view()),
    path('bonus/', ExtraIncomeView.as_view()),
    path('penalty/', PenaltyView.as_view()),
    path('dailyincome/', DailyIncomeView.as_view()),
    path('weekldyincome/', WeeklyIncomeView.as_view()),
]
