# Generated by Django 3.2.4 on 2021-06-06 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collaborate', '0005_messenger'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_pending',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='GP_Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(max_length=10)),
                ('duration', models.IntegerField(max_length=53)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_group', to='collaborate.group')),
                ('rated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reted_user', to=settings.AUTH_USER_MODEL)),
                ('rating_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reting_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Avg_Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user',),
            },
        ),
    ]
