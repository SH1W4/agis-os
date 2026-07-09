# Agis Ops 🧭

<div align="center">

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-v0.100+-green.svg)
![Celery](https://img.shields.io/badge/celery-v5.3+-orange.svg)
![Docker](https://img.shields.io/badge/docker-v24+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue.svg)
![Redis](https://img.shields.io/badge/redis-7-red.svg)
![Version](https://img.shields.io/badge/version-v3.0.0--alpha-blue.svg)

**Plataforma de Decisão Cognitiva Operacional e Orquestração Física**

*Gestão avançada de status de entrega baseada em OCC State Engine, APIs assíncronas JWT e processamento distribuído.*

[🇺🇸 English](./README.md) | [🇧🇷 Português](./docs/pt-br/README.md)

[📖 Documentation](./docs/AGIS_CODEMAP.md) | [🐛 Issues](https://github.com/SH1W4/agis-os/issues)

</div>

---

## ✨ Principais Características (v3.0.0)

🧠 **OCC State Engine**: Motor dinâmico baseado em estados cognitivos fluidos (*Representations, Knowledge, Beliefs, Intentions, Decisions*) para avaliar rotas, entregas e status de motoristas sem depender de flags estáticas no banco.

🔐 **FastAPI com JWT Auth**: API assíncrona robusta protegida por tokens JWT com controle granular baseado em Roles e escopos (*Admin, User, Visitor*).

⚡ **Arquitetura Distribuída**: Workers assíncronos em Celery utilizando Redis como broker de mensagens, desonerando o servidor de API de rotinas pesadas de geolocalização e roteirização.

🐳 **Infraestrutura em Containers**: Configuração Docker Compose com instâncias isoladas do PostgreSQL 15 e Redis 7.

🛣️ **Motor de Otimização**: Algoritmos eficientes para agrupamento de rotas (*Nearest Neighbor*) e atribuição dinâmica com base em geolocalização em tempo real.

📊 **Design System Premium**: Guia conceitual de UI/UX moderno projetado com Glassmorphism e paletas escuras otimizadas para centros de controle operacionais (COP).

---

## 🏗️ Estrutura do Projeto

Para uma navegação detalhada sobre a responsabilidade de cada diretório e arquivo, veja o [Agis CodeMap](./docs/AGIS_CODEMAP.md).

```
agis-os/
├── src/                            # Módulo Core da Aplicação
│   ├── api/                        # endpoints FastAPI, Rotas e JWT Middleware
│   ├── config/                     # Pydantic Settings e configurações globais
│   ├── database/                   # Modelos ORM SQLAlchemy e Conexões
│   └── operational_state/          # Motor cognitivo de transições OCC
├── workers/                        # Configuração do Celery e Tarefas Assíncronas
├── alembic/                        # Controle de Histórico de Migrações do Banco
├── docs/                           # Guias técnicos de arquitetura e UI/UX
└── docker-compose.yml              # PostgreSQL e Redis Orchestration
```

---

## 🚀 Como Iniciar

### 1. Pré-requisitos
Certifique-se de ter instalado em sua máquina:
- Python 3.10+
- Docker & Docker Compose

### 2. Clonar e Instalar Dependências
```bash
git clone https://github.com/SH1W4/agis-os.git
cd agis-os

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências do projeto
pip install -r requirements.txt
```

### 3. Iniciar Infraestrutura Local (Docker)
```bash
docker-compose up -d
```
Isso iniciará os containers do PostgreSQL 15 (`agis-postgres`) e Redis 7 (`agis-redis`).

### 4. Rodar Migrações do Banco
Execute as migrações com o Alembic para criar as tabelas estruturadas no PostgreSQL:
```bash
alembic upgrade head
```

### 5. Iniciar Serviços do Agis
Em terminais diferentes, ative o ambiente virtual e execute:

**Iniciar API FastAPI**:
```bash
python run_api.py
```
A API estará rodando em `http://localhost:8000`. Acesse `/docs` para ver o Swagger interativo.

**Iniciar Celery Workers**:
```bash
python run_worker.py
```

---

## 📚 Documentação Técnica

- 🧭 [**CodeMap do Repositório**](./docs/AGIS_CODEMAP.md)
- 🧠 [**Arquitetura Cognitiva (OCC)**](./docs/AGIS_OCC_ARCHITECTURE.md)
- 📖 [**Manual de Integração de API e JWT**](./docs/AGIS_INTEGRATION_GUIDE.md)
- 🔧 [**Guia de Operações e Deploy**](./docs/pt-br/AGIS_OPS_SKILL.md)
- 🎨 [**UI/UX Design Guide & Stitch Prompts**](./docs/ui-design/UI_UX_DESIGN_GUIDE.md)

---

## 🏆 Licença

Este projeto é licenciado sob a MIT License. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">

**[🏠 Homepage](https://github.com/SH1W4/agis-os) • [🐛 Issues](https://github.com/SH1W4/agis-os/issues)**

**Desenvolvido por SH1W4 | Versão 3.0.0-alpha**

</div>
