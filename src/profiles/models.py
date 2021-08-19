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
    substantiv_stimmt = models.ManyToManyField(Substantiv)
    substantiv_falsch = models.ManyToManyField(Substantiv)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}'
