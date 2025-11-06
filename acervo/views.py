# ARQUIVO: acervo/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Livro, Emprestimo

def index(request):
    termo_busca = request.GET.get('q', '')
    if termo_busca:
        livros = Livro.objects.filter(titulo__icontains=termo_busca) | Livro.objects.filter(autor__icontains=termo_busca)
    else:
        livros = Livro.objects.all().order_by('titulo')
    
    # --- NOVA LÓGICA PARA O TEMPLATE ---
    livros_emprestados_pelo_usuario_ids = []
    if request.user.is_authenticated:
        livros_emprestados_pelo_usuario_ids = Emprestimo.objects.filter(usuario=request.user).values_list('livro__id', flat=True)

    contexto = {
        'livros': livros, 
        'termo_busca': termo_busca,
        'livros_emprestados_ids': livros_emprestados_pelo_usuario_ids # Passa a lista de IDs para o template
    }
    return render(request, 'acervo/index.html', contexto)
    
    contexto = {'livros': livros, 'termo_busca': termo_busca}
    return render(request, 'acervo/index.html', contexto)

def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    return render(request, 'acervo/detalhe_livro.html', {'livro': livro})

@login_required
def meus_emprestimos(request):
    emprestimos = Emprestimo.objects.filter(usuario=request.user)
    return render(request, 'acervo/meus_emprestimos.html', {'emprestimos': emprestimos})

@login_required
def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    LIMITE_EMPRESTIMOS = 3

    # --- VERIFICAÇÕES NA ORDEM CORRETA E SEGURA ---

    # 1. (MAIS IMPORTANTE) O livro está fisicamente disponível na biblioteca?
    if not livro.disponivel:
        messages.error(request, 'Operação falhou: este livro já foi emprestado por outra pessoa.')
        return redirect('index')

    # 2. O usuário atual já está com este mesmo livro?
    usuario_ja_pegou = Emprestimo.objects.filter(usuario=request.user, livro=livro).exists()
    if usuario_ja_pegou:
        messages.warning(request, 'Você já está com este livro emprestado.')
        return redirect('index')

    # 3. O usuário atual atingiu seu limite pessoal de empréstimos?
    emprestimos_ativos = Emprestimo.objects.filter(usuario=request.user).count()
    if emprestimos_ativos >= LIMITE_EMPRESTIMOS:
        messages.warning(request, f'Você atingiu seu limite de {LIMITE_EMPRESTIMOS} livros emprestados.')
        return redirect('index')

    # --- Se todas as regras passarem, o empréstimo é realizado ---
    Emprestimo.objects.create(usuario=request.user, livro=livro)
    livro.disponivel = False  # AGORA o livro é marcado como indisponível
    livro.save()
    messages.success(request, f'Você pegou "{livro.titulo}" emprestado com sucesso!')
    return redirect('index')

@login_required
def devolver_livro(request, emprestimo_id):
    # Procura um empréstimo que pertença ao usuário logado para segurança
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id, usuario=request.user)
    
    livro_titulo = emprestimo.livro.titulo
    
    # Atualiza o status do livro para disponível
    emprestimo.livro.disponivel = True
    emprestimo.livro.save()
    
    # Remove o registro do empréstimo
    emprestimo.delete()
    
    # Envia a notificação de sucesso
    messages.success(request, f'Você devolveu "{livro_titulo}" com sucesso!')
    
    # Redireciona de volta para a lista de empréstimos
    return redirect('meus_emprestimos')

class CadastroView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/cadastro.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Bem-vindo(a), {self.object.username}! Cadastro realizado com sucesso.')
        return response