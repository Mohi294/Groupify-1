# Generated by Django 3.2.4 on 2021-06-22 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collaborate', '0011_auto_20210620_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gp_rate',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='related_group', to='collaborate.group'),
        ),
    ]