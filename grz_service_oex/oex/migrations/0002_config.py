# Generated by Django 3.2.9 on 2021-12-08 11:09

from django.db import migrations, models
import django.utils.timezone
import ks_shared.django.model_utils
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('oex', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=255)),
                ('value', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]