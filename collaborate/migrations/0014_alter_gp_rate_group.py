# Generated by Django 3.2.4 on 2021-06-22 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collaborate', '0013_alter_gp_rate_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gp_rate',
            name='group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='related_group', to='collaborate.group'),
        ),
    ]
