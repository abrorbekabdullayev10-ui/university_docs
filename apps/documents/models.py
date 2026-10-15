from django.db import models
from django.conf import settings


class DocumentTemplate(models.Model):
    """Hujjat shabloni"""
    title = models.CharField("Shablon nomi", max_length=200)
    description = models.TextField("Tavsif", blank=True)
    content = models.TextField("Shablon matni", blank=True)
    is_active = models.BooleanField("Faol", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Shablon"
        verbose_name_plural = "Shablonlar"
        ordering = ['title']

    def __str__(self):
        return self.title


class StudentDocument(models.Model):
    """O'quvchi to'ldirgan hujjat"""
    STATUS_DRAFT = 'draft'
    STATUS_SUBMITTED = 'submitted'
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Javonda"),
        (STATUS_SUBMITTED, "Yuborilgan"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="O'quvchi"
    )
    template = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.CASCADE,
        related_name='student_documents',
        verbose_name="Shablon"
    )
    content = models.TextField("Hujjat mazmuni", blank=True)
    file = models.FileField("Fayl", upload_to='documents/', blank=True, null=True)
    status = models.CharField(
        "Holat",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )
    
    # Yangi maydonlar
    teacher_score = models.IntegerField("O'qituvchi bahosi", null=True, blank=True, help_text="0-100 orasida")
    teacher_comment = models.TextField("O'qituvchi izohi", blank=True)
    allow_teacher_view_draft = models.BooleanField(
        "O'qituvchiga javonni ko'rishga ruxsat berish",
        default=False,
        help_text="Agar belgilansa, o'qituvchi bu hujjatni javonda ham ko'ra oladi"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "O'quvchi hujjati"
        verbose_name_plural = "O'quvchi hujjatlari"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.student.username} - {self.template.title} ({self.get_status_display()})"