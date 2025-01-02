# Generated by Django 5.0 on 2025-01-02 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_answer_id_alter_candidate_id_alter_question_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('degree', models.CharField(blank=True, max_length=30, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('photo', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='age',
        ),
        migrations.AddField(
            model_name='candidate',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_one',
            field=models.TextField(default='This is true'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='option1',
            field=models.TextField(default='Option 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='option2',
            field=models.TextField(default='Option 2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='option3',
            field=models.TextField(default='Option 3'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='is_mandatory',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='test',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.author'),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]