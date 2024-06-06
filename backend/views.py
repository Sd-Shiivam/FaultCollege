import random
import base64
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Attendance, Lecture, Teacher, hackersDB, studentsDB

def checklogin(session_cookies):
    if not session_cookies:
        return redirect("homepage")
    
    uid, utype = str(session_cookies).split("#")
    
    if utype == "11":
        if not studentsDB.objects.filter(id=uid).exists():
            return redirect("homepage")
    elif utype == "22":
        if not Teacher.objects.filter(id=uid).exists():
            return redirect("homepage")

def home(request):
    if request.session.get('CookiesId'):
        return redirect("student_dashboard")
    
    parms = {
        "source_code": "hello",
        "hackers": hackersDB.objects.all()
    }
    return render(request, "home_page.html", parms)


def forget_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        uid = request.POST.get('id')
        is_teacher = request.POST.get('teacher', False)
        try:
            if is_teacher:
                teacher = Teacher.objects.get(email=email, Tid=uid)
                password = teacher.password
            else:
                student = studentsDB.objects.get(email=email, RollNo=uid)
                password = student.password
                password = base64.b64decode(password.encode()).decode()
            messages.success(request, f'Your Password is - {password}.')
            return redirect('forgot_password')
        except (studentsDB.DoesNotExist, Teacher.DoesNotExist):
            messages.error(request, 'No user found with that email and ID.')
            return redirect('forget_password')
    else:
        return render(request, "forgot_password_page.html")

def logout(request):
    try:
        request.session['CookiesId'] = ""
    except:
        pass
    return redirect("homepage")

def student_login(request):
    if request.session.get('CookiesId'):
        if request.session['CookiesId'].endswith("#11"):
            return redirect('student_dashboard')
        else:
            return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        codePass = base64.b64encode(password.encode()).decode()
        try:
            student = studentsDB.objects.get(email=email, password=codePass)
            request.session['CookiesId'] = str(student.id) + "#" + "11"
            return redirect('student_dashboard')
        except studentsDB.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('student_login')
    else:
        return render(request, "student_login_page.html")

def generate_unique_uid(utype):
    while True:
        uid = ''.join(random.choices('0123456789', k=6))
        if utype == 11:
            if not studentsDB.objects.filter(RollNo=uid).exists():
                return uid
        elif utype == 22:
            if not Teacher.objects.filter(Tid=uid).exists():
                return uid

def student_signup(request):
    if not request.session.get('CookiesId'):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('student_signup')
            codedPass = base64.b64encode(password.encode()).decode()
            uid = generate_unique_uid(11)
            student = studentsDB.objects.create(name=name, email=email, password=codedPass, RollNo=uid)
            request.session['CookiesId'] = str(student.id) + "#" + "11"
            return redirect('student_dashboard')
        else:
            return render(request, "student_signup_page.html")
    else:
        return redirect('student_dashboard')

def student_dashboard(request):
    if not request.session.get('CookiesId'):
        return redirect("homepage")
    if request.session['CookiesId'].endswith("#22"):
        return redirect('teacher_dashboard')
    uId=request.session['CookiesId'].split("#")[0]
    myprofile=studentsDB.objects.get(id=uId)
    myattended=Attendance.objects.filter(student=myprofile)
    total_present=myattended.filter(attended=True).count()
    if myattended.count() > 0:
        percentage=((total_present*100)/myattended.count())
    else:
        percentage=0
    parm={
        "profile":myprofile,
        "percentage":percentage,
        "myclsses":myattended
    }
    return render(request, "student_dashboard_page.html",parm)


def teacher_login(request):
    if request.session.get('CookiesId'):
        if request.session['CookiesId'].endswith("#22"):
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            teacher = Teacher.objects.get(email=email)
            if teacher.password == password:
                request.session['CookiesId'] = str(teacher.Tid) + "#" + "22"
                return redirect('teacher_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('teacher_login')
        except Teacher.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('teacher_login')
    else:
        return render(request, "teacher_login_page.html")

def teacher_signup(request):
    if not request.session.get('CookiesId'):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('teacher_signup')
            uid=generate_unique_uid(22)
            teacher = Teacher.objects.create(Tid=uid,name=name, email=email, password=password)
            request.session['CookiesId'] = str(teacher.Tid) + "#" + "22"
            return redirect('teacher_dashboard')
        else:
            return render(request, "teacher_signup_page.html")
    else:
        return redirect('teacher_dashboard')

def teacher_dashboard(request):
    if not request.session.get('CookiesId'):
        return redirect("homepage")
    tid=str(request.session.get('CookiesId')).split("#")[0]
    try:
        teacher_profile=Teacher.objects.get(Tid=tid)
        lactures=Lecture.objects.filter(teacher=teacher_profile)
        attendance=Attendance.objects.filter(lecture__in=lactures)
        parm={
            "teacher":teacher_profile,
            "lectures":lactures,
            "attendance":attendance
        }
    except:
        return redirect("logout")
    return render(request, "teacher_dashboard_page.html",parm)

def add_edit_lecture(request):
    if not request.session.get('CookiesId'):
        return redirect("teacher_login")
    
    teacher_id = request.session.get('CookiesId', None)
    if teacher_id:
        teacher_id = teacher_id.split("#")[0]
        teacher = Teacher.objects.get(Tid=teacher_id)

        if request.method == 'POST':
            lecture_name = request.POST.get('lecture_name')
            date = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            present_students = request.POST.getlist('present_students')
            lecture_id = request.POST.get('lecture_id')
            if lecture_id:
                lecture = Lecture.objects.get(pk=lecture_id)
                lecture.topic = lecture_name
                lecture.date=date
                lecture.start_time=start_time
                lecture.end_time=end_time
                lecture.save()
            else:
                lecture, created = Lecture.objects.get_or_create(topic=lecture_name,teacher=teacher,date=date,start_time=start_time,end_time=end_time)
            Attendance.objects.filter(lecture=lecture).update(attended=False)
            for student_id in present_students:
                student = studentsDB.objects.get(id=student_id)
                x,y = Attendance.objects.update_or_create(lecture=lecture, student=student)
                x.attended=True
                x.save()

            return redirect('add_edit_lecture')
        else:
            lecture_id = request.GET.get('lecture_id') 
            if lecture_id:
                lecture = Lecture.objects.get(pk=lecture_id)
                Atstudents=Attendance.objects.filter(lecture=lecture)
                student_in_lecture=[]
                for i in Atstudents:
                    if i.attended:
                        student_in_lecture.append(i.student.id)
            else:
                lecture = None
                Atstudents = None
                student_in_lecture=[]
            teacher_profile=Teacher.objects.get(Tid=teacher_id)
            all_lectures=Lecture.objects.filter(teacher=teacher_profile)
            attendance=Attendance.objects.filter(lecture__in=all_lectures)
            students = studentsDB.objects.all() 
            lecture_states=[]
            for l in all_lectures:
                attendance = Attendance.objects.filter(lecture=l)
                attended_count = attendance.filter(attended=True).count()
                total_students = attendance.count()
                if total_students != 0:
                    attendance_percentage = (attended_count / total_students) * 100
                else:
                    attendance_percentage = 0
                lecture_states.append({
                    'pk': l.pk,
                    'topic': l.topic,
                    'name': l.date,
                    'percentage': attendance_percentage,
                })
            parm= {
                'teacher': teacher, 
                'lecture': lecture, 
                'Atstudents': student_in_lecture, 
                'lecture_states': lecture_states, 
                'students': students
                }
            return render(request, "add_edit_lecture_page.html",parm)
    else:
        return redirect('teacher_login')
