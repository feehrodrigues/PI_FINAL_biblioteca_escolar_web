from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Livro, Emprestimo

class BibliotecaTests(TestCase):
    def setUp(self):
        # 1. Criação de Usuários para os testes
        self.aluno = User.objects.create_user(username='joao_aluno', password='password123')
        self.admin = User.objects.create_superuser(username='admin_biblioteca', password='password123')

        # 2. Criação de um Livro com Código de Barras
        self.livro = Livro.objects.create(
            titulo="O Senhor dos Anéis",
            autor="J.R.R. Tolkien",
            genero="Fantasia",
            ano_publicacao=1954,
            codigo_isbn="9780007136599"
        )

    def test_livro_criado_com_sucesso(self):
        """Testa se o livro foi salvo no banco de dados corretamente"""
        self.assertEqual(Livro.objects.count(), 1)
        self.assertEqual(self.livro.titulo, "O Senhor dos Anéis")

    def test_acessibilidade_index_view(self):
        """Testa se a página inicial carrega com HTTP 200 (Sucesso) e exibe o livro"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "O Senhor dos Anéis")

    def test_api_consulta_livro_scanner(self):
        """Testa o fornecimento de API para o Scanner (Requisito API/IoT)"""
        response = self.client.get(reverse('api_consultar_livro', args=["9780007136599"]))
        self.assertEqual(response.status_code, 200)
        dados = response.json()
        self.assertTrue(dados['sucesso'])
        self.assertEqual(dados['titulo'], "O Senhor dos Anéis")

    def test_registrar_emprestimo(self):
        """Testa se o Aluno consegue solicitar um livro APÓS FAZER LOGIN"""
        # Robô faz login como Aluno
        self.client.login(username='joao_aluno', password='password123')
        
        response = self.client.post(reverse('registrar_emprestimo', args=[self.livro.id]))
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Emprestimo.objects.count(), 1)
        
        emprestimo = Emprestimo.objects.first()
        self.assertFalse(emprestimo.aprovado) # Inicia como Aguardando Aprovação

    def test_aprovar_emprestimo(self):
        """Testa se APENAS o Admin consegue aprovar o empréstimo"""
        emprestimo = Emprestimo.objects.create(livro=self.livro, usuario=self.aluno, aprovado=False)
        
        # Robô faz login como Admin (Bibliotecário)
        self.client.login(username='admin_biblioteca', password='password123')
        self.client.post(reverse('aprovar_emprestimo', args=[emprestimo.id]))
        
        # Verifica no banco de dados se foi aprovado
        emprestimo.refresh_from_db()
        self.assertTrue(emprestimo.aprovado)

    def test_registrar_devolucao(self):
        """Testa se APENAS o Admin consegue registrar a devolução"""
        emprestimo = Emprestimo.objects.create(livro=self.livro, usuario=self.aluno, aprovado=True, devolvido=False)
        
        # Robô faz login como Admin (Bibliotecário)
        self.client.login(username='admin_biblioteca', password='password123')
        self.client.post(reverse('registrar_devolucao', args=[emprestimo.id]))
        
        # Atualiza e verifica se mudou para devolvido
        emprestimo.refresh_from_db()
        self.assertTrue(emprestimo.devolvido)