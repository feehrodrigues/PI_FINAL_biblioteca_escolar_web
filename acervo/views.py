import json
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Livro, Emprestimo

# View 1: Página Inicial (Sem alterações)
def index(request):
    termo = request.GET.get('q')
    if termo:
        livros = Livro.objects.filter(titulo__icontains=termo) | Livro.objects.filter(autor__icontains=termo)
    else:
        livros = Livro.objects.all()
    
    return render(request, 'acervo/index.html', {'livros': livros, 'termo_busca': termo})

# View 2: Página de Detalhes do Livro (MODIFICADA)
def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    
    # LÓGICA NOVA: Verifica se existe um empréstimo ativo para este livro
    # Um empréstimo ativo é aquele que ainda não foi marcado como 'devolvido'.
    emprestimo_ativo = Emprestimo.objects.filter(livro=livro, devolvido=False).first()
    
    contexto = {
        'livro': livro,
        'emprestimo_ativo': emprestimo_ativo
    }
    return render(request, 'acervo/detalhe_livro.html', contexto)

# View 3: Página do Dashboard (Sem alterações)
def dashboard(request):
    grafico_generos = Livro.objects.values('genero').annotate(total=Count('id')).order_by('-total')
    labels_generos = [item['genero'] for item in grafico_generos]
    dados_generos = [item['total'] for item in grafico_generos]

    grafico_emprestimos = Emprestimo.objects.values('livro__titulo').annotate(total=Count('id')).order_by('-total')[:5]
    labels_emprestimos = [item['livro__titulo'] for item in grafico_emprestimos]
    dados_emprestimos = [item['total'] for item in grafico_emprestimos]

    contexto = {
        'labels_generos': json.dumps(labels_generos),
        'dados_generos': json.dumps(dados_generos),
        'labels_emprestimos': json.dumps(labels_emprestimos),
        'dados_emprestimos': json.dumps(dados_emprestimos),
    }
    return render(request, 'acervo/dashboard.html', contexto)

# View 4: API do Scanner (Sem alterações)
def api_consultar_livro(request, isbn):
    try:
        livro = Livro.objects.get(codigo_isbn=isbn)
        dados = {'sucesso': True, 'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor, 'genero': livro.genero}
        return JsonResponse(dados)
    except Livro.DoesNotExist:
        return JsonResponse({'sucesso': False, 'mensagem': 'Livro não encontrado no acervo.'}, status=404)

# View 5: Página do Scanner (Sem alterações)
def scanner(request):
    return render(request, 'acervo/scanner.html')

# --- NOVAS VIEWS DE AÇÃO ---

# View 6: Registrar um Empréstimo
def registrar_emprestimo(request, livro_id):
    if request.method == 'POST':
        livro = get_object_or_404(Livro, pk=livro_id)
        # Simplificação: Em um sistema real, pegaríamos o usuário logado com 'request.user'.
        # Para este projeto, vamos pegar o primeiro superusuário cadastrado como exemplo.
        usuario_admin = User.objects.filter(is_superuser=True).first()

        # Cria um novo registro de empréstimo no banco de dados
        Emprestimo.objects.create(livro=livro, usuario=usuario_admin)
    
    # Redireciona de volta para a página de detalhes do livro
    return redirect('detalhe_livro', livro_id=livro_id)

# View 7: Registrar uma Devolução
def registrar_devolucao(request, emprestimo_id):
    if request.method == 'POST':
        emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)
        
        # Marca o empréstimo como devolvido
        emprestimo.devolvido = True
        emprestimo.save()
        
        # Pega o ID do livro para poder redirecionar de volta
        livro_id = emprestimo.livro.id
        return redirect('detalhe_livro', livro_id=livro_id)
    
    # Se não for POST, apenas redireciona
    return redirect('index')