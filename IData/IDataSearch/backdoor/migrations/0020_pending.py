# Generated by Django 3.0.4 on 2020-06-05 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backdoor', '0019_auto_20200604_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.TextField()),
                ('extract', models.TextField()),
                ('recommend', models.TextField()),
            ],
        ),
    ]
