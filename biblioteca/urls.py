# ARQUIVO: biblioteca/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin

# Classe customizada para adicionar mensagem de sucesso no Login
class LoginViewComMensagem(SuccessMessageMixin, auth_views.LoginView):
    success_message = "Login efetuado com sucesso. Bem-vindo(a) de volta!"
    template_name = 'registration/login.html'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas de Autenticação
    path('login/', LoginViewComMensagem.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # Inclui TODAS as URLs do app 'acervo' (index, cadastro, emprestar, etc.)
    path('', include('acervo.urls')),
]