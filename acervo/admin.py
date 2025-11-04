# ARQUIVO: acervo/admin.py

from django.contrib import admin
from .models import Livro, Emprestimo
from django.utils.html import format_html

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # Adicionamos a nova coluna 'emprestado_para'
    list_display = ('titulo', 'autor', 'disponivel', 'emprestado_para')
    list_filter = ('disponivel', 'autor')
    search_fields = ('titulo', 'autor')
    actions = ['marcar_como_disponivel', 'marcar_como_indisponivel']

    # --- NOVA FUNÇÃO DE AUDITORIA ---
    @admin.display(description='Emprestado Para')
    def emprestado_para(self, obj):
        if not obj.disponivel:
            emprestimo = Emprestimo.objects.filter(livro=obj).first()
            if emprestimo:
                return emprestimo.usuario.username
        return format_html('<span style="color: #999;">--</span>') # Retorna um traço cinza se estiver disponível
    
    # --- AÇÕES EXISTENTES ---
    @admin.action(description='Marcar selecionados como Disponível')
    def marcar_como_disponivel(self, request, queryset):
        # Ação inteligente: também apaga o registro de empréstimo associado
        for livro in queryset:
            Emprestimo.objects.filter(livro=livro).delete()
            livro.disponivel = True
            livro.save()

    @admin.action(description='Marcar selecionados como Indisponível (Sem Dono)')
    def marcar_como_indisponivel(self, request, queryset):
        queryset.update(disponivel=False)
        # Nota: Esta ação apenas marca como indisponível, mas não cria um empréstimo.
        # Útil para marcar livros como "em manutenção", etc.

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'data_emprestimo')
    list_filter = ('usuario', 'data_emprestimo')
    search_fields = ('livro__titulo', 'usuario__username')
    autocomplete_fields = ['livro', 'usuario']