# Generated by Django 3.0.5 on 2020-04-22 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0007_auto_20200417_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='age',
            field=models.CharField(choices=[('junior', '18-20'), ('senior', '20-30'), ('young', '30-40'), ('adult', '40-60')], max_length=10, null=True),
        ),
    ]
