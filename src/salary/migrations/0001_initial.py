# Generated by Django 4.0.5 on 2022-06-03 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('income', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('type', models.CharField(help_text='\n            types should be one of this list:\n            []\n        ', max_length=200, verbose_name='type of customer for calculating ride price')),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('ride_distance', models.FloatField()),
                ('courier_distance', models.FloatField()),
                ('price', models.FloatField()),
                ('assigned_courier', models.ForeignKey(on_delete=models.SET('Courier is not exist'), to='salary.courier')),
                ('customer_type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='salary.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('courier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='salary.courier')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('courier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='salary.courier')),
            ],
        ),
    ]
