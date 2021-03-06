# Generated by Django 3.2.9 on 2021-12-10 06:41

from django.db import migrations, models
import django.db.models.deletion
import ks_shared.django.model_utils


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('oex', '0003_alter_space_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedThrough',
            fields=[
                ('object_id', models.CharField(default=ks_shared.django.model_utils.generate_uuid, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oex_taggedthrough_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
