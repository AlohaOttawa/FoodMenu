# Generated by Django 3.0.4 on 2020-06-03 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20200603_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]