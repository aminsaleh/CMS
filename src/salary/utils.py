import logging
from datetime import datetime, timedelta

from django.db import transaction

from .models import Courier, DailyIncome, WeeklyIncome
from .serializers import DailyIncomeSerializer, WeeklyIncomeSerializer

logger = logging.getLogger(__name__)

def get_saturday(day: datetime) -> datetime:
    if day.weekday() == 5:
        return day
    if day.weekday() == 6:
        return day - timedelta(1)
    else:
        return day - timedelta(day.weekday()+2)


def assign(ride: dict) -> object:
    """_summary_

    Args:
        ride (dict): ride info with these keys: [
            ride_distance,
            courier_distance,
            customer_type,
            price,
        ]

    Returns:
        object: A courier object (django ORM object of courier)
    """
    return Courier.objects.last().pk


def update_income(req_day: datetime, courier: Courier, volume: float) -> None:
    """ This function will update daily and weekly table
    based on time, courier, and amount. 

    Args:
        time (datetime): Time of the request
        courier (Courier object): The courier object of that courier
        volume (float): The amount of any change in courier income
    """

    daily_existance = DailyIncome.objects.filter(date=req_day, courier=courier).first()
    weekly_existance = WeeklyIncome.objects.filter(saturday=get_saturday(req_day), courier=courier).first()
    
    if daily_existance:
        with transaction.atomic():
            daily_existance.amount=daily_existance.amount+volume
            daily_existance.save()

    if not daily_existance:
        with transaction.atomic():
            new_row = {
                'date': req_day,
                'courier': courier,
                'amount': volume,
            }
            serializer = DailyIncomeSerializer(data=new_row)
            
            if serializer.is_valid():
                serializer.save()
            else:
                logger.error(f'Daily serializer is not valid!')

    if weekly_existance:
        with transaction.atomic():
            weekly_existance.amount=weekly_existance.amount+volume
            weekly_existance.save()

    if not weekly_existance:
        with transaction.atomic():
            new_row = {
                'saturday': get_saturday(req_day),
                'courier': courier,
                'amount': volume,
            }
            serializer = WeeklyIncomeSerializer(data=new_row)
            if serializer.is_valid():
                serializer.save()
            else:
                logger.error('Weekly serializer is not valid!')
