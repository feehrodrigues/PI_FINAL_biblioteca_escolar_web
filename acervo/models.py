from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    ano_publicacao = models.IntegerField()

    def _str_(self):
        return self.titulo
    
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(default=timezone.now)
    data_devolucao = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    devolvido = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.usuario.username} - {self.livro.titulo}"
    
    

# Create your models here.
