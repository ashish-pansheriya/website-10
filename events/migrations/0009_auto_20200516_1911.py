# Generated by Django 3.0.5 on 2020-05-16 13:41

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20200515_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]