from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from apps.groups.models import Group  # To'g'ridan-to'g'ri import qilamiz

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
    
    # String o'rniga to'g'ridan-to'g'ri Group modelini ishlatamiz
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="O'quvchi guruhi"
    )

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