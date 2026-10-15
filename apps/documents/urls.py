from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
path('student/vault/<int:pk>/toggle-teacher/', views.student_toggle_teacher_view, name='student_toggle_teacher_view'),
path('teacher/student/<int:student_id>/vault/', views.student_vault_by_teacher_view, name='student_vault_by_teacher'),
path('teacher/score/<int:pk>/', views.teacher_score_view, name='teacher_score'),
path('', views.documents_hub_view, name='documents_hub'),
path('student/vault/', views.student_vault_view, name='student_vault'),
path('student/vault/<int:pk>/toggle/', views.student_vault_toggle_view, name='student_vault_toggle'),
path('teacher/vault/', views.teacher_vault_view, name='teacher_vault'),
path('api/template/<int:pk>/', views.get_template_content, name='get_template_content'),
path('teacher/<int:pk>/', views.teacher_document_view, name='teacher_document_view'),    
path('student/', views.student_documents_view, name='student_documents'),
    path('student/create/', views.student_document_create_view, name='student_document_create'),
    path('student/<int:pk>/edit/', views.student_document_edit_view, name='student_document_edit'),
    path('student/<int:pk>/delete/', views.student_document_delete_view, name='student_document_delete'),
    path('teacher/', views.teacher_documents_view, name='teacher_documents'),
]