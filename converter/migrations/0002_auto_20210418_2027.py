# Generated by Django 3.1.7 on 2021-04-18 12:27

import converter.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='txt_file',
        ),
        migrations.AddField(
            model_name='story',
            name='text_file',
            field=models.FileField(null=True, upload_to=converter.models.Story.update_filename),
        ),
    ]