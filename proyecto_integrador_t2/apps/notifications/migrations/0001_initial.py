# Generated by Django 5.1.1 on 2024-11-15 15:06

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('Success', 'success'), ('Info', 'info'), ('Wrong', 'wrong')], default='Info', max_length=20)),
                ('object_id_actor', models.PositiveIntegerField()),
                ('verb', models.CharField(max_length=220)),
                ('read', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('url', models.URLField(blank=True, null=True)),
                ('actor_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notication_actor', to='contenttypes.contenttype')),
                ('destinity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
