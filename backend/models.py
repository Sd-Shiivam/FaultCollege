import datetime
from django.db import models


class hackersDB(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1000, default='', blank=True)
    photo = models.ImageField(blank=True, upload_to='hacker_photos')
    linkdin = models.TextField(max_length=10000,blank=True)
    instagram = models.TextField(max_length=10000,blank=True)
    github = models.TextField(max_length=10000,blank=True)

    def __str__(self):
        return f"{self.name}"

class studentsDB(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, default='', blank=True)
    RollNo = models.CharField(max_length=10, default='', blank=True)
    email = models.CharField(max_length=1000, default='', blank=True)
    password = models.CharField(max_length=1000, default='', blank=True)

    def __str__(self):
        return f"{self.name} | {self.email}"

class Lecture(models.Model):
    topic = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.topic} - {self.teacher}"


class Attendance(models.Model):
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE)
    student = models.ForeignKey('studentsDB', on_delete=models.CASCADE)
    attended = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.student} - {self.lecture} | {"Persent" if self.attended else "Absent"}"

class Teacher(models.Model):
    Tid=models.CharField(max_length=10, default='', blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=1000)

    def __str__(self):
        return self.name