from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('teacher/groups/', views.teacher_groups_view, name='teacher_groups'),
    path('', views.login_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]