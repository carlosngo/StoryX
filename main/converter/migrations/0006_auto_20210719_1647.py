# Generated by Django 3.1.7 on 2021-07-19 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0005_auto_20210427_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_transition',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TransitionEvent',
        ),
    ]
