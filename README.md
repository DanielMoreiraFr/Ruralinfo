<p align="center">
    <strong>Nome da Aplicação:</strong> Ruralinfo<br>
    <strong>Integrantes:</strong> <a href="https://github.com/DanielMoreiraFr">Daniel Moreira</a>, <a href="https://github.com/kauefreitasR">Kaue Freitas</a><br>
    <strong>Professor:</strong> Cleyton Vanut<br>
    <strong>Disciplina:</strong> Projeto Interdisciplinar para Sistemas de Informação I<br>
    <strong>Curso:</strong> Bacharelado em Sistemas de Informação<br>
    <strong>Unidade de Ensino:</strong> Universidade Federal Rural de Pernambuco (UFRPE)<br>
</p>

<p>
O Ruralinfo é uma aplicação web desenvolvida para centralizar o fluxo de informações no Campus Dois Irmãos da UFRPE.
O sistema funciona como um mural digital onde a administração pode gerenciar comunicados e avisos institucionais,
garantindo que o corpo discente tenha acesso rápido e seguro às informações da universidade.
O projeto também oferece um espaço para que a comunidade conheça os espaços do campus, consulte horários do
Circular Rural e contribua com sugestões de pauta para a administração.
</p>

---

## Ferramentas Utilizadas

| Ferramenta | Descrição |
|---|---|
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="20"> **Python 3.11+** | Linguagem de programação principal |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" width="20"> **Django 5.x / 6.x** | Framework web principal (MTV) |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sqlite/sqlite-original.svg" width="20"> **SQLite** | Banco de dados relacional via ORM do Django |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg" width="20"> **VSCode** | IDE de desenvolvimento |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" width="20"> **Git** | Versionamento de código |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg" width="20"> **GitHub** | Repositório e cooperação remota |

## Bibliotecas Utilizadas

| Biblioteca | Descrição |
|---|---|
| **Django** | Framework principal: ORM, autenticação, roteamento e templates |
| **Pillow** | Processamento de imagens para `ImageField` nos models de avisos e locais |
| **django-widget-tweaks** | Aplicação de classes CSS nos campos de formulário nos templates |
| **python-dotenv** | Leitura de variáveis de ambiente do arquivo `.env` |

---

# VERSÃO 1VA — Release 1.0

## Contexto

A primeira versão do Ruralinfo foi desenvolvida como uma aplicação **desktop** utilizando **CustomTkinter**
e banco de dados **SQLite** gerenciado manualmente com `sqlite3` e `contextlib`.
O foco foi estabelecer a base do sistema com autenticação e o mural informativo.

## Funcionalidades Implementadas

- **1 — Sistema de Autenticação Dual:** Tela unificada para Login e Cadastro com alternância dinâmica de modo.
- **2 — Validação Institucional:** Filtro obrigatório para e-mails do domínio `@ufrpe.br`.
- **3 — Segurança de Credenciais:** Validação de senhas com mínimo 10 caracteres, letra maiúscula, número e caractere especial.
- **4 — Mural Informativo:** Interface para visualização de avisos e comunicados acadêmicos.
- **5 — Acesso por Visitante:** Possibilidade de acessar o mural sem autenticação.
- **6 — Persistência em SQLite:** Gestão de dados de usuários e avisos com tratamento de transações e Context Managers.

## Execução da V1

```bash
pip install customtkinter
python src/main.py

```


# VERSÃO 2VA — Release 2.0

## Contexto

A segunda versão marca a **migração completa** da aplicação desktop para uma **plataforma web moderna**
utilizando o framework Django. A interface CustomTkinter foi substituída por templates HTML com CSS nativo
e identidade visual própria da UFRPE. O banco de dados manual foi substituído pelo ORM do Django,
e o sistema de autenticação foi completamente reconstruído com segurança real.

## Funcionalidades Implementadas

### 🔐 Autenticação e Segurança

* **1 — Dualidade de Contas:** Um mesmo e-mail `@ufrpe.br` pode ter uma conta COMUM e uma ADMIN independentes.
* **2 — Username Composto:** Login construído internamente como `email_TIPO` para suporte à dualidade.
* **3 — Hashing de Senha:** Senhas armazenadas com PBKDF2-SHA256 via `set_password()` do Django.
* **4 — Sistema de Convites UUID:** Cadastro de ADMIN exige código gerado por administrador existente.
* **5 — Verificação de E-mail:** Envio de código de confirmação por e-mail ao realizar cadastro.
* **6 — Proteção CSRF:** Todos os formulários POST protegidos com token CSRF.
* **7 — Transação Atômica:** Convite só é consumido se o usuário for criado com sucesso no banco.

### 📰 Mural de Avisos

* **8 — CRUD Completo:** Administradores criam, editam, ocultam e deletam qualquer aviso.
* **9 — Categorias:** Avisos organizados por Aviso Geral, Evento, Acadêmico, Oportunidade, Extensão, Pesquisa, Manutenção e Urgente.
* **10 — Ocultar sem Deletar:** Aviso pode ser retirado do ar sem ser removido do banco.
* **11 — Rastreabilidade:** Cada aviso registra o autor via chave estrangeira para auditoria.
* **12 — Imagem com Acessibilidade:** Avisos suportam imagem com campo `alt_texto` obrigatório.
* **13 — Acesso por Visitante:** Mural público acessível sem login para avisos urgentes.

### 👤 Perfil do Usuário

* **14 — Visualização de Perfil:** Tela com dados cadastrais do usuário logado.
* **15 — Alteração de Username:** Usuário pode personalizar seu identificador.
* **16 — Exclusão de Conta:** Remoção permanente com confirmação por senha via modal.

### 🎨 Interface e Experiência

* **17 — Identidade Visual UFRPE:** Paleta de cores `#112b38` / `#f4c430` aplicada em toda a interface.
* **18 — Indicador de Força de Senha:** Feedback visual em tempo real no cadastro.
* **19 — Toggle de Senha:** Botão para mostrar/ocultar campos de senha.
* **20 — Sidebar de Navegação:** Menu lateral com overlay acessível por botão hambúrguer.
* **21 — Flash Messages:** Notificações com auto-fechamento em 5 segundos.

---

# VERSÃO 3VA — Release 3.0

## Contexto

A terceira versão expande o Ruralinfo de um simples mural de avisos para uma **plataforma informativa completa do campus**. O foco é engajar a comunidade com conteúdo interativo — avaliações, comentários, galeria de fotos dos espaços do campus —, criar um canal direto entre alunos e administração por meio do sistema de sugestões de pauta, e introduzir um **mecanismo inteligente de rastreamento assíncrono para o transporte interno da UFRPE**.

## Funcionalidades Implementadas

### 🗺️ Áreas da Rural

* **22 — Listagem de Locais:** Grid de cards com imagem, descrição e média de avaliações de cada espaço do campus.
* **23 — Página de Detalhe:** Tela completa do local com galeria, avaliação e comentários.
* **24 — Galeria de Fotos:** Exibe linha de 5 thumbnails; se houver mais, a última mostra blur com contador `+N`.
* **25 — Lightbox:** Visualização ampliada das fotos com navegação por setas e teclado.
* **26 — Avaliação por Estrelas:** Notas de 0.5 a 5.0 com meias estrelas interativas, validação matemática rigorosa no backend.
* **27 — Reavaliação:** Usuário pode atualizar sua nota a qualquer momento.
* **28 — Comentários e Respostas:** Sistema com um nível de profundidade — comentário e resposta.
* **29 — Moderação:** Admin pode deletar qualquer comentário; autor pode deletar o próprio.
* **30 — CRUD de Locais pela Interface:** Admins do sistema criam, editam e removem locais sem precisar do painel superuser.
* **31 — Galeria Dinâmica:** Formulário permite adicionar fotos ilimitadas com botão "+ Adicionar foto".

### 💡 Sugestões de Pauta

* **32 — Envio de Sugestão:** Usuários logados sugerem pautas com texto e categoria.
* **33 — Painel de Pendentes:** Admin visualiza sugestões aguardando análise.
* **34 — Aceitar com Pré-preenchimento:** Ao aceitar, admin é redirecionado para criar aviso com texto e categoria já preenchidos.
* **35 — Negar e Arquivar:** Sugestão negada é arquivada com data para futura limpeza automática.
* **36 — Aba de Arquivadas:** Admin acessa histórico de sugestões negadas separadamente.

### 🚌 Sistema Ao Vivo do Circular Rural (Destaque Tecnológico)

* **37 — Tabela de Horários:** Consulta dos horários do Circular Rural com dois sentidos — Zootecnia (Início) e Zootecnia (Fim).
* **38 — Scroll Horizontal:** Tabela navegável com coluna de ponto fixada para facilitar a leitura em dispositivos móveis.
* **39 — API de Monitoramento: Criação de um endpoint que calcula dinamicamente o próximo horário de saída com base no fuso horário local (America/Recife).
* **40 — Componentização do Banner: Isolamento do painel dinâmico em um template parcial reaproveitável, integrado simultaneamente na tela de horários e no feed do Mural de Avisos.
* **41 — Atualização Assíncrona (Polling): Script em JavaScript que atualiza os dados do banner em segundo plano a cada 30 segundos e destaca automaticamente o horário ativo diretamente na tabela.
* **42 — Refinamento de Interface (UI): Novo indicador visual animado para o status "Ao Vivo" e estilização de alto contraste para facilitar a leitura rápida dos próximos ônibus.

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

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

```

### 3. Instale as dependências

```bash
pip install -r requirements.txt

```

### 4. Configure o `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-gerada-aqui
DEBUG=True
ALLOWED_HOSTS=

# --- CONFIGURAÇÃO DE E-MAIL ---
# Para desenvolvimento local (evita erros de autenticação SMTP/Brevo com IP dinâmico):
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Para ambiente de homologação/produção (usando Brevo):
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp-relay.brevo.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=seu-usuario-brevo
# EMAIL_HOST_PASSWORD=sua-senha-api-brevo
# DEFAULT_FROM_EMAIL=seu-email-remetente

```

Para gerar a `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

```

### 5. Execute as migrations

> ⚠️ Sempre gere a migration do `accounts` antes das demais.

```bash
python manage.py makemigrations accounts
python manage.py makemigrations mural
python manage.py makemigrations locais
python manage.py migrate

```

### 6. Crie o primeiro administrador e Código de Convite

Como o cadastro de novos administradores exige um código de convite baseado em UUID válido, use o shell do Django para criar o primeiro administrador do sistema e, opcionalmente, gerar convites iniciais:

```bash
python manage.py shell

```

```python
from accounts.models import Usuario, CodigoConvite

# 1. Criação do Administrador Raiz
admin = Usuario(
    nome_completo='Admin UFRPE',
    email='admin@ufrpe.br',
    tipo_conta='ADMIN',
    is_superuser=True,
)
admin.set_password('SuaSenhaForte@2025!')
admin.save()

# 2. (Opcional) Criar um token de convite para cadastrar outros administradores via interface
convite = CodigoConvite.objects.create(criado_por=admin)
print(f"Código de Convite gerado: {convite.codigo}")

exit()

```

### 7. Inicie o servidor

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
├── .env                          # variáveis sensíveis (não commitado)
├── .env.example                  # modelo público do .env
├── db.sqlite3                    # gerado após migrate
├── media/                        # uploads de imagens
│
├── ruralinfo/                    # pacote de configuração
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                     # autenticação e usuários
│   ├── models.py                 # Usuario · CodigoConvite
│   ├── forms.py                  # LoginForm · CadastroComumForm · CadastroAdminForm
│   ├── views.py                  # login · cadastro · logout · perfil
│   ├── urls.py
│   └── admin.py
│
├── mural/                        # avisos e sugestões
│   ├── models.py                 # Aviso · Sugestao
│   ├── forms.py                  # AvisoForm · SugestaoForm
│   ├── views.py                  # mural · CRUD avisos · sugestões
│   ├── urls.py
│   └── admin.py
│
├── locais/                       # áreas do campus
│   ├── models.py                 # LocalRural · ImagemLocal · Avaliacao · Comentario
│   ├── forms.py                  # LocalRuralForm · AvaliacaoForm · ComentarioForm
│   ├── views.py                  # lista · detalhe · CRUD · avaliação · comentários
│   ├── urls.py
│   └── admin.py
│
├── circular/                     # horários do circular 
│   ├── models.py                 
│   ├── views.py                  # Posicionamento do Circular · API
│   ├── urls.py
│   └── admin.py

├── static/
│   ├── css/
│   │   ├── base.css              # navbar · sidebar · botões · alertas
│   │   ├── accounts.css          # login e cadastro
│   │   ├── mural.css             # cards e grid do mural
│   │   ├── perfil.css            # perfil e modal de exclusão
│   │   ├── locais_lista.css      # grid de locais
│   │   ├── locais_detalhe.css    # galeria · lightbox · avaliação · comentários
│   │   ├── locais_form.css       # formulário de local
│   │   ├── horarios.css          # tabela estrutural estilo excel do circular
│   │   └── horarios_live.css     # estilos do banner, badge dinâmico e animações ao vivo
│   └── js/
│       ├── alerta.js             # auto-fechamento de mensagens
│       ├── navbar.js             # dropdown e menu mobile
│       ├── sidebar.js            # sidebar lateral
│       ├── olho_login.js         # toggle senha no login
│       ├── olho_cadastro.js      # toggle senha + força no cadastro
│       ├── perfil.js             # modal de exclusão de conta
│       ├── galeria.js            # thumbnails + lightbox
│       ├── galeria_form.js       # slots dinâmicos de foto
│       ├── estrelas.js           # avaliação interativa
│       ├── comentarios.js        # toggle de resposta inline
│       └── horarios_live.js      # motor assíncrono de busca e polling do circular ao vivo
│
└── templates/
    ├── base.html
    ├── accounts/
    │   ├── login.html
    │   ├── cadastro.html
    │   └── perfil.html
    ├── mural/
    │   ├── index.html
    │   ├── aviso_form.html
    │   ├── confirmar_delete.html
    │   ├── sugestao_form.html
    │   ├── sugestoes_pendentes.html
    │   └── sugestoes_arquivadas.html
    ├── locais/
    │   ├── lista.html
    │   ├── detalhe.html
    │   ├── form_local.html
    │   └── confirmar_delete_local.html
    └── circular/
        ├── horarios.html
        └── _banner_ao_vivo.html

```

---

## Link para os Fluxogramas do Projeto

[📁 Google Drive — Diagramas e Fluxogramas](https://drive.google.com/drive/folders/1mM4qqK3J-SPdMHgQSI99EP3JTfQxVX9q?usp=drive_link)
