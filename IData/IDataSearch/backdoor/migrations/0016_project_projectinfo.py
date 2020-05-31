# Generated by Django 3.0.4 on 2020-05-31 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backdoor', '0015_auto_20200522_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Projectinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.TextField()),
                ('date', models.TextField()),
                ('type', models.TextField()),
                ('source', models.TextField()),
                ('description', models.TextField()),
                ('method', models.TextField()),
                ('extract', models.TextField()),
                ('recommend', models.TextField()),
            ],
        ),
    ]
