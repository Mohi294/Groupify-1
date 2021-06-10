# Generated by Django 3.2.4 on 2021-06-10 19:37

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0001_initial'),
        ('collaborate', '0007_auto_20210606_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='topic',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='topic', to='topic.topic'),
        ),
    ]
