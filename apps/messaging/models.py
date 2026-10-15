from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages',
        verbose_name="Yuboruvchi"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_messages',
        verbose_name="Qabul qiluvchi"
    )
    subject = models.CharField("Mavzu", max_length=200)
    content = models.TextField("Xabar matni")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField("O'qilgan", default=False)

    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.subject})"