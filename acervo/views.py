from django.shortcuts import render, get_object_or_404 
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Livro
from django.contrib.auth.decorators import login_required
from .models import Livro, Emprestimo

def index(request):
    termo_busca = request.GET.get('q')

    if termo_busca:
        # Se há um termo de busca, filtra os livros
        livros = Livro.objects.filter(titulo__icontains=termo_busca) | Livro.objects.filter(autor__icontains=termo_busca)
    else:
        # Se não há busca, lista todos os livros, ordenados por título
        livros = Livro.objects.all().order_by('titulo')

    # O contexto sempre terá a variável 'livros', mesmo que a busca não retorne nada
    contexto = {
        'livros': livros,
        'termo_busca': termo_busca or '' # Garante que termo_busca nunca seja None no template
    }
    
    return render(request, 'acervo/index.html', contexto)

def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    
    # Verifica se existe um empréstimo ativo (não devolvido) para este livro
    emprestimo_ativo = Emprestimo.objects.filter(livro=livro, devolvido=False).first()
    
    contexto = {
        'livro': livro,
        'emprestimo_ativo': emprestimo_ativo
    }
    return render(request, 'acervo/detalhe_livro.html', contexto)

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Cria o usuário no banco de dados
            return redirect('login') # Redireciona para a página de login
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/cadastro.html', {'form': form})

@login_required
def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    
    # Verifica novamente se o livro já não foi emprestado enquanto o usuário olhava a página
    if Emprestimo.objects.filter(livro=livro, devolvido=False).exists():
        # Idealmente, aqui mostraríamos uma mensagem de erro. Por enquanto, redirecionamos.
        return redirect('detalhe_livro', livro_id=livro.id)

    # Cria o novo empréstimo
    Emprestimo.objects.create(livro=livro, usuario=request.user)
    
    return redirect('detalhe_livro', livro_id=livro.id)

@login_required
def meus_emprestimos(request):
    # Busca todos os empréstimos associados ao usuário logado
    # e ordena pelos mais recentes primeiro
    emprestimos = Emprestimo.objects.filter(usuario=request.user).order_by('-data_emprestimo')
    
    contexto = {
        'emprestimos': emprestimos
    }
    return render(request, 'acervo/meus_emprestimos.html', contexto)

@login_required
def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id, usuario=request.user)
    
    if request.method == 'POST':
        emprestimo.devolvido = True
        emprestimo.save()
        
    return redirect('meus_emprestimos')