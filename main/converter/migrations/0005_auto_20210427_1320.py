# Generated by Django 3.1.7 on 2021-04-27 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0004_auto_20210426_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='scene',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='converter.scene'),
        ),
    ]
