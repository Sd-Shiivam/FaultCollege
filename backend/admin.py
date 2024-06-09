from django.contrib import admin
from .models import LoginLog, hackersDB,studentsDB,Teacher,Lecture,Attendance

admin.site.name = "faltWeb"
admin.site.register(hackersDB)
admin.site.register(studentsDB)
admin.site.register(Teacher)
admin.site.register(Lecture)
admin.site.register(Attendance)
admin.site.register(LoginLog)