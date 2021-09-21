import django
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import Profile, CreateSemester, EditSemester, DeleteSemester, CreateDiscipline, EditDisciplineKM, \
    EditDisciplineMarks, DeleteDiscipline
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('session', views.session, name='session'),
    path('progress', views.progress, name='progress'),
    path('profile', Profile.as_view()),
    path('semesters/create', CreateSemester.as_view()),
    path('semesters', EditSemester.as_view()),
    path('semesters/delete', DeleteSemester.as_view()),
    path('semesters/discipline/create', CreateDiscipline.as_view()),
    path('semesters/discipline/delete', DeleteDiscipline.as_view()),
    path('semesters/discipline', EditDisciplineKM.as_view()),
    path('semesters/discipline_marks', EditDisciplineMarks.as_view())
    # path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
]