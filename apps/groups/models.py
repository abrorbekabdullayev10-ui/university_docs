from django.db import models

class Direction(models.Model):
    """O'quv yo'nalishi (masalan: Kompyuter injiniring)"""
    name = models.CharField("Yo'nalish nomi", max_length=200)
    code = models.CharField("Qisqa kod", max_length=20, unique=True)

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Group(models.Model):
    """O'quvchilar guruhi (masalan: 204-22)"""
    direction = models.ForeignKey(
        Direction, 
        on_delete=models.CASCADE, 
        related_name='groups',
        verbose_name="Yo'nalish"
    )
    name = models.CharField("Guruh nomi", max_length=50)
    year = models.IntegerField("O'qish yili", default=2024)

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        ordering = ['-year', 'name']

    def __str__(self):
        return f"{self.name} — {self.direction.name}"