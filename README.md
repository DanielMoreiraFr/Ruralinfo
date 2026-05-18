<p align="center">
    <strong>Nome da Aplicação:</strong> Ruralinfo<br>
    <strong>Integrantes:</strong> <a href="https://github.com/DanielMoreiraFr">Daniel Moreira</a>, <a href="https://github.com/kauefreitasR">Kaue Freitas</a><br>
    <strong>Professor:</strong> Cleyton Vanut<br>
    <strong>Disciplina:</strong> Projeto Interdisciplinar para Sistemas de Informação 1<br>
    <strong>Curso:</strong> Bacharelado em Sistemas de Informação<br>
    <strong>Unidade de Ensino:</strong> Universidade Federal Rural de Pernambuco (UFRPE)<br>
</p>

<p>
O Ruralinfo é uma aplicação web desenvolvida para centralizar o fluxo de informações no Campus Dois Irmãos da UFRPE.
O sistema funciona como um mural digital onde a administração pode gerenciar comunicados, avisos acadêmicos e informações institucionais,
garantindo que o corpo discente tenha acesso rápido e seguro aos dados da universidade.
Esta versão representa a migração completa da aplicação desktop (CustomTkinter + SQLite) para uma plataforma web moderna utilizando o framework Django.
</p>

---

## Ferramentas Utilizadas

| Ferramenta | Descrição |
|---|---|
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="20"> **Python 3.11+** | Linguagem de programação principal |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" width="20"> **Django 5.x** | Framework web principal (MTV) |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-original.svg" width="20"> **Bootstrap 5** | Framework CSS para o frontend responsivo |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlite/sqlite-original.svg" width="20"> **SQLite** | Banco de dados relacional (via ORM do Django) |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg" width="20"> **VSCode** | IDE de desenvolvimento |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" width="20"> **Git** | Versionamento de código |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg" width="20"> **GitHub** | Repositório e cooperação remota |

---

# VERSÃO 2VA

## Funcionalidades Implementadas

- **1 — Sistema de Autenticação Dual:** Um mesmo e-mail `@ufrpe.br` pode possuir uma conta **COMUM** e uma conta **ADMIN** independentes. O login exige a seleção explícita do tipo de conta.
- **2 — Validação Institucional:** Filtro obrigatório para e-mails do domínio `@ufrpe.br` nos formulários de cadastro e login.
- **3 — Segurança de Credenciais:** Senhas armazenadas com hashing PBKDF2-SHA256. Validação de força: mínimo 10 caracteres, letra maiúscula, número e caractere especial.
- **4 — Sistema de Convites para Admin:** Nenhuma conta ADMIN pode ser criada publicamente. O cadastro exige um código UUID gerado por um administrador existente.
- **5 — Mural Informativo com Categorias:** Feed público de avisos organizados por categoria (Aviso Geral, Evento, Acadêmico, Oportunidade, Extensão, Pesquisa, Manutenção, Urgente) com filtro interativo.
- **6 — CRUD Completo para Admin:** Administradores podem criar, editar, ocultar e deletar qualquer aviso do sistema. A função de **ocultar** mantém o registro no banco sem exibi-lo ao público.
- **7 — Rastreabilidade de Autoria:** Cada aviso registra o administrador que o criou via chave estrangeira, servindo como auditoria interna.
- **8 — Suporte a Imagens:** Avisos podem conter imagem com campo de texto alternativo obrigatório (acessibilidade).
- **9 — Acesso por Visitante:** O mural é acessível sem autenticação. A navbar adapta-se automaticamente exibindo opções de login/cadastro para visitantes e o perfil do usuário para contas autenticadas.

## Bibliotecas Utilizadas

| Biblioteca | Descrição |
|---|---|
| **Django** | Framework principal: ORM, autenticação, roteamento e templates |
| **Pillow** | Processamento de imagens para o `ImageField` do mural |
| **django-widget-tweaks** | Aplicação de classes CSS Bootstrap diretamente nos campos de formulário nos templates |
| **Bootstrap 5** *(CDN)* | Componentes visuais responsivos e sistema de grid |
| **Bootstrap Icons** *(CDN)* | Ícones utilizados na interface |

---

## Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/DanielMoreiraFr/Ruralinfo.git
cd Ruralinfo
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrations

> **Importante:** sempre gere a migration do `accounts` antes das demais, pois os outros apps dependem do model de usuário customizado.

```bash
python manage.py makemigrations accounts
python manage.py makemigrations mural
python manage.py migrate
```

### 5. Crie o primeiro administrador

```bash
python manage.py shell
```

```python
from accounts.models import Usuario

admin = Usuario(
    nome_completo='Admin UFRPE',
    email='admin@ufrpe.br',
    tipo_conta='ADMIN',
    is_superuser=True,
)
admin.set_password('SuaSenhaForte@2025!')
admin.save()
exit()
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

Acesse em: **http://127.0.0.1:8000/**

---

## Estrutura do Projeto

```
ruralinfo/
├── manage.py
├── requirements.txt
├── db.sqlite3                    # gerado após migrate
├── media/                        # uploads de imagens dos avisos
│
├── ruralinfo/                    # pacote de configuração
│   ├── settings.py               # AUTH_USER_MODEL · MEDIA · MESSAGE_TAGS
│   ├── urls.py                   # roteador principal
│   └── wsgi.py
│
├── accounts/                     # app de autenticação
│   ├── models.py                 # Usuario (AbstractUser) · CodigoConvite
│   ├── forms.py                  # LoginForm · CadastroComumForm · CadastroAdminForm
│   ├── views.py                  # login · cadastro · logout
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── mural/                        # app do feed de avisos
│   ├── models.py                 # Aviso (categoria · publicado · FK autor)
│   ├── forms.py                  # AvisoForm
│   ├── views.py                  # index · criar · editar · deletar · toggle
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
└── templates/
    ├── base.html                 # navbar · paleta UFRPE · mensagens flash
    ├── accounts/
    │   ├── login.html
    │   ├── cadastro.html
    │   ├── _campos_base.html     # partial: nome e email
    │   └── _campos_senha.html    # partial: senha + confirmar + indicador de força
    └── mural/
        ├── index.html            # feed público com filtro de categorias
        ├── form.html             # criar e editar aviso
        └── confirmar_delete.html
```

---

## Link para os Fluxogramas do Projeto

[📁 Google Drive — Diagramas e Fluxogramas](https://drive.google.com/drive/folders/1mM4qqK3J-SPdMHgQSI99EP3JTfQxVX9q?usp=drive_link)

---

# VERSÃO 3VA (Planejamento)

## Funcionalidades Futuras

- **10 — Implementação da Rota do Circular:** Mapeamento visual dos trajetos realizados pelo transporte interno da UFRPE.
- **11 — Busca do Circular:** Consulta dos horários previstos de saída e chegada por ponto de parada.
- **12 — Review Técnico do Ônibus:** Área para feedback discente sobre as condições de transporte, com dados consolidados para melhorias institucionais.
- **13 — Review Ruralinfo + Sugestões:** Canal direto para feedback sobre a experiência do usuário com a plataforma web.
- **14 — A definir:** Funcionalidade bônus baseada nas necessidades identificadas durante os testes da 2VA.

---

# VERSÃO 1VA (Histórico)

A primeira versão do Ruralinfo foi desenvolvida como uma aplicação **desktop** utilizando **CustomTkinter** e banco de dados **SQLite** gerenciado manualmente com `sqlite3` e `contextlib`.

## Funcionalidades da V1

- Sistema de autenticação dual com alternância dinâmica de modo (Login/Cadastro)
- Validação institucional de e-mails `@ufrpe.br`
- Validação rigorosa de senhas
- Mural informativo para visualização de avisos
- Persistência em SQLite com tratamento de transações e Context Managers

## Execução da V1

```bash
pip install customtkinter
python src/main.py
```