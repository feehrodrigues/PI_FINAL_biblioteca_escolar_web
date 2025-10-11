from django.contrib import admin
from django.urls import path
from acervo import views  # importa as views do app acervo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # rota da página inicial
]
