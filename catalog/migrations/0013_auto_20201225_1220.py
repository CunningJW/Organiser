# Generated by Django 3.1.4 on 2020-12-25 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0012_auto_20201225_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='performer',
            field=models.ForeignKey(help_text='Who will need to complete it?', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_for', to=settings.AUTH_USER_MODEL),
        ),
    ]
