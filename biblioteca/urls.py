from django.contrib import admin
from django.urls import path
from acervo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/livro/consulta/<str:isbn>/', views.api_consultar_livro, name='api_consultar_livro'),
    path('scanner/', views.scanner, name='scanner'),

    # --- NOVAS ROTAS DE AÇÃO ---
    path('livro/<int:livro_id>/emprestar/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('emprestimo/<int:emprestimo_id>/devolver/', views.registrar_devolucao, name='registrar_devolucao'),
]