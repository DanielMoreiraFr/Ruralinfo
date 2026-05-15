from django.db import models

# Create your models here.

class Mural(models.Model):
    mensagem = models.CharField(max_length=512, null=False, blank=False)
    img_url = models.CharField(max_length=512)
    alt = models.CharField(max_length=512)
    data = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)