# 📚 Biblioteca Inteligente com IoT: Transformação Digital Escolar

Projeto Integrador desenvolvido para o curso de Tecnologia da UNIVESP. O objetivo é modernizar a gestão do acervo da EMEF Gianfrancesco Guarnieri, promovendo acessibilidade, eficiência e integração tecnológica.

## 🎯 Requisitos Atendidos

Este projeto foi construído seguindo rigorosamente os requisitos acadêmicos estipulados:

- **Framework Web & Linguagem:** Desenvolvido em **Python** utilizando o framework **Django**.
- **Banco de Dados:** Uso de banco de dados relacional (**SQLite**), modelando Livros, Usuários e Empréstimos.
- **Nuvem (Cloud):** Aplicação conteinerizada e hospedada na plataforma **Render**, acessível publicamente.
- **Controle de Versão:** Versionamento de código feito com **Git** e hospedado no **GitHub**.
- **Scripts Web (JavaScript):** Utilização avançada de JS Vanilla e bibliotecas de terceiros no frontend para interatividade em tempo real.
- **Acessibilidade:** 
  - 🌓 Sistema de Alto Contraste persistente (salvo em *LocalStorage*).
  - 🔊 Leitura de tela nativa implementada via `window.speechSynthesis` da Web Speech API.
- **Integração Contínua (CI) e Testes:** Workflow configurado no **GitHub Actions** (`django.yml`) que executa testes automatizados (implementados no `tests.py`) a cada novo *push* ou *pull request*.
- **Fornecimento de API & IoT:** Scanner de código de barras utilizando a câmera do dispositivo (simulando sensor IoT via *QuaggaJS*), que consome uma API RESTful criada no Django (`/api/livro/consulta/<isbn>/`) para localizar livros físicos instantaneamente.
- **Análises de Dados:** *Dashboard* analítico interativo construído com **Chart.js** e consultas avançadas no banco de dados (usando `Count` e `annotate` do Django ORM) para exibir estatísticas do acervo.

## 🚀 Como rodar o projeto localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/CaioRocha23/biblioteca_escolar_web.git