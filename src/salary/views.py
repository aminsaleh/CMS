import logging
from datetime import datetime, timezone

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .utils import assign, update_income

logger = logging.getLogger(__name__)

def today():
    return datetime.now(timezone.utc).replace(
        hour=0, minute=0,
        second=0, microsecond=0,
    )

class RideView(APIView):
    serializer_class = RideSerializer

    def get(self, request):
        ride = Ride.objects.all()
        serializer = RideSerializer(ride, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):

        new_ride = {
            'ride_distance': request.data['ride_distance'],
            'courier_distance': request.data['courier_distance'],
            'customer_type': Customer.objects.get(name=request.data['customer']).pk,
            'price': request.data['price'],
        }
        new_ride['assigned_courier'] = assign(ride=new_ride)
        
        update_income(
            req_day=today(),
            courier=new_ride['assigned_courier'],
            volume=new_ride['price'],
        )
        logger.info(f"New ride updated a courier income. Courier national id: {new_ride['assigned_courier']}")

        serializer = RideSerializer(data=new_ride)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerView(APIView):
    serializer_class = CustomerSerializer

    def get(self, request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourierView(APIView):
    serializer_class = CourierSerializer

    def get(self, request):
        courier = Courier.objects.all()
        serializer = CourierSerializer(courier, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):

        courier_data = {
            'id': request.data['national_id'],
            'name': request.data['name'],
        }

        serializer = CourierSerializer(data=courier_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExtraIncomeView(APIView):
    serializer_class = ExtraIncomeSerializer

    def get(self, request):
        extra_incomes = ExtraIncome.objects.all()
        serializer = ExtraIncomeSerializer(extra_incomes, many=True)
        return Response(serializer.data)
    
    @transaction.atomic
    def post(self, request):
        income_data = {
            'courier': request.data['courier_national_id'],
            'amount': request.data['amount'],
        }

        serializer = ExtraIncomeSerializer(data=income_data)
        
        update_income(
            req_day=today(),
            courier=income_data['courier'],
            volume=income_data['amount'],
        )
        logger.info(f"New bonus updated a courier income. Courier national id: {income_data['courier']}")

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PenaltyView(APIView):
    serializer_class = PenaltySerializer

    def get(self, request):
        penalties = Penalty.objects.all()
        serializer = ExtraIncomeSerializer(penalties, many=True)
        return Response(serializer.data)
    
    @transaction.atomic
    def post(self, request):
        penalty_body = {
            'courier': request.data['courier_national_id'],
            'amount': request.data['amount'],
        }

        serializer = PenaltySerializer(data=penalty_body)

        update_income(
            req_day=today(),
            courier=penalty_body['courier'],
            volume=-penalty_body['amount'],
        )
        logger.info(f"New penalty updated a courier income. Courier national id: {penalty_body['courier']}")
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DailyIncomeView(APIView):
    serializer_class = DailyIncomeSerializer

    def get(self, request):
        daily_body = request.data
        daily_by_id = DailyIncome.objects.filter(
            courier=daily_body['national_id'],
            date=datetime.strptime(daily_body['date'], '%Y/%m/%d').replace(tzinfo=timezone.utc),
        )
        serializer = DailyIncomeSerializer(daily_by_id, many=True)

        return Response(serializer.data)
        
class WeeklyIncomeView(APIView):
    serializer_class = WeeklyIncomeSerializer

    def get(self, request):
        weekly_body = {
            'courier': request.data['national_id'],
            'from_date': datetime.strptime(request.data['from_date'], '%Y/%m/%d').replace(tzinfo=timezone.utc),
            'to_date': datetime.strptime(request.data['to_date'], '%Y/%m/%d').replace(tzinfo=timezone.utc),
        }
        
        weekly_by_id = WeeklyIncome.objects.filter(
            courier=weekly_body['courier'],
            saturday__gte=weekly_body['from_date'],
            saturday__lte=weekly_body['to_date'],
        )
        serializer = WeeklyIncomeSerializer(data=weekly_by_id, many=True)

        return Response(serializer.data)
