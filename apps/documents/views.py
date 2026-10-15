from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import DocumentTemplate, StudentDocument
from apps.groups.models import Direction, Group
from apps.accounts.models import CustomUser


@login_required
def documents_hub_view(request):
    """Hujjatlar bo'limi - ikkita karta ko'rsatadi"""
    return render(request, 'documents_hub.html')


@login_required
def student_documents_view(request):
    """O'quvchi o'z hujjatlarini ko'radi"""
    if not request.user.is_student:
        return redirect('dashboard')
    
    documents = StudentDocument.objects.filter(student=request.user).select_related('template')
    templates = DocumentTemplate.objects.filter(is_active=True)
    
    draft_count = documents.filter(status=StudentDocument.STATUS_DRAFT).count()
    submitted_count = documents.filter(status=StudentDocument.STATUS_SUBMITTED).count()
    
    return render(request, 'student/documents.html', {
        'documents': documents,
        'templates': templates,
        'draft_count': draft_count,
        'submitted_count': submitted_count
    })


@login_required
def student_document_create_view(request):
    """O'quvchi yangi hujjat yaratadi"""
    if not request.user.is_student:
        return redirect('dashboard')
    
    if request.method == 'POST':
        template_id = request.POST.get('template')
        content = request.POST.get('content', '')
        file = request.FILES.get('file')
        status = request.POST.get('status', StudentDocument.STATUS_DRAFT)
        
        template = get_object_or_404(DocumentTemplate, id=template_id, is_active=True)
        
        StudentDocument.objects.create(
            student=request.user,
            template=template,
            content=content,
            file=file,
            status=status
        )
        return redirect('documents:student_vault')
    
    templates = DocumentTemplate.objects.filter(is_active=True)
    return render(request, 'student/document_form.html', {'templates': templates})


@login_required
def student_document_edit_view(request, pk):
    """O'quvchi hujjatni tahrirlaydi"""
    if not request.user.is_student:
        return redirect('dashboard')
    
    document = get_object_or_404(StudentDocument, pk=pk, student=request.user)
    
    if request.method == 'POST':
        document.content = request.POST.get('content', document.content)
        
        if 'file' in request.FILES:
            document.file = request.FILES['file']
        
        action = request.POST.get('action')
        if action == 'submit':
            document.status = StudentDocument.STATUS_SUBMITTED
        elif action == 'draft':
            document.status = StudentDocument.STATUS_DRAFT
        
        document.save()
        return redirect('documents:student_vault')
    
    return render(request, 'student/document_form.html', {'document': document})


@login_required
def student_document_delete_view(request, pk):
    """O'quvchi hujjatni o'chiradi"""
    if not request.user.is_student:
        return redirect('dashboard')
    
    document = get_object_or_404(StudentDocument, pk=pk, student=request.user)
    
    if request.method == 'POST':
        document.delete()
        return redirect('documents:student_vault')
    
    return render(request, 'student/document_confirm_delete.html', {'document': document})


@login_required
def student_vault_view(request):
    """O'quvchi uchun javon - barcha hujjatlar ko'z ikonkasi bilan boshqariladi"""
    if not request.user.is_student:
        return redirect('dashboard')
    
    documents = StudentDocument.objects.filter(
        student=request.user
    ).select_related('template').order_by('-updated_at')
    
    return render(request, 'student/vault.html', {'documents': documents})


@login_required
def student_vault_toggle_view(request, pk):
    """O'quvchi ko'z ikonkasi orqali holatni o'zgartiradi"""
    if not request.user.is_student:
        return redirect('dashboard')
    
    document = get_object_or_404(StudentDocument, pk=pk, student=request.user)
    
    if request.method == 'POST':
        if document.status == StudentDocument.STATUS_DRAFT:
            document.status = StudentDocument.STATUS_SUBMITTED
        else:
            document.status = StudentDocument.STATUS_DRAFT
        document.save()
        return redirect('documents:student_vault')
    
    return redirect('documents:student_vault')


@login_required
def teacher_documents_view(request):
    """O'qituvchi yuborilgan va ruxsat berilgan javon hujjatlarini ko'radi"""
    if not request.user.is_teacher:
        return redirect('dashboard')
    
    direction_id = request.GET.get('direction')
    group_id = request.GET.get('group')
    
    # Submitted hujjatlar + ruxsat berilgan draft hujjatlar
    documents = StudentDocument.objects.filter(
        Q(status=StudentDocument.STATUS_SUBMITTED) |
        Q(status=StudentDocument.STATUS_DRAFT, allow_teacher_view_draft=True)
    ).select_related('student', 'template', 'student__group', 'student__group__direction')
    
    if direction_id:
        documents = documents.filter(student__group__direction_id=direction_id)
    if group_id:
        documents = documents.filter(student__group_id=group_id)
    
    directions = Direction.objects.all()
    groups = Group.objects.select_related('direction').all()
    
    return render(request, 'teacher/documents.html', {
        'documents': documents,
        'directions': directions,
        'groups': groups,
        'selected_direction': direction_id,
        'selected_group': group_id,
        'total_count': documents.count()
    })


@login_required
def teacher_document_view(request, pk):
    """O'qituvchi bitta hujjatni ko'radi (submitted yoki ruxsat berilgan draft)"""
    if not request.user.is_teacher:
        return redirect('dashboard')
    
    document = get_object_or_404(StudentDocument, pk=pk)
    
    # Agar draft bo'lsa, ruxsat berilganligini tekshirish
    if document.status == StudentDocument.STATUS_DRAFT:
        if not document.allow_teacher_view_draft:
            return redirect('documents:teacher_vault')
    
    return render(request, 'teacher/document_detail.html', {'document': document})


@login_required
def teacher_vault_view(request):
    """O'qituvchi uchun javon - faqat yuborilgan hujjatlar"""
    if not request.user.is_teacher:
        return redirect('dashboard')
    
    vault_documents = StudentDocument.objects.filter(
        status=StudentDocument.STATUS_SUBMITTED
    ).select_related(
        'student', 'template', 'student__group', 'student__group__direction'
    ).order_by('-updated_at')
    
    directions = Direction.objects.all()
    
    return render(request, 'teacher/vault.html', {
        'vault_documents': vault_documents,
        'directions': directions,
        'total_vault': vault_documents.count()
    })


def get_template_content(request, pk):
    """Shablon matnini JSON formatida qaytaradi"""
    template = get_object_or_404(DocumentTemplate, pk=pk, is_active=True)
    return JsonResponse({
        'title': template.title,
        'content': template.content,
        'description': template.description
    })


@login_required
def teacher_score_view(request, pk):
    """O'qituvchi o'quvchiga baho beradi"""
    if not request.user.is_teacher:
        return redirect('dashboard')
    
    document = get_object_or_404(StudentDocument, pk=pk)
    
    if request.method == 'POST':
        score = request.POST.get('score')
        comment = request.POST.get('comment', '')
        
        if score is not None and score != '':
            document.teacher_score = int(score)
        document.teacher_comment = comment
        document.save()
        
        return redirect('documents:teacher_documents')
    
    return redirect('documents:teacher_documents')


@login_required
def student_vault_by_teacher_view(request, student_id):
    """O'qituvchi o'quvchining javonini ko'radi (faqat ruxsat berilgan hujjatlar)"""
    if not request.user.is_teacher:
        return redirect('dashboard')
    
    student = get_object_or_404(CustomUser, id=student_id, role='student')
    
    vault_documents = StudentDocument.objects.filter(
        student=student,
        status=StudentDocument.STATUS_DRAFT,
        allow_teacher_view_draft=True
    ).select_related('template')
    
    all_vault = StudentDocument.objects.filter(
        student=student,
        status=StudentDocument.STATUS_DRAFT
    ).select_related('template')
    
    return render(request, 'teacher/student_vault.html', {
        'student': student,
        'vault_documents': vault_documents,
        'all_vault_count': all_vault.count()
    })


@login_required
def student_toggle_teacher_view(request, pk):
    """O'quvchi o'qituvchiga javonni ko'rishga ruxsat beradi"""
    if not request.user.is_student:
        return redirect('dashboard')
    
    document = get_object_or_404(StudentDocument, pk=pk, student=request.user)
    
    if request.method == 'POST':
        document.allow_teacher_view_draft = request.POST.get('allow') == 'on'
        document.save()
    
    return redirect('documents:student_vault')