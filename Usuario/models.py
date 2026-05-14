from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)
    email = models.CharField(max_length=255, null=False, blank=False)
    senha = models.CharField(max_length=255, null=False, blank=False)
    tipo_conta = models.IntegerField(max_length=1, null=False, blank=False)