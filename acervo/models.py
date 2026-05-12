from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    ano_publicacao = models.IntegerField()
    # Campo para conectar com o sensor da câmera (IoT)
    codigo_isbn = models.CharField(max_length=20, blank=True, null=True, unique=True, help_text="Código de barras ou ISBN do livro")

    def __str__(self):
        return self.titulo
    
class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(default=timezone.now)
    
    def devolucao_padrao():
        return timezone.now() + timedelta(days=7)
        
    data_devolucao = models.DateTimeField(default=devolucao_padrao)
    
    # STATUS DE CONTROLE
    aprovado = models.BooleanField(default=False)
    devolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"