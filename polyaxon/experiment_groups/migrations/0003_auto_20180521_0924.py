# Generated by Django 2.0.3 on 2018-05-21 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment_groups', '0002_auto_20180505_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='experimentgroupstatus',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'Experiment group Statuses'},
        ),
    ]
