from django.contrib import admin
from .models import DocumentTemplate, StudentDocument


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'template', 'status', 'updated_at')
    list_filter = ('status', 'template')
    search_fields = ('student__username', 'template__title')