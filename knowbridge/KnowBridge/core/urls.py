from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('get_started/', views.get_started, name='get_started'),
    path('role_selection/', views.role_selection, name='role_selection'),
    path('login_teacher/', views.login_teacher, name='login_teacher'),
    path('login_student/', views.login_student, name='login_student'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('hello/', views.hello, name='hello'),
    path('logout/', views.user_logout, name='logout'), 
    path('contact/',views.contact, name='contact'),
    path('generate_mcq_tests/', views.generate_mcq_tests, name='generate_mcq_tests'),
    path('confirm_mcq_tests/', views.confirm_mcq_tests, name='confirm_mcq_tests'),

]