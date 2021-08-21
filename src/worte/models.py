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
    
    substantiv = models.CharField(unique=True, max_length=250)
    artikel = models.CharField(max_length=1, choices=ARTIKEL, blank=True, null=True)
    plural = models.CharField(max_length=250, blank=True, null=True)
    stufe = models.ForeignKey(Stufe, on_delete=models.PROTECT, blank=True, null=True)
    beispiele = models.TextField(blank=True, null=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.get_artikel_display()} {self.substantiv}'
    
    def save(self, *args, **kwargs):
        self.substantiv = self.substantiv.capitalize()
        if self.plural is None:
            self.plural = self.substantiv
        self.plural = self.plural.capitalize()
        # if self.artikel is None:
        #     if preg_match_all('/()/', self.substantiv):
            
            
        
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
