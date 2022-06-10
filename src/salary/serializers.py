from rest_framework import serializers

from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = '__all__'



class RideSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ride
        fields = '__all__'

    def validate_price(self, value):
        if value<0:
            raise serializers.ValidationError('Negative ride price entered!')
        else: 
            return value

class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = ('id', 'name')

    def validate_id(self, value):
        if len(value) == 10:
            return value
        else:
            raise serializers.ValidationError(f'National id has {len(value)} digits')

class ExtraIncomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExtraIncome
        fields = '__all__'


class PenaltySerializer(serializers.ModelSerializer):

    class Meta:
        model = Penalty
        fields = '__all__'

class DailyIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyIncome
        fields = '__all__'

class WeeklyIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeeklyIncome
        fields = '__all__'
