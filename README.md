# Nome da Aplicação: Ruralinfo

O Ruralinfo é uma aplicação web desenvolvida para centralizar o fluxo de informações no Campus Dois Irmãos da UFRPE. O sistema funciona como um mural digital onde a administração pode gerenciar comunicados, avisos acadêmicos e informações institucionais, garantindo que o corpo discente tenha acesso rápido e seguro aos dados da universidade. Esta versão representa a migração completa da aplicação desktop (CustomTkinter + SQLite) para uma plataforma web moderna utilizando o framework Django.

---

## Ferramentas Utilizadas

| Ferramenta | Descrição |
| :---: | --- |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="25" height="25"> | **Python 3.11+** — Linguagem de programação principal |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" width="25" height="25"> | **Django 5.x** — Framework web principal (Arquitetura MTV) |

| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlite/sqlite-original.svg" width="25" height="25"> | **SQLite** — Banco de dados relacional (via ORM nativo do Django) |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg" width="25" height="25"> | **VSCode** — IDE de desenvolvimento principal |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" width="25" height="25"> | **Git** — Sistema de controle de versionamento distribuído |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg" width="25" height="25"> | **GitHub** — Hospedagem de repositório e cooperação remota |

---z

## VERSÃO 2VA

- **1 — Sistema de Autenticação Dual:** Um mesmo e-mail `@ufrpe.br` pode possuir uma conta **COMUM** e uma conta **ADMIN** independentes. O login exige a seleção explícita do tipo de conta.
- **2 — Validação Institucional:** Filtro obrigatório para e-mails do domínio `@ufrpe.br` nos formulários de cadastro e login.
- **3 — Segurança de Credenciais:** Senhas armazenadas com hashing PBKDF2-SHA256. Validação de força: mínimo 10 caracteres, letra maiúscula, número e caractere especial.
- **4 — Sistema de Convites para Admin:** Nenhuma conta ADMIN pode ser criada publicamente. O cadastro exige um código UUID gerado por um administrador existente.
- **5 — Mural Informativo com Categorias:** Feed público de avisos organizados por categoria (Aviso Geral, Evento, Acadêmico, Oportunidade, Extensão, Pesquisa, Manutenção, Urgente) com filtro interativo.
- **6 — CRUD Completo para Admin:** Administradores podem criar, editar, ocultar e deletar qualquer aviso do sistema. A função de **ocultar** mantém o registro no banco sem exibi-lo ao público.
- **7 — Rastreabilidade de Autoria:** Cada aviso registra o administrador que o criou via chave estrangeira, servindo como auditoria interna.
- **8 — Suporte a Imagens:** Avisos podem conter imagem com campo de texto alternativo obrigatório (acessibilidade).
- **9 — Acesso por Visitante:** O mural é acessível sem autenticação. A navbar adapta-se automaticamente exibindo opções de login/cadastro para visitantes e o perfil do usuário para contas autenticadas.
- **10 — Nome de Usuário Customizado (Nickname):** Interface embutida na tela de perfil para alteração do identificador do usuário com validação inline de unicidade, preparando a identidade visual para futuras salas de conversa.
- **11 — Exclusão Avançada de Conta:** Sistema destrutivo seguro com acionamento por janela popup modal nativa (JavaScript puro) que exige a digitação e validação criptográfica da senha atual do usuário antes da remoção definitiva do banco de dados.

* **1 — Sistema de Autenticação Dual:** Um mesmo e-mail `@ufrpe.br` pode possuir uma conta **COMUM** e uma conta **ADMIN** independentes. O login exige a seleção explícita do tipo de conta.
* **2 — Validação Institucional:** Filtro obrigatório para e-mails do domínio `@ufrpe.br` nos formulários de cadastro e login.
* **3 — Segurança de Credenciais:** Senhas armazenadas com hashing PBKDF2-SHA256. Validação de força: mínimo 10 caracteres, letra maiúscula, número e caractere especial.
* **4 — Sistema de Convites para Admin:** Nenhuma conta ADMIN pode ser criada publicamente. O cadastro exige um código UUID gerado por um administrador existente.
* **5 — Mural Informativo com Categorias:** Feed público de avisos organizados por categoria (Aviso Geral, Evento, Acadêmico, Oportunidade, Extensão, Pesquisa, Manutenção, Urgente) com filtro interativo.
* **6 — CRUD Completo para Admin:** Administradores podem criar, editar, ocultar e deletar qualquer aviso do sistema. A função de **ocultar** mantém o registro no banco sem exibi-lo ao público.
* **7 — Rastreabilidade de Autoria:** Cada aviso registra o administrador que o criou via chave estrangeira, servindo como auditoria interna.
* **8 — Suporte a Imagens:** Avisos podem conter imagem com campo de texto alternativo obrigatório (acessibilidade).
* **9 — Acesso por Visitante:** O mural é acessível sem autenticação. A navbar adapta-se automaticamente exibindo opções de login/cadastro para visitantes e o perfil do usuário para contas autenticadas.
* **10 — Nome de Usuário Customizado (Nickname):** Interface embutida na tela de perfil para alteração do identificador do usuário com validação inline de unicidade, preparando a identidade visual para futuras salas de conversa.
* **11 — Exclusão Avançada de Conta:** Sistema destrutivo seguro com acionamento por janela popup modal nativa (JavaScript puro) que exige a digitação e validação criptográfica da senha atual do usuário antes da remoção definitiva do banco de dados.

### Bibliotecas Utilizadas

| Biblioteca | Descrição |
| --- | --- |
| **Django** | Framework principal: ORM, autenticação, roteamento e templates |
| **Pillow** | Processamento de imagens para o `ImageField` do mural |
| **python-dotenv** | Isolamento de chaves secretas do Django e credenciais do banco através de arquivos `.env` |
| **django-widget-tweaks** | Aplicação de classes CSS diretamente nos campos de formulário nos templates |
| **Bootstrap 5** *(CDN)* | Componentes visuais responsivos e sistema de grid |
| **Bootstrap Icons** *(CDN)* | Ícones utilizados na interface |

---

## Instalação e Execução

### 1. Clone o repositório

```bash
git clone [https://github.com/DanielMoreiraFr/Ruralinfo.git](https://github.com/DanielMoreiraFr/Ruralinfo.git)
cd Ruralinfo

```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

```

### 3. Instale as dependências e configure as variáveis de ambiente

```bash
pip install -r requirements.txt

```

> **Nota:** Crie um arquivo chamado `.env` na raiz do projeto baseado no `.env.example` preenchendo sua `SECRET_KEY` e mudando a flag `DEBUG=True`.

### 4. Execute as migrations

### 4. Execute as migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations mural
python manage.py migrate

```

### 5. Crie o primeiro administrador

Abra o shell do Django:

```bash
python manage.py shell

```

Execute o script abaixo dentro do shell interativo:

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

Acesse em: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Estrutura do Projeto

```
ruralinfo/
├── manage.py
├── requirements.txt
├── .env                          # variáveis de ambiente configuradas localmente
├── db.sqlite3                    # gerado após migrate
├── media/                        # uploads de imagens dos avisos
│
├── ruralinfo/                    # pacote de configuração
│   ├── settings.py               # AUTH_USER_MODEL · MEDIA · MESSAGE_TAGS · dotenv
│   ├── urls.py                   # roteador principal
│   └── wsgi.py
│
├── static/                       # arquivos estáticos globais
│   └── css/
│       └── base.css              # design system, variáveis de cor, botões e modal
│
├── accounts/                     # app de autenticação e perfil
│   ├── models.py                 # Usuario (AbstractUser) · CodigoConvite
│   ├── forms.py                  # LoginForm · CadastroComumForm · CadastroAdminForm
│   ├── views.py                  # login · cadastro · perfil · deletar_conta
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
    │   ├── perfil.html           # alteração de nick e modal de exclusão
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

## VERSÃO 3VA (Planejamento)

### Funcionalidades Futuras

- **10 — Implementação da Rota do Circular:** Mapeamento visual dos trajetos realizados pelo transporte interno da UFRPE.
- **11 — Busca do Circular:** Consulta dos horários previstos de saída e chegada por ponto de parada.
- **12 — Review Técnico do Ônibus:** Área para feedback discente sobre as condições de transporte, com dados consolidados para melhorias institucionais.
- **13 — Review Ruralinfo + Sugestões:** Canal direto para feedback sobre a experiência do usuário com a plataforma web.
- **14 — Chat de Interação síncrono:** Canal de bate-papo em tempo real conectando a comunidade acadêmica através dos nicknames customizados gerenciados no perfil.

---

## VERSÃO 1VA (Histórico)

A primeira versão do Ruralinfo foi desenvolvida como uma aplicação **desktop** utilizando **CustomTkinter** e banco de dados **SQLite** gerenciado manualmente com `sqlite3` e `contextlib`.

### Funcionalidades da V1

* Sistema de autenticação dual com alternância dinâmica de modo (Login/Cadastro)
* Validação institucional de e-mails `@ufrpe.br`
* Validação rigorosa de senhas
* Mural informativo para visualização de avisos
* Persistência em SQLite com tratamento de transações e Context Managers

### Execução da V1

```bash
pip install customtkinter
python src/main.py
```

---

# 📋 Matriz de Requisitos & Cronograma de Desenvolvimento

| Feature / ID | Requisito / Fluxo Principal | Validação de Erros / Fluxos Alternativos | Status | Prioridade |
| :--- | :--- | :--- | :--- | :--- |
| **RF001** | **Tela Inicial:** Escolha entre cadastro / visitante / login / fechar | Notificação de dígito inválido fora do menu prescrito no cadastro. | Pronta | P1 - Altíssima |
| **RF002** | **Cadastro:** Seleção de conta (Admin ou Comum), Nome e E-mail | Validação de espaços, bloqueio de duplicidade e restrição ao domínio `@ufrpe.br`. Senha forte com min. 10 chars, maiúscula, número e char especial. | Pronta | P1 - Altíssima |
| **RF003** | **Login:** Inserção de e-mail institucional e senha | Validação de credenciais. Se for verificado como ADM, libera rotas exclusivas. | Pronta | P1 - Altíssima |
| **RF004** | **Tela do Mural:** Exibição do feed público de informações | Renderização adaptável com base no status da sessão do usuário. | Pronta | P1 - Altíssima |
| **RF005** | **CRUD do Mural:** Gerenciamento dos posts pelos administradores | Restrição de área. Usuário comum precisa estar logado para interagir. | Pronta | P2 - Alta |
| **RF006** | **Filtro de Categorias:** Separador do mural por tipo de evento | Separação lógica automatizada em nível de banco sem quebras. | Pronta | P2 - Alta |
| **RF007** | **Horários do Circular:** Quadro de horários do transporte interno | Tratamento de endereço inválido ou inexistente na busca. | Em des. | P3 - Regular |
| **RF008** | **Pesquisa por Local:** Localização de blocos e prédios do campus | Erro de local não catalogado no sistema. | A fazer | P1 - Altíssima |
| **RF009** | **Comentários por Local:** Espaço para debates sobre locais específicos | Bloqueio de spam e validação de autenticação ativa. | A fazer | P2 - Alta |
| **RF010** | **Informações do Local:** Exibição de dados da pesquisa | Fallback para dados ausentes ou indisponíveis temporariamente. | A fazer | P2 - Alta |
| **RF011** | **Hierarquia de Permissões:** Definições feitas pelo Super ADM | Bloqueio de elevação de privilégios maliciosa. | Pronta | P1 - Altíssima |
| **RF012** | **Painel do Super ADM:** Tela administrativa avançada | Auditoria de segurança de tokens gerados. | Pronta | P1 - Altíssima |
| **RF013** | **Feedback do Local:** Avaliações das instalações pelos discentes | Tratamento de duplicidade de notas pelo mesmo usuário. | A fazer | P3 - Regular |
| **RF014** | **Sugestão de Anúncios:** Envio de posts sugeridos por usuários comuns | Validação de campos obrigatórios antes do envio à fila. | A fazer | P2 - Alta |
| **RF015** | **Revisão de Sugestões:** Área do ADM para aprovar/reprovar posts | Redirecionamento correto pós-validação de aprovação. | A fazer | P2 - Alta |
| **RF016** | **Token por E-mail:** Envio de código verificador para ativação | Expiração de token e reenvio de código de segurança. | A fazer | P2 - Alta |
