from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from .views import home, logout, roborts_view,student_dashboard,add_edit_lecture,forget_pass,student_login,student_signup, teacher_dashboard, teacher_login, teacher_signup

urlpatterns = [
    path("",home,name="homepage"),
    path("robots.txt/",roborts_view ,name="roborts_view"),
    path("forget_pass/",forget_pass ,name="forgot_password"),
    path("logout/",logout ,name="logout"),

    path("student/",lambda request: redirect('homepage')),
    path("student/login",student_login,name="student_login"),
    path("student/signup",student_signup,name="student_signup"),
    path("student/dashboard",student_dashboard,name="student_dashboard"),

    path("teacher/",lambda request: redirect('homepage')),
    path("teacher/login",teacher_login,name="teacher_login"),
    path("teacher/signup",teacher_signup,name="teacher_signup"),
    path("teacher/dashboard",teacher_dashboard,name="teacher_dashboard"),
    path("teacher/add_edit_lecture",add_edit_lecture,name="add_edit_lecture"),
]
