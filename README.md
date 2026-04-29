# Ruralinfo

## Objetivo
O Ruralinfo é uma aplicação desktop desenvolvida para centralizar e gerenciar informações pertinentes ao Campus Dois Irmãos da Universidade Federal Rural de Pernambuco (UFRPE). O sistema atua como um mural informativo digital, permitindo a comunicação eficiente entre a administração e o corpo discente sobre horários de transporte, avisos de departamentos e comunicados gerais.

## Funcionalidades
* **Autenticação de Usuários**: Sistema de login e cadastro com validação obrigatória de e-mail institucional (@ufrpe.br).
* **Gestão de Níveis de Acesso**: Diferenciação de permissões entre usuários comuns, visitantes e administradores.
* **Mural Dinâmico**: Visualização de avisos em tempo real com interface otimizada para leitura.
* **Controle Administrativo (CRUD)**: Ferramentas para usuários com perfil de Administrador realizarem a criação, edição, ativação/desativação e exclusão de postagens no mural.
* **Persistência de Dados**: Armazenamento estruturado em banco de dados relacional com gerenciamento automatizado de conexões.

## Tecnologias Utilizadas
* **Linguagem**: Python 3.14.4.
* **Interface Gráfica**: CustomTkinter.
* **Banco de Dados**: SQLite3.
* **Gerenciamento de Contexto**: Utilização do módulo `contextlib` para manipulação segura do banco de dados.

## Estrutura de Diretórios
O projeto está organizado de forma modular para facilitar a manutenção e escalabilidade:

```text
Ruralinfo/
├── src/
│   ├── banco/              # Módulos de persistência e esquemas SQL
│   │   ├── banco_infos.py
│   │   ├── banco_usuarios.py
│   │   └── banco.db
│   ├── Interface/
│   │   └── entidades/      # Definição das telas e componentes da GUI
│   │       ├── infos.py
│   │       └── usuarios.py
│   ├── utils/              # Funções auxiliares e constantes
│   │   ├── texto.py
│   │   └── requirements.txt
│   └── main.py             # Ponto de entrada da aplicação
├── venv/                   # Ambiente virtual
├── .gitignore
└── LICENSE
```

## Instalação e Configuração
Para configurar o ambiente de desenvolvimento e executar o sistema, siga os passos abaixo:

1. Certifique-se de possuir o Python instalado em seu sistema.
2. Instale as dependências necessárias através do gerenciador de pacotes:
   ```bash
   pip install -r src/utils/requirements.txt
   ```
3. A base de dados SQLite será inicializada automaticamente na primeira execução, criando as tabelas `contas_usuarios` e `infos` caso não existam.

## Execução
Para iniciar o sistema, execute o arquivo principal a partir da raiz do projeto:

```bash
python src/main.py
```

## Notas de Implementação
* **Segurança**: O sistema implementa verificações de segurança no lado do cliente para garantir que as senhas atendam aos requisitos mínimos de complexidade e que os e-mails pertençam ao domínio institucional.
* **Integridade de Dados**: As operações de banco de dados utilizam o decorador `@contextmanager`, garantindo que transações sejam finalizadas corretamente com `commit` ou revertidas com `rollback` em caso de exceções.

## Desenvolvedor
Projeto desenvolvido por Daniel, acadêmico da Universidade Federal Rural de Pernambuco (UFRPE).