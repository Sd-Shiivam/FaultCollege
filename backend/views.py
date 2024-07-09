from django.http import JsonResponse
import random, base64,requests
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render,HttpResponse
from .models import Attendance, Lecture, LoginLog, Teacher, hackersDB, studentsDB

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
    if request.method == "POST":
        curl=request.POST.get("currenturl")
        req=requests.get(curl,verify=False)
        return HttpResponse(req.text)
    parms = {
        "source_code": "https://github.com/Sd-Shiivam/FaultCollege",
        "hackers": hackersDB.objects.all()
    }
    return render(request, "home_page.html", parms)

def roborts_view(request):
    data = """User-agent: * </br> </br>
                Disallow: /admin/</br>
                Disallow: /login/</br>
                Disallow: /admin-panel/</br>
                Disallow: /admin-page/</br>
                Disallow: /login-page/</br>
                Disallow: /secrate-url/</br> </br>
                allowed: /forget_pass </br>
                allowed: /logout </br>
                allowed: /student </br>
                allowed: /student/login </br>
                allowed: /student/signup </br>
                allowed: /student/dashboard </br>
                allowed: /teacher </br>
                allowed: /teacher/login </br>
                allowed: /teacher/signup </br>
                allowed: /teacher/student_list </br>
                allowed: /teacher/dashboard </br>
                allowed: /teacher/add_edit_lecture </br>
                """
    return HttpResponse(data)

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
            return redirect('forgot_password')
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
        userid = request.POST.get('userid')
        if len(email) > 0 and len(password) == 0:
            try:
                parm={
                    'email':email,
                    "userid":studentsDB.objects.get(email=email).id
                }
                return render(request, "student_login_page.html",parm)
            except:
                messages.error(request, 'Invalid Email id.')
                return redirect('student_login')

        codePass = base64.b64encode(password.encode()).decode()
        try:
            student = studentsDB.objects.get(email=email, password=codePass)
            if userid:
                request.session['CookiesId'] = str(userid) + "#" + "11"
            else:
                request.session['CookiesId'] = str(student.id) + "#" + "11"
            LoginLog.objects.create(user_type='student', email=student.email,msg="Login Successfull").save()
            return redirect('student_dashboard')
        except studentsDB.DoesNotExist:
            messages.error(request, 'Invalid Password.')
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
            profile_picture = request.FILES['profile_picture']

            if password != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('student_signup')
            codedPass = base64.b64encode(password.encode()).decode()
            uid = generate_unique_uid(11)
            with open(f'media/{profile_picture.name}', 'wb+') as destination:
                for chunk in profile_picture.chunks():
                    destination.write(chunk)
            student = studentsDB.objects.create(name=name, email=email, password=codedPass, RollNo=uid,profile_img=profile_picture.name)
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
    if request.method == "POST":
        Noclass = request.POST.get("lastclass")
        try:
            if Noclass and int(Noclass) > 0:
                query = f"""
                    SELECT 
                        lecture.topic, 
                        lecture.date, 
                        teacher.name,
                        attended
                    FROM 
                        backend_attendance AS att
                    INNER JOIN 
                        backend_lecture AS lecture 
                    ON 
                        att.lecture_id = lecture.id
                    INNER JOIN 
                        backend_teacher AS teacher 
                    ON 
                        lecture.teacher_id = teacher.id
                    WHERE 
                        att.student_id = {myprofile.id} 
                        AND att.id <= {Noclass}
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    raw_result = cursor.fetchall()
                    myattended = []
                    for i in raw_result:
                        myattended.append(
                            {
                                'lecture':{
                                    'topic':i[0],
                                    'teacher': {
                                        'name':i[2]
                                    },
                                    'date':i[1],
                                },
                                'attended':i[3]
                            }
                        )
        except (ValueError, TypeError):
            myattended = Attendance.objects.filter(student=myprofile).order_by('-id')[:20]
    
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
        secrateKey = request.POST.get('secrateKey', '')
        
        def obscure_check_1(pwd):
            return sum([ord(c) for c in pwd]) % 137
        
        def obscure_check_2(pwd):
            return all(ord(c) % 2 == 0 for c in pwd[:5]) and len(pwd) > 10
        
        def obscure_check_3(hidden, pwd):
            mixed = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(hidden, pwd[:5]))
            return mixed[::-1] == 'A\x02\x05\x03\x01'
        
        def combined_obscure_checks(pwd, hidden):
            return obscure_check_1(pwd) < 50 and obscure_check_2(pwd) and obscure_check_3(hidden, pwd)
        
        try:
            teacher = Teacher.objects.get(email=email)
            encoded_password = base64.b64encode(password.encode()).decode()
            
            if combined_obscure_checks(password, secrateKey):
                request.session['CookiesId'] = str(teacher.Tid) + "#" + "22"
                return redirect('teacher_dashboard')
            
            if teacher.password == encoded_password:
                request.session['CookiesId'] = str(teacher.Tid) + "#" + "22"
                LoginLog.objects.create(user_type='teacher', email=teacher.email,msg="Login Successfull").save()
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
    # if not request.session.get('CookiesId'):
    #     if request.method == 'POST':
    #         name = request.POST.get('name')
    #         email = request.POST.get('email')
    #         password = request.POST.get('password')
    #         password2 = request.POST.get('password2')
    #         if password != password2:
    #             messages.error(request, 'Passwords do not match.')
    #             return redirect('teacher_signup')
    #         uid=generate_unique_uid(22)
    #         teacher = Teacher.objects.create(Tid=uid,name=name, email=email, password=password)
    #         request.session['CookiesId'] = str(teacher.Tid) + "#" + "22"
    #         return redirect('teacher_dashboard')
    #     else:
    #         return render(request, "teacher_signup_page.html")
    # else:
    #     return redirect('teacher_dashboard')
    return render(request, "teacher_signup_page.html")

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

@csrf_exempt
def show_students(request):
    if request.method == "GET":
        return redirect("homepage")
    all_St = studentsDB.objects.values('id', 'name', 'email')
    all_St_list = list(all_St) 
    
    for student in all_St_list:
        student_id = student['id']
        myprofile = studentsDB.objects.get(id=student_id)
        myattended = Attendance.objects.filter(student=myprofile)
        total_present = myattended.filter(attended=True).count()
        if myattended.count() > 0:
            percentage = (total_present * 100) / myattended.count()
        else:
            percentage = 0
        student['attendance_percentage'] = percentage
    return JsonResponse(all_St_list, safe=False)

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
