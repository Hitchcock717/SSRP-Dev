# Generated by Django 3.0.4 on 2020-03-16 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backdoor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=50)),
                ('source', models.CharField(max_length=10)),
                ('info', models.TextField()),
                ('date', models.TextField()),
                ('kws', models.CharField(max_length=50)),
                ('cited', models.PositiveIntegerField()),
                ('downed', models.PositiveIntegerField()),
                ('download', models.URLField()),
                ('abstract', models.TextField()),
                ('fund', models.TextField()),
            ],
            options={
                'verbose_name': 'idataspider',
            },
        ),
        migrations.DeleteModel(
            name='IDataSpider',
        ),
    ]
