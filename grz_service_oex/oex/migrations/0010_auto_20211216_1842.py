# Generated by Django 3.2.9 on 2021-12-16 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oex', '0009_auto_20211216_1301'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DisplaySpace',
            new_name='WorkSpace',
        ),
        migrations.RenameModel(
            old_name='DisplaySpacePosition',
            new_name='WorkSpacePosition',
        ),
    ]
