from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Livro(models.Model):
    # Adicionamos 'verbose_name' para cada campo
    titulo = models.CharField(max_length=200, verbose_name="Título")
    autor = models.CharField(max_length=100, verbose_name="Autor")
    genero = models.CharField(max_length=50, verbose_name="Gênero", blank=True)
    ano_publicacao = models.IntegerField(verbose_name="Ano de Publicação")
    disponivel = models.BooleanField(default=True)
    capa_url = models.URLField(max_length=500, blank=True, null=True)
    ano_publicacao = models.IntegerField(blank=True, null=True)
    sinopse = models.TextField(blank=True, null=True)



    # Meta classe para dar um nome amigável ao modelo no plural e singular
    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"

    # Corrigido de _str_ para __str__ (dois underscores)
    def __str__(self):
        return self.titulo
    

class Emprestimo(models.Model):
    # Adicionamos 'verbose_name' aqui também
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    data_emprestimo = models.DateTimeField(default=timezone.now, verbose_name="Data de Empréstimo")
    data_devolucao = models.DateTimeField(default=timezone.now() + timedelta(days=7), verbose_name="Data de Devolução")
    devolvido = models.BooleanField(default=False, verbose_name="Devolvido")

    class Meta:
        verbose_name = "Empréstimo"
        verbose_name_plural = "Empréstimos"

    # Corrigido de _str_ para __str__
    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"