# Generated by Django 5.0.6 on 2024-06-06 07:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='hackersDB',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=1000)),
                ('photo', models.ImageField(blank=True, upload_to='hacker_photos')),
                ('linkdin', models.TextField(blank=True, max_length=10000)),
                ('instagram', models.TextField(blank=True, max_length=10000)),
                ('github', models.TextField(blank=True, max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='studentsDB',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=300)),
                ('section', models.CharField(blank=True, default='', max_length=100)),
                ('year', models.CharField(blank=True, default='', max_length=100)),
                ('RollNo', models.CharField(blank=True, default='', max_length=10)),
                ('semester', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.CharField(blank=True, default='', max_length=1000)),
                ('password', models.CharField(blank=True, default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tid', models.CharField(blank=True, default='', max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.BooleanField(default=False)),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.lecture')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.studentsdb')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.teacher'),
        ),
    ]
