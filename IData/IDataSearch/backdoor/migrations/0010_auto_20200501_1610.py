# Generated by Django 3.0.4 on 2020-05-01 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backdoor', '0009_collection_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='flag',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='collection',
            name='folder',
            field=models.TextField(default=''),
        ),
    ]
