# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-19 16:13
from __future__ import unicode_literals

import colorful.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import durationfield.db.models.fields.duration
import fk.fields
import model_utils.fields


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# fk.migrations.0004_msfield_to_durationfield
# fk.migrations.0005_add_created_time_for_video

def duration_millisecond_to_microsecond(apps, schema_editor):
    for modelname in ['Scheduleitem', 'Video', 'WeeklySlot']:
        Model = apps.get_model('fk', modelname)
        for item in Model.objects.all():
            # Old duration used milliseconds, new one uses microseconds
            if item.duration:
                item.duration = item.duration * 1000
                item.save()

def noop(*args):
    return None

def add_created_time(apps, schema_editor):
    Model = apps.get_model('fk', 'Video')
    for item in Model.objects.filter(created_time__isnull=True):
        alternatives = [
            item.uploaded_time,
            item.updated_time,
        ]
        try:
            item.created_time = min(a for a in alternatives if a)
        except ValueError:
            pass
        else:
            item.save(update_fields=['created_time'])




class Migration(migrations.Migration):

    replaces = [(b'fk', '0001_initial'), (b'fk', '0002_schedulepurpose_strategies'), (b'fk', '0003_asrun'), (b'fk', '0004_msfield_to_durationfield'), (b'fk', '0005_add_created_time_for_video'), (b'fk', '0006_video_upload_token'), (b'fk', '0007_auto_20170603_1412'), (b'fk', '0008_remove_colorful_20180819_1810')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('rgb', colorful.fields.RGBColorField()),
                ('desc', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'Category',
                'verbose_name': 'video category',
                'verbose_name_plural': 'video categories',
            },
        ),
        migrations.CreateModel(
            name='FileFormat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, max_length=255, null=True, unique=True)),
                ('fsname', models.CharField(max_length=20)),
                ('rgb', colorful.fields.RGBColorField(default=b'cccccc')),
            ],
            options={
                'db_table': 'ItemType',
                'verbose_name': 'video file format',
                'verbose_name_plural': 'video file formats',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('fkmember', models.BooleanField(default=False)),
                ('orgnr', models.CharField(blank=True, max_length=255)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'Organization',
            },
        ),
        migrations.CreateModel(
            name='Scheduleitem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('default_name', models.CharField(blank=True, max_length=255)),
                ('schedulereason', models.IntegerField(blank=True, choices=[(1, b'Legacy'), (2, b'Administrative'), (3, b'User'), (4, b'Automatic')])),
                ('starttime', models.DateTimeField()),
                ('duration', fk.fields.MillisecondField()),
            ],
            options={
                'db_table': 'ScheduleItem',
                'verbose_name': 'TX schedule entry',
                'verbose_name_plural': 'TX schedule entries',
            },
        ),
        migrations.CreateModel(
            name='SchedulePurpose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, default=b'', max_length=255, null=True)),
                ('mailing_address', models.CharField(blank=True, default=b'', max_length=512, null=True)),
                ('post_code', models.CharField(blank=True, default=b'', max_length=255, null=True)),
                ('city', models.CharField(blank=True, default=b'', max_length=255, null=True)),
                ('country', models.CharField(blank=True, default=b'', max_length=255, null=True)),
                ('legacy_username', models.CharField(blank=True, default=b'', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('header', models.TextField(blank=True, max_length=2048, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=2048, null=True)),
                ('has_tono_records', models.BooleanField(default=False)),
                ('is_filler', models.BooleanField(default=False)),
                ('publish_on_web', models.BooleanField(default=True)),
                ('proper_import', models.BooleanField(default=False)),
                ('played_count_web', models.IntegerField(default=0, help_text=b'Number of times it has been played')),
                ('updated_time', models.DateTimeField(help_text=b'Time the program record has been updated', null=True)),
                ('uploaded_time', models.DateTimeField(help_text=b'Time the program record was created', null=True)),
                ('framerate', models.IntegerField(default=25000, help_text=b'Framerate of master video in thousands / second')),
                ('ref_url', models.CharField(blank=True, help_text=b'URL for reference', max_length=1024)),
                ('duration', fk.fields.MillisecondField()),
                ('categories', models.ManyToManyField(to=b'fk.Category')),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(help_text=b'Organization for video', null=True, on_delete=django.db.models.deletion.CASCADE, to='fk.Organization')),
            ],
            options={
                'db_table': 'Video',
                'get_latest_by': 'uploaded_time',
            },
        ),
        migrations.CreateModel(
            name='VideoFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=256)),
                ('old_filename', models.CharField(max_length=256)),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fk.FileFormat')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fk.Video')),
            ],
            options={
                'verbose_name': 'video file',
                'verbose_name_plural': 'video files',
            },
        ),
        migrations.CreateModel(
            name='WeeklySlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('duration', durationfield.db.models.fields.duration.DurationField()),
                ('purpose', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fk.SchedulePurpose')),
            ],
            options={
                'ordering': ('day', 'start_time', 'pk'),
            },
        ),
        migrations.AddField(
            model_name='schedulepurpose',
            name='direct_videos',
            field=models.ManyToManyField(blank=True, to=b'fk.Video'),
        ),
        migrations.AddField(
            model_name='schedulepurpose',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fk.Organization'),
        ),
        migrations.AddField(
            model_name='scheduleitem',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fk.Video'),
        ),
        migrations.AddField(
            model_name='schedulepurpose',
            name='strategy',
            field=models.CharField(choices=[(b'latest', b'latest'), (b'random', b'random'), (b'least_scheduled', b'least_scheduled')], default='latest', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedulepurpose',
            name='type',
            field=models.CharField(choices=[(b'videos', b'videos'), (b'organization', b'organization')], default='videos', max_length=32),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AsRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('program_name', models.CharField(blank=True, default=b'', max_length=160)),
                ('playout', models.CharField(blank=True, default=b'main', max_length=255)),
                ('played_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('in_ms', models.IntegerField(blank=True, default=0)),
                ('out_ms', models.IntegerField(blank=True, null=True)),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fk.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='scheduleitem',
            name='duration',
            field=durationfield.db.models.fields.duration.DurationField(),
        ),
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=durationfield.db.models.fields.duration.DurationField(),
        ),
        migrations.RunPython(
            code=duration_millisecond_to_microsecond,
        ),
        migrations.AddField(
            model_name='video',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, help_text=b'Time the program record was created', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=durationfield.db.models.fields.duration.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, help_text=b'Time the program record has been updated', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='uploaded_time',
            field=models.DateTimeField(blank=True, help_text=b'Time the original video for the program was uploaded', null=True),
        ),
        migrations.RunPython(
            code=add_created_time,
            reverse_code=noop,
        ),
        migrations.AddField(
            model_name='video',
            name='upload_token',
            field=models.CharField(blank=True, default=b'', help_text=b'Code for upload', max_length=32),
        ),
        migrations.AddField(
            model_name='videofile',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, help_text=b'Time the video  file was created', null=True),
        ),
        migrations.AlterField(
            model_name='videofile',
            name='old_filename',
            field=models.CharField(default=b'', max_length=256),
        ),
        migrations.RemoveField(
            model_name='category',
            name='rgb',
        ),
        migrations.RemoveField(
            model_name='fileformat',
            name='rgb',
        ),
        migrations.AlterField(
            model_name='videofile',
            name='old_filename',
            field=models.CharField(blank=True, default=b'', max_length=256),
        ),
    ]
