from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Livro, Emprestimo

class BibliotecaTests(TestCase):
    def setUp(self):
        # 1. Criação de Usuários (Atendendo ao seu lembrete perfeitamente!)
        self.aluno = User.objects.create_user(username='joao_aluno', password='password123')
        self.admin = User.objects.create_superuser(username='admin_biblioteca', password='password123')

        # 2. Criação de um Livro com Código de Barras (IoT/Scanner)
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
        """Testa se um empréstimo é criado corretamente e associado a um usuário"""
        # Simulando o POST no botão 'Registrar Empréstimo'
        response = self.client.post(reverse('registrar_emprestimo', args=[self.livro.id]))
        
        # 302 significa redirecionamento de sucesso
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Emprestimo.objects.count(), 1)
        
        emprestimo = Emprestimo.objects.first()
        self.assertFalse(emprestimo.devolvido) # O livro ainda não foi devolvido
        self.assertEqual(emprestimo.livro.titulo, "O Senhor dos Anéis")

    def test_registrar_devolucao(self):
        """Testa se a devolução atualiza o status do empréstimo"""
        # Criamos o empréstimo primeiro
        emprestimo = Emprestimo.objects.create(livro=self.livro, usuario=self.admin)
        
        # Simulamos o clique no botão 'Registrar Devolução'
        response = self.client.post(reverse('registrar_devolucao', args=[emprestimo.id]))
        self.assertEqual(response.status_code, 302)
        
        # Atualiza a informação do banco de dados e verifica se mudou para devolvido
        emprestimo.refresh_from_db()
        self.assertTrue(emprestimo.devolvido)