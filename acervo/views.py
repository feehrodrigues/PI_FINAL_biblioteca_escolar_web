from django.shortcuts import render
from .models import Livro  # importa o modelo de livros

def index(request):
    termo = request.GET.get('q')  # pega o texto digitado no campo "q"
    livros = None
    if termo:
        livros = Livro.objects.filter(titulo__icontains=termo) | Livro.objects.filter(autor__icontains=termo)
    return render(request, 'acervo/index.html', {'livros': livros})