# 🗺️ CodeMap Completo do Sistema - Agis v3.0

Este documento fornece um mapeamento detalhado da estrutura do repositório, descrevendo a responsabilidade de cada diretório e arquivo técnico do **Agis v3.0**. Ele serve como guia de navegação rápida para desenvolvedores.

---

## 📌 Visão Geral da Arquitetura

O sistema é construído sobre uma arquitetura modular distribuída de três camadas:
1. **Frontend**: Interface interativa em Streamlit que consome a API REST e gerencia dados analíticos legados.
2. **Backend (API REST)**: API assíncrona FastAPI protegida com autenticação JWT que gerencia o estado operacional do negócio.
3. **Processamento em Background (Workers)**: Filas de tarefas assíncronas em Celery (usando Redis como Broker) que executam tarefas pesadas como otimização de rotas e normalização de dados.

---

## 📂 Árvore de Diretórios e Responsabilidades

```
LOGISTIC_SMART/ (Futuro AGIS/)
├── app.py                          # Streamlit: Interface visual e análise legada
├── requirements.txt                # Dependências de produção (FastAPI, Streamlit, Celery, Postgres, Redis)
├── docker-compose.yml              # Configuração PostgreSQL 15 + Redis 7
├── alembic.ini                     # Configurações de conexão e logs do Alembic Migrations
├── run_api.py                      # Script de inicialização da API REST FastAPI (Agis API)
├── run_worker.py                   # Script de inicialização do Celery Worker (Agis Workers)
│
├── src/                            # Módulo Core da Aplicação
│   ├── api/                        # FastAPI REST API Layer (Agis REST Services)
│   │   ├── main.py                 # Ponto de entrada FastAPI e setup do middleware
│   │   ├── middleware/
│   │   │   └── jwt_auth.py         # Middleware de validação de escopo e Roles de JWT
│   │   └── routes/                 # Endpoints REST expostos
│   │       ├── auth.py             # Login e dados do usuário logado
│   │       ├── orders.py           # Gestão de Pedidos (criação, consulta, status)
│   │       ├── drivers.py          # Gestão de Motoristas (criação, geolocalização, status)
│   │       └── routes.py           # Monitoramento e criação de Rotas Operacionais
│   │
│   ├── auth/                       # Sistema Legado de Autenticação do Streamlit
│   │   └── authentication.py       # Gerenciador de Login seguro com bcrypt
│   │
│   ├── config/                     # Configurações Globais do Sistema
│   │   ├── settings.py             # Configurações Pydantic Settings (.env, caminhos, flags)
│   │   └── celery_config.py        # Configurações do Celery, limites e auto-discover de tasks
│   │
│   ├── database/                   # Camada de Persistência (PostgreSQL & ORM)
│   │   ├── models.py               # Models do SQLAlchemy (Orders, Drivers, OperationalStates, etc.)
│   │   └── session.py              # Gerenciador de conexão e SessionLocal com fallback SQLite
│   │
│   ├── operational_state/          # Operational State Engine (Core OCC - Agis Cognition)
│   │   ├── engine.py               # Motor cognitivo: Representations, Beliefs, Confidence Decay
│   │   └── events.py               # Sistema de Mensageria CloudEvents-compatible
│   │
│   ├── ingestion/                  # Módulos de entrada de dados de plataformas externas
│   │   ├── normalizer.py           # Normalizador estrutural de pedidos
│   │   └── connectors/             # Conectores de APIs de terceiros (Shoppi, manual, etc.)
│   │
│   ├── routing/                    # Motor de Roteamento e Atribuição
│   │   ├── optimizer.py            # Algoritmo Nearest Neighbor para caminhos mais curtos
│   │   └── assignment.py           # Atribuição autônoma de pedidos a motoristas baseada em proximidade
│   │
│   ├── tracking/                   # Módulo de Notificações e Monitoramento de SLAs
│   │   └── notifier.py             # Notificações assíncronas para clientes e motoristas
│   │
│   ├── reconciliation/             # Reconciliação e faturamento
│   │   └── calculator.py           # Calculadora de pagamentos baseada em rotas e taxas concluídas
│   │
│   └── utils/                      # Funções Utilitárias Gerais
│   │   ├── data_processor.py       # Manipulação de DataFrames com Pandas
│   │   ├── export_utils.py         # Exportação de relatórios em Excel, PDF, CSV
│   │   └── logger.py               # Sistema centralizado de logs estruturados (structlog)
│   │
│   └── ui/                         # Recursos de UI, assets e esquemas de cores
│
├── alembic/                        # Controle de Histórico de Migrations do Banco
│   ├── env.py                      # Arquivo de configuração de conexões e autogenerate do Alembic
│   ├── script.py.mako              # Template de script para geração de migrations
│   └── versions/                   # Scripts autogerados de transição de banco
│
├── workers/                        # Fila de tarefas distribuídas
│   ├── celery_app.py               # Inicializador da aplicação Celery
│   └── tasks/                      # Tasks assíncronas registradas no worker
│       ├── ingestion.py            # Normalização de cargas e processamento em lote
│       ├── routing.py              # Consolidação física e geração de rotas
│       └── notifications.py        # Envio de alertas de atraso e status
│
├── tests/                          # Suíte de Testes Automatizados (pytest)
│   ├── test_authentication.py      # Cobertura do fluxo de segurança do Streamlit
│   └── test_data_processor.py      # Validação lógica do DataProcessor do Pandas
│
└── docs/                           # Documentação e Governança do Sistema
    ├── pt-br/                      # Documentos em Português
    │   ├── AGIS_OPS_SKILL.md                           # Manual de operações de deploy e rotinas
    │   └── CHECKLIST_EAP_TASKMASH_OPERACIONAL.md        # Lista de marcos operacionais validados (EAP)
    │
    ├── AGIS_OCC_ARCHITECTURE.md                        # Documentação conceitual do State Engine (OCC)
    ├── AGIS_INTEGRATION_GUIDE.md                       # Manual de API, endpoints e payloads JWT
    ├── CORPORATE_GOVERNANCE_FRAMEWORK.md               # Diretrizes de propriedade intelectual (independente)
    └── ui-design/                                      # Pasta com visual guides, mockups e prompts
        ├── UI_UX_DESIGN_GUIDE.md                       # O Guia de UI/UX e prompts para o Stitch
        ├── screen_01_dashboard.png                     # Visual do Dashboard Principal
        └── screen_02_state_engine.png                  # Visual da tela de estados OCC do Agis
```

---

## 🛠️ Principais Arquivos e suas Funções

*   **`src/database/models.py`**: Define o esquema relacional completo do banco no PostgreSQL. Suas principais entidades são: `Order` (pedidos), `Driver` (motoristas), `OperationalState` (tabela de histórico cognitivo OCC) e `OperationalEvent` (eventos de telemetria baseados em CloudEvents).
*   **`src/operational_state/engine.py`**: O cérebro dinâmico. Contém o motor de gerenciamento de estado cognitivo que valida a confiabilidade do sinal de GPS dos motoristas e atualiza a intenção de rota de pedidos.
*   **`workers/tasks/routing.py`**: Executa a lógica de consolidação espacial de pedidos e otimização de rotas geográficas de maneira assíncrona, desonerando o servidor principal da API.
*   **`src/api/middleware/jwt_auth.py`**: Intercepta todas as requisições HTTPS e assegura que somente usuários autorizados com escopos corretos acessem endpoints sensíveis como despacho de rotas e criação de motoristas.
*   **`docs/ui-design/UI_UX_DESIGN_GUIDE.md`**: Guia que especifica os Design Tokens (cores, fontes), a arquitetura UX e contém os prompts estruturados para a montagem de layouts no Google Stitch.
