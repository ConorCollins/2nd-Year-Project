# Generated by Django 4.1.7 on 2023-04-05 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_alter_extra_options'),
        ('cart', '0002_alter_moviecartitem_numseats_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviecartitem',
            name='numSeats',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='moviecartitem',
            name='seats',
            field=models.ManyToManyField(to='cinema.seat'),
        ),
    ]
