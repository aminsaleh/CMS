# Generated by Django 4.0.5 on 2022-06-07 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0002_alter_courier_id_alter_courier_income_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='id',
            field=models.TextField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='National ID'),
        ),
    ]