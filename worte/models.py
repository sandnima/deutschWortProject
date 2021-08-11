from django.db import models
from django.conf import settings


class Stufe(models.Model):
    stufe = models.CharField(max_length=2, unique=True)
    
    def __str__(self):
        return self.stufe
    

class Substantiv(models.Model):
    DIE = 'F'
    DER = 'M'
    DAS = 'N'
    ARTIKEL = [
        (DIE, 'Die'),
        (DER, 'Der'),
        (DAS, 'Das'),
    ]

    PLURALS = [
        ('EN', '-en'),
        ('S', '-s'),
        ('E', '-e/⸚e'),
        ('ER', '-er/⸚er'),
        ('U', '-/⸚'),
    ]
    
    substantiv = models.CharField(unique=True, max_length=250)
    artikel = models.CharField(max_length=1, choices=ARTIKEL, default='N')
    plural = models.CharField(max_length=2, choices=PLURALS, default='U')
    stufe = models.ForeignKey(Stufe, on_delete=models.PROTECT, blank=True, null=True)
    beispiele = models.TextField(blank=True, null=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.get_artikel_display()} {self.substantiv}'
    
    def save(self, *args, **kwargs):
        self.substantiv = self.substantiv.capitalize()
        super().save(*args, **kwargs)


class Adjektiv(models.Model):
    adjektiv = models.CharField(unique=True, max_length=250)
    stufe = models.ForeignKey(Stufe, on_delete=models.PROTECT, blank=True, null=True)
    beispiele = models.TextField(blank=True, null=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.adjektiv
    
    def save(self, *args, **kwargs):
        self.adjektiv = self.adjektiv.capitalize()
        super().save(*args, **kwargs)
