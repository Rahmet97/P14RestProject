# Generated by Django 4.2.6 on 2023-11-15 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_subscriber_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]