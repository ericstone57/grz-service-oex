# Generated by Django 3.2.9 on 2021-12-17 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oex', '0011_rename_name_workspaceposition_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workspaceposition',
            old_name='display_space',
            new_name='work_space',
        ),
    ]