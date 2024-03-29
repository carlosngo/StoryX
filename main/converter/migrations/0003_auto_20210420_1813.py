# Generated by Django 3.1.7 on 2021-04-20 10:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0002_auto_20210418_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference_start', models.IntegerField()),
                ('reference_end', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('event_number', models.IntegerField()),
                ('actor_start', models.IntegerField()),
                ('actor_end', models.IntegerField()),
                ('sentence_start', models.IntegerField()),
                ('sentence_end', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='story',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='ActionEvent',
            fields=[
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='converter.event')),
                ('verb', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='converter.entity')),
            ],
        ),
        migrations.CreateModel(
            name='DialogueEvent',
            fields=[
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='converter.event')),
                ('content_start', models.IntegerField()),
                ('content_end', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Prop',
            fields=[
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='converter.entity')),
            ],
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('scene_number', models.IntegerField()),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='converter.story')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='scene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='converter.scene'),
        ),
        migrations.AddField(
            model_name='entity',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='converter.story'),
        ),
        migrations.CreateModel(
            name='TransitionEvent',
            fields=[
                ('action_event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='converter.actionevent')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='character',
            field=models.ManyToManyField(to='converter.Character'),
        ),
        migrations.AddField(
            model_name='event',
            name='prop',
            field=models.ManyToManyField(to='converter.Prop'),
        ),
        migrations.AddField(
            model_name='actionevent',
            name='prop',
            field=models.ManyToManyField(to='converter.Prop'),
        ),
    ]
