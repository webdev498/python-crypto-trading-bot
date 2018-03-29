# Generated by Django 2.0.3 on 2018-03-29 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MoonMachine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketinfo',
            name='userId',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='userId',
        ),
        migrations.AddField(
            model_name='marketinfo',
            name='user',
            field=models.ForeignKey(db_column='user_id', db_index=False, default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(db_column='user_id', db_index=False, default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]