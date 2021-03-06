# Generated by Django 3.2.9 on 2021-12-07 07:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ks_shared.django.model_utils
import model_utils.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplaySpace',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('cover', models.ImageField(upload_to=ks_shared.django.model_utils.upload_to)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exhibition',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('cover', models.ImageField(upload_to=ks_shared.django.model_utils.upload_to)),
                ('cover_s', models.ImageField(upload_to=ks_shared.django.model_utils.upload_to)),
                ('start_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('end_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('favorite_count', models.IntegerField(default=0)),
                ('intro', models.CharField(blank=True, default='', max_length=2000)),
                ('curator', models.CharField(blank=True, default='', max_length=512)),
                ('author', models.CharField(blank=True, default='', max_length=512)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LinkType',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('cover', models.ImageField(upload_to=ks_shared.django.model_utils.upload_to)),
                ('price', models.DecimalField(blank=True, decimal_places=6, default=None, max_digits=9, null=True)),
                ('status', model_utils.fields.StatusField(choices=[('on', 'on'), ('offline', 'offline')], default='offline', max_length=100, no_check_for_status=True)),
                ('status_text', models.CharField(max_length=100)),
                ('intro', models.CharField(blank=True, default='', max_length=2000)),
                ('size', models.CharField(blank=True, default='', max_length=100)),
                ('copyright', models.CharField(blank=True, default='', max_length=100)),
                ('inventory', models.IntegerField(default=0)),
                ('exhibition', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oex.exhibition')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('cover', models.ImageField(upload_to=ks_shared.django.model_utils.upload_to)),
                ('cover_s', models.ImageField(upload_to=ks_shared.django.model_utils.upload_to)),
                ('address', models.CharField(blank=True, default='', max_length=512)),
                ('province', models.CharField(blank=True, default='', max_length=100)),
                ('city', models.CharField(blank=True, default='', max_length=100)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, default=None, max_digits=9, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, default=None, max_digits=9, null=True)),
                ('intro', models.CharField(blank=True, default='', max_length=2000)),
                ('opentime_from', models.TimeField()),
                ('opentime_to', models.TimeField()),
                ('favorite_count', models.IntegerField(default=0)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(blank=True, default='', max_length=512)),
                ('wxmp_appid', models.CharField(blank=True, default='', max_length=100)),
                ('wxmp_pagepath', models.CharField(blank=True, default='', max_length=512)),
                ('type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oex.linktype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='exhibition',
            name='space',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oex.space'),
        ),
        migrations.CreateModel(
            name='DisplaySpacePosition',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('display_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oex.displayspace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='displayspace',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oex.space'),
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('pic', models.ImageField(upload_to=ks_shared.django.model_utils.upload_to)),
                ('display_order', models.IntegerField(default=100)),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published')], default='draft', max_length=100, no_check_for_status=True)),
                ('published_at', model_utils.fields.MonitorField(blank=True, default=None, monitor='status', null=True, when={'published'})),
                ('link', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oex.link')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
