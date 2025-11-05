# ARQUIVO: acervo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rotas da aplicação
    path('', views.index, name='index'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('meus-emprestimos/', views.meus_emprestimos, name='meus_emprestimos'),
    
    # Rotas de Ações
    path('livro/<int:livro_id>/emprestar/', views.emprestar_livro, name='emprestar_livro'),
    path('emprestimo/<int:emprestimo_id>/devolver/', views.devolver_livro, name='devolver_livro'),

    # Rota de Cadastro
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
]