from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField('tytuł', max_length=69)
    description = models.TextField('opis', max_length=420)
    complete = models.BooleanField('status', default=False)
    created = models.DateTimeField('utworzono', auto_now_add=True)
    deadline = models.DateTimeField('termin')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="osoba")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', 'user_id', 'deadline']

