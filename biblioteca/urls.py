from django.contrib import admin
from django.urls import path, include 
from django.urls import path
from acervo import views  # importa as views do app acervo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # rota da página inicial
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('contas/', include('django.contrib.auth.urls')), 
    path('contas/cadastro/', views.cadastro, name='cadastro'),
    path('livro/<int:livro_id>/emprestar/', views.emprestar_livro, name='emprestar_livro'),
    path('meus-emprestimos/', views.meus_emprestimos, name='meus_emprestimos'),
    path('emprestimo/<int:emprestimo_id>/devolver/', views.devolver_livro, name='devolver_livro'),

]
