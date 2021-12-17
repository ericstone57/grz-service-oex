# Generated by Django 3.2.9 on 2021-12-15 13:03

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('oex', '0007_genericstringtaggeditem_is_strike_through'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedThrough',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, max_length=50, verbose_name='Object id')),
                ('is_strike_through', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oex_taggedthrough_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oex_taggedthrough_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='GenericStringTaggedItem',
        ),
        migrations.AlterField(
            model_name='space',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='oex.TaggedThrough', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
