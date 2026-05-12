import json
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Livro, Emprestimo

def index(request):
    termo = request.GET.get('q')
    if termo:
        livros = Livro.objects.filter(titulo__icontains=termo) | Livro.objects.filter(autor__icontains=termo)
    else:
        livros = Livro.objects.all()
    return render(request, 'acervo/index.html', {'livros': livros, 'termo_busca': termo})

def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    emprestimo_ativo = Emprestimo.objects.filter(livro=livro, devolvido=False).first()
    
    contexto = {
        'livro': livro,
        'emprestimo_ativo': emprestimo_ativo
    }
    return render(request, 'acervo/detalhe_livro.html', contexto)

@login_required
def dashboard(request):
    """Dashboard Analítico Profundo para a Direção da Escola"""
    
    # 1. MÉTRICAS EXCELENTES (KPIs Históricos e Atuais)
    total_livros = Livro.objects.count()
    total_historico_emprestimos = Emprestimo.objects.count() # Tudo que já foi rodado na escola
    livros_devolvidos = Emprestimo.objects.filter(devolvido=True).count()
    
    emprestimos_ativos = Emprestimo.objects.filter(devolvido=False, aprovado=True).count()
    aguardando_aprovacao = Emprestimo.objects.filter(aprovado=False).count()

    # 2. GRÁFICO 1: Distribuição do Acervo por Gênero
    grafico_generos = Livro.objects.values('genero').annotate(total=Count('id')).order_by('-total')
    labels_generos = [item['genero'] for item in grafico_generos]
    dados_generos = [item['total'] for item in grafico_generos]

    # 3. GRÁFICO 2: Top 5 Livros Mais Requisitados
    grafico_emprestimos = Emprestimo.objects.values('livro__titulo').annotate(total=Count('id')).order_by('-total')[:5]
    labels_emprestimos = [item['livro__titulo'] for item in grafico_emprestimos]
    dados_emprestimos = [item['total'] for item in grafico_emprestimos]

    contexto = {
        'total_livros': total_livros,
        'total_historico': total_historico_emprestimos,
        'livros_devolvidos': livros_devolvidos,
        'emprestimos_ativos': emprestimos_ativos,
        'aguardando_aprovacao': aguardando_aprovacao,
        'labels_generos': json.dumps(labels_generos),
        'dados_generos': json.dumps(dados_generos),
        'labels_emprestimos': json.dumps(labels_emprestimos),
        'dados_emprestimos': json.dumps(dados_emprestimos),
    }
    return render(request, 'acervo/dashboard.html', contexto)

    """Dashboard Analítico para a Direção da Escola"""
    
    # 1. MÉTRICAS RÁPIDAS (KPIs)
    total_livros = Livro.objects.count()
    emprestimos_ativos = Emprestimo.objects.filter(devolvido=False, aprovado=True).count()
    aguardando_aprovacao = Emprestimo.objects.filter(aprovado=False).count()

    # 2. GRÁFICO 1: Distribuição do Acervo por Gênero
    grafico_generos = Livro.objects.values('genero').annotate(total=Count('id')).order_by('-total')
    labels_generos = [item['genero'] for item in grafico_generos]
    dados_generos = [item['total'] for item in grafico_generos]

    # 3. GRÁFICO 2: Top 5 Livros Mais Requisitados pelos Alunos
    grafico_emprestimos = Emprestimo.objects.values('livro__titulo').annotate(total=Count('id')).order_by('-total')[:5]
    labels_emprestimos = [item['livro__titulo'] for item in grafico_emprestimos]
    dados_emprestimos = [item['total'] for item in grafico_emprestimos]

    # Envia tudo para o HTML
    contexto = {
        'total_livros': total_livros,
        'emprestimos_ativos': emprestimos_ativos,
        'aguardando_aprovacao': aguardando_aprovacao,
        'labels_generos': json.dumps(labels_generos),
        'dados_generos': json.dumps(dados_generos),
        'labels_emprestimos': json.dumps(labels_emprestimos),
        'dados_emprestimos': json.dumps(dados_emprestimos),
    }
    return render(request, 'acervo/dashboard.html', contexto)
def api_consultar_livro(request, isbn):
    try:
        livro = Livro.objects.get(codigo_isbn=isbn)
        dados = {'sucesso': True, 'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor, 'genero': livro.genero}
        return JsonResponse(dados)
    except Livro.DoesNotExist:
        return JsonResponse({'sucesso': False, 'mensagem': 'Livro não encontrado no acervo.'}, status=404)

def scanner(request):
    return render(request, 'acervo/scanner.html')

def cadastro(request):
    """Tela de cadastro para novos alunos"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/cadastro.html', {'form': form})

@login_required
def registrar_emprestimo(request, livro_id):
    """O Aluno SOLICITA o empréstimo"""
    if request.method == 'POST':
        livro = get_object_or_404(Livro, pk=livro_id)
        Emprestimo.objects.create(livro=livro, usuario=request.user, aprovado=False)
    return redirect('detalhe_livro', livro_id=livro_id)

@login_required
def aprovar_emprestimo(request, emprestimo_id):
    """O Admin APROVA a retirada do livro"""
    if request.method == 'POST' and request.user.is_staff:
        emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)
        emprestimo.aprovado = True
        emprestimo.save()
    return redirect('detalhe_livro', livro_id=emprestimo.livro.id)

@login_required
def registrar_devolucao(request, emprestimo_id):
    """O Admin DEVOLVE o livro"""
    if request.method == 'POST' and request.user.is_staff:
        emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)
        emprestimo.devolvido = True
        emprestimo.save()
        return redirect('detalhe_livro', livro_id=emprestimo.livro.id)
    return redirect('index')

@login_required
def meus_emprestimos(request):
    """Aba de Histórico do Aluno (Meus Livros)"""
    historico = Emprestimo.objects.filter(usuario=request.user).order_by('-data_emprestimo')
    return render(request, 'acervo/meus_emprestimos.html', {'historico': historico})