# Generated by Django 3.2.9 on 2022-02-25 04:58

from django.db import migrations, models
import django.utils.timezone
import ks_shared.django.model_utils
import model_utils.fields
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        migrations.CreateModel(
            name='User',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('openid', models.CharField(blank=True, db_index=True, max_length=30)),
                ('unionid', models.CharField(blank=True, db_index=True, default='', max_length=30)),
                ('name', models.CharField(blank=True, db_index=True, default='', max_length=255)),
                ('cellphone', models.CharField(blank=True, default='', max_length=20)),
                ('email', models.CharField(blank=True, default='', max_length=255)),
                ('birthday', models.DateField(blank=True, default=None, null=True)),
                ('gender', model_utils.fields.StatusField(choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')], default='unknown', max_length=100, no_check_for_status=True)),
                ('city', models.CharField(blank=True, default='', max_length=100)),
                ('province', models.CharField(blank=True, default='', max_length=100)),
                ('country', models.CharField(blank=True, default='', max_length=100)),
                ('language', models.CharField(blank=True, default='', max_length=100)),
                ('avatar_url', models.CharField(blank=True, default='', help_text='avatar url', max_length=255)),
                ('avatar', models.ImageField(blank=True, default=None, null=True, upload_to=ks_shared.django.model_utils.upload_to_without_rename)),
                ('last_login_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('last_info_updated_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('raw_data', models.JSONField(blank=True, default=dict)),
                ('utm_campaign', models.CharField(blank=True, default='', max_length=255)),
                ('utm_source', models.CharField(blank=True, default='', max_length=255)),
                ('seed', shortuuid.django_fields.ShortUUIDField(alphabet='23456789abcdefghijkmnopqrstuvwxyz', db_index=True, length=7, max_length=7, prefix='')),
                ('role', model_utils.fields.StatusField(choices=[('user', 'User'), ('storekeeper', 'storekeeper')], default='user', max_length=100, no_check_for_status=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
