from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Max
from .models import Message
from apps.accounts.models import CustomUser


@login_required
def chat_list_view(request):
    """Foydalanuvchining barcha suhbatlari ro'yxati"""
    user = request.user
    
    # Foydalanuvchi yuborgan yoki qabul qilgan xabarlardan suhbatlarni olish
    sent = Message.objects.filter(sender=user).values('receiver').annotate(last_time=Max('timestamp'))
    received = Message.objects.filter(receiver=user).values('sender').annotate(last_time=Max('timestamp'))
    
    # Barcha suhbatdagi odamlar
    chat_users_ids = set()
    for s in sent:
        chat_users_ids.add(s['receiver'])
    for r in received:
        chat_users_ids.add(r['sender'])
    
    chat_users = CustomUser.objects.filter(id__in=chat_users_ids).order_by('full_name')
    
    # Har bir suhbat uchun oxirgi xabar va o'qilmaganlar soni
    chats = []
    for chat_user in chat_users:
        last_message = Message.objects.filter(
            Q(sender=user, receiver=chat_user) | Q(sender=chat_user, receiver=user)
        ).order_by('-timestamp').first()
        
        unread_count = Message.objects.filter(
            sender=chat_user, receiver=user, is_read=False
        ).count()
        
        chats.append({
            'user': chat_user,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    return render(request, 'messaging/chat_list.html', {'chats': chats})


@login_required
def chat_view(request, user_id):
    """Bitta suhbatni ko'rish (Telegram uslubida)"""
    other_user = get_object_or_404(CustomUser, id=user_id)
    current_user = request.user
    
    if other_user.id == current_user.id:
        return redirect('messaging:chat_list')
    
    # Xabarlarni olish
    messages_list = Message.objects.filter(
        Q(sender=current_user, receiver=other_user) | Q(sender=other_user, receiver=current_user)
    ).order_by('timestamp')
    
    # Qabul qilingan xabarlarni o'qilgan deb belgilash
    Message.objects.filter(
        sender=other_user, receiver=current_user, is_read=False
    ).update(is_read=True)
    
    # AJAX uchun JSON ma'lumot
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        messages_data = []
        for msg in messages_list:
            messages_data.append({
                'id': msg.id,
                'sender_id': msg.sender.id,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M'),
                'is_mine': msg.sender.id == current_user.id
            })
        return JsonResponse({'messages': messages_data})
    
    return render(request, 'messaging/chat.html', {
        'other_user': other_user,
        'messages': messages_list,
        'current_user': current_user
    })


@login_required
def send_message_view(request, user_id):
    """Xabar yuborish (AJAX)"""
    if request.method == 'POST':
        other_user = get_object_or_404(CustomUser, id=user_id)
        content = request.POST.get('content', '').strip()
        
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                subject='Chat',
                content=content
            )
            return JsonResponse({'status': 'success', 'content': content})
        
        return JsonResponse({'status': 'error', 'message': 'Xabar bo\'sh'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Noto\'g\'ri so\'rov'}, status=400)


@login_required
def compose_message_view(request, receiver_id=None):
    """Eski forma (orqaga moslik uchun)"""
    if receiver_id:
        return redirect('messaging:chat', user_id=receiver_id)
    return redirect('messaging:chat_list')


@login_required
def inbox_view(request):
    return redirect('messaging:chat_list')


@login_required
def message_detail_view(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if msg.receiver == request.user:
        return redirect('messaging:chat', user_id=msg.sender.id)
    elif msg.sender == request.user:
        return redirect('messaging:chat', user_id=msg.receiver.id)
    return redirect('messaging:chat_list')