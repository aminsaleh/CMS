from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=250, unique=True)
    type = models.CharField(
        max_length=200,
        verbose_name='type of customer for calculating ride price',
        null=False,
        help_text='''
            types should be one of this list:
            []
        '''
    )

class Courier(models.Model):
    id = models.TextField(
        max_length=10,
        verbose_name='National ID',
        primary_key=True,
        unique=True,
        null=False,
    )
    name = models.CharField(max_length=250)
    income = models.FloatField(default=0)

    def __str__(self) -> str:
        return f'Courier, national id: {self.id}'

class Ride(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    assigned_courier = models.ForeignKey(Courier, on_delete=models.SET('Courier is not exist'))
    ride_distance = models.FloatField()
    courier_distance = models.FloatField()
    customer_type = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.FloatField()

class ExtraIncome(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    amount = models.FloatField()

class Penalty(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    amount = models.FloatField()

class DailyIncome(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.FloatField()

class WeeklyIncome(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    saturday = models.DateTimeField()
    amount = models.FloatField()
