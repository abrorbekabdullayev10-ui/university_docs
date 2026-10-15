from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Prefetch
from .forms import RegisterForm
from apps.groups.models import Group, Direction
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.is_teacher:
        # O'qituvchi uchun: Barcha yo'nalishlar va guruhlar, ichidagi o'quvchilar bilan
        directions = Direction.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.prefetch_related('customuser_set'))
        ).all()
        return render(request, 'teacher/dashboard.html', {'directions': directions})
    else:
        # O'quvchi uchun
        return render(request, 'student/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def teacher_groups_view(request):
    """O'qituvchi uchun guruhlar va o'quvchilar ro'yxati"""
    if not request.user.is_teacher:
        return redirect('dashboard')
    
    from apps.groups.models import Direction
    directions = Direction.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.prefetch_related('customuser_set'))
    ).all()
    
    return render(request, 'teacher/groups.html', {'directions': directions})