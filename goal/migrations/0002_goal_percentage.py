# Generated by Django 5.0.3 on 2024-04-06 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='percentage',
            field=models.IntegerField(null=True),
        ),
    ]
