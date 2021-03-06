# Generated by Django 3.0.4 on 2020-06-17 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20200612_1811'),
        ('orders', '0002_auto_20200612_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='billing.BillingProfile'),
        ),
    ]
