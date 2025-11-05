# ARQUIVO: acervo/admin.py

import requests
from django.contrib import admin
from .models import Livro, Emprestimo
from django.utils.html import format_html

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'disponivel', 'emprestado_para')
    list_filter = ('disponivel', 'autor')
    search_fields = ('titulo', 'autor')
    actions = ['marcar_como_disponivel', 'marcar_como_indisponivel']

    fieldsets = (
        ('Informações Principais', {
            'fields': ('titulo', 'autor', 'sinopse', 'genero')
        }),
        ('Status e Dados da API', {
            'fields': ('disponivel', 'ano_publicacao', 'capa_url'), # 'capa_url' agora está aqui
            'classes': ('collapse',),
        }),
    )
    
    # A CORREÇÃO ESTÁ AQUI: 'capa_url' foi removido da lista de somente leitura
    readonly_fields = ('ano_publicacao',)


    def save_model(self, request, obj, form, change):
        # ... (A função save_model continua exatamente a mesma, não precisa mudar nada nela) ...
        super().save_model(request, obj, form, change)

        if not obj.capa_url and obj.titulo and obj.autor:
            try:
                query = f"intitle:{obj.titulo}+inauthor:{obj.autor}"
                url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1&langRestrict=pt"
                
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                if data.get('totalItems', 0) > 0:
                    book_info = data['items'][0]['volumeInfo']
                    dados_para_salvar = []

                    image_links = book_info.get('imageLinks', {})
                    thumbnail = image_links.get('thumbnail') or image_links.get('smallThumbnail')
                    if thumbnail:
                        obj.capa_url = thumbnail
                        dados_para_salvar.append('capa_url')

                    published_date = book_info.get('publishedDate')
                    if published_date:
                        try:
                            obj.ano_publicacao = int(published_date.split('-')[0])
                            dados_para_salvar.append('ano_publicacao')
                        except (ValueError, IndexError):
                            pass

                    if not obj.sinopse and book_info.get('description'):
                        obj.sinopse = book_info.get('description')
                        dados_para_salvar.append('sinopse')
                    
                    if dados_para_salvar:
                        obj.save(update_fields=dados_para_salvar)
                    
                    self.message_user(request, "Livro salvo e dados da Google Books API foram importados com sucesso.")
                else:
                    self.message_user(request, "Nenhum resultado correspondente encontrado na Google Books API.", level='warning')
            except Exception as e:
                self.message_user(request, f"Ocorreu um erro inesperado ao buscar dados da API: {e}", level='error')
    
    # ... (O resto do arquivo, com as outras funções, continua o mesmo) ...
    @admin.display(description='Emprestado Para')
    def emprestado_para(self, obj):
        if not obj.disponivel:
            emprestimo = Emprestimo.objects.filter(livro=obj).first()
            if emprestimo:
                return emprestimo.usuario.username
        return format_html('<span style="color: #999;">--</span>')
    
    @admin.action(description='Marcar selecionados como Disponível')
    def marcar_como_disponivel(self, request, queryset):
        for livro in queryset:
            Emprestimo.objects.filter(livro=livro).delete()
            livro.disponivel = True
            livro.save()

    @admin.action(description='Marcar selecionados como Indisponível (Sem Dono)')
    def marcar_como_indisponivel(self, request, queryset):
        queryset.update(disponivel=False)

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'usuario', 'data_emprestimo')
    list_filter = ('usuario', 'data_emprestimo')
    search_fields = ('livro__titulo', 'usuario__username')
    autocomplete_fields = ['livro', 'usuario']