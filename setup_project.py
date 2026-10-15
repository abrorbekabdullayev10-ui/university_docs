import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 1. config/settings.py
settings_content = '''from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-2026')
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.groups',
    'apps.documents',
    'apps.resources',
    'apps.messaging',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'university_docs_db',
        'USER': 'uni_user',
        'PASSWORD': 'uni_pass_2026',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''

with open(BASE_DIR / 'config' / 'settings.py', 'w', encoding='utf-8') as f:
    f.write(settings_content)

# 2. config/urls.py
urls_content = '''from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Universitet Hujjatlar Tizimi — ADMIN"
admin.site.site_title = "Admin Panel"
admin.index_title = "Boshqaruv markazi"

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''

with open(BASE_DIR / 'config' / 'urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)

# 3. apps/accounts/apps.py
accounts_apps_content = '''from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = "Foydalanuvchilar va Rollar"
'''

with open(BASE_DIR / 'apps' / 'accounts' / 'apps.py', 'w', encoding='utf-8') as f:
    f.write(accounts_apps_content)

# 4. apps/accounts/models.py
accounts_models_content = '''from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class Role(models.TextChoices):
    TEACHER = 'teacher', "O'qituvchi"
    STUDENT = 'student', "O'quvchi"

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username majburiy")
        user = self.model(username=username, email=self.normalize_email(email or ''), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', Role.TEACHER)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    full_name = models.CharField("Ism Familiya", max_length=150, blank=True)

    objects = CustomUserManager()

    class Meta:
        ordering = ['full_name', 'username']

    def __str__(self):
        return f"{self.full_name or self.username} ({self.get_role_display()})"

    @property
    def is_teacher(self):
        return self.role == Role.TEACHER

    @property
    def is_student(self):
        return self.role == Role.STUDENT
'''

with open(BASE_DIR / 'apps' / 'accounts' / 'models.py', 'w', encoding='utf-8') as f:
    f.write(accounts_models_content)

# 5. apps/accounts/admin.py
accounts_admin_content = '''from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'full_name', 'email')
    ordering = ('role', 'username')

    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumot", {'fields': ('role', 'full_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Qo'shimcha ma'lumot", {'fields': ('role', 'full_name', 'email')}),
    )
'''

with open(BASE_DIR / 'apps' / 'accounts' / 'admin.py', 'w', encoding='utf-8') as f:
    f.write(accounts_admin_content)

print("✅ Barcha fayllar muvaffaqiyatli yaratildi!") 
