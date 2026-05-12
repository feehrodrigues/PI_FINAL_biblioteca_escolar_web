from django.contrib import admin
from django.urls import path, include
from acervo import views

urlpatterns = [
    # Rotas Padrão do Django
    path('admin/', admin.site.urls),
    path('contas/', include('django.contrib.auth.urls')),
    
    # Rota de Cadastro de Alunos
    path('cadastro/', views.cadastro, name='cadastro'),
    
    # Rotas do Acervo e Dashboard
    path('', views.index, name='index'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Rotas da API e Scanner (IoT)
    path('api/livro/consulta/<str:isbn>/', views.api_consultar_livro, name='api_consultar_livro'),
    path('scanner/', views.scanner, name='scanner'),

    # Rotas do Fluxo de Empréstimo
    path('livro/<int:livro_id>/solicitar/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('emprestimo/<int:emprestimo_id>/aprovar/', views.aprovar_emprestimo, name='aprovar_emprestimo'),
    path('emprestimo/<int:emprestimo_id>/devolver/', views.registrar_devolucao, name='registrar_devolucao'),
    
    # Rota do Histórico do Aluno (Esta era a que estava faltando!)
    path('meus-livros/', views.meus_emprestimos, name='meus_emprestimos'),
]