from django.contrib import admin
from .models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'genero', 'ano_publicacao')  # colunas mostradas na lista
    list_filter = ('genero', 'ano_publicacao')  # filtros na barra lateral
    search_fields = ('titulo', 'autor')  # campo de busca no topo

# Register your models here.
