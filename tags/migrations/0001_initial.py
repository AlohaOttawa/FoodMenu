# Generated by Django 3.0.4 on 2020-06-07 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0010_auto_20200607_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('menuitem', models.ManyToManyField(blank=True, to='menu.MenuItem')),
            ],
        ),
    ]
