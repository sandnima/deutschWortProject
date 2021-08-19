from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from worte.models import Substantiv


def get_guest_user():
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # bio = models.TextField(max_length=160, blank=True, null=True)
    # avatar = models.ImageField(upload_to='avatars', default='avatars/avatar.png')
    substantiv_stimmt = models.ManyToManyField(Substantiv, through='StimmtHistory', related_name='stimmt_history')
    substantiv_falsch = models.ManyToManyField(Substantiv, through='FalschHistory', related_name='falsch_history')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}'


class StimmtHistory(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    wort = models.ForeignKey(Substantiv, on_delete=models.CASCADE)
    mal = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'stimmt histories'

    def __str__(self):
        return f'{self.user} {self.wort} ({self.mal})'


class FalschHistory(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    wort = models.ForeignKey(Substantiv, on_delete=models.CASCADE)
    mal = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'falsch histories'

    def __str__(self):
        return f'{self.wort} ({self.mal})'
