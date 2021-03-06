# Generated by Django 3.2.9 on 2021-12-13 07:37

from django.db import migrations, models
import django.db.models.deletion
import ks_shared.django.model_utils
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('oex', '0004_taggedthrough'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericStringTaggedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, max_length=50, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oex_genericstringtaggeditem_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oex_genericstringtaggeditem_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='space',
            name='cover',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=ks_shared.django.model_utils.upload_to),
        ),
        migrations.AlterField(
            model_name='space',
            name='cover_s',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=ks_shared.django.model_utils.upload_to),
        ),
        migrations.AlterField(
            model_name='space',
            name='opentime_from',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='space',
            name='opentime_to',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='TaggedThrough',
        ),
        migrations.AlterField(
            model_name='space',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='oex.GenericStringTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
