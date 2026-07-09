# LogisticSmart v3.0 - Guia de Configuração e Instalação

Este guia fornece instruções passo a passo para configurar e executar o LogisticSmart v3.0 com PostgreSQL, Redis e Celery.

## Pré-requisitos

- Docker Desktop instalado e rodando
- Python 3.11+
- pip (gerenciador de pacotes Python)

## 1. Configuração do Ambiente

### 1.1 Instalar Dependências Python

```bash
pip install -r requirements.txt
```

### 1.2 Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` conforme necessário:

```env
# Database
DATABASE_URL=postgresql://logisticsmart:logisticsmart@localhost:5432/logisticsmart
DATABASE_ECHO=false

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# Streamlit
STREAMLIT_SERVER_PORT=8501

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 2. Configuração Docker (PostgreSQL + Redis)

### 2.1 Subir Containers Docker

```bash
docker-compose up -d
```

### 2.2 Verificar Status dos Containers

```bash
docker-compose ps
```

Você deve ver algo como:

```
NAME                      STATUS
logisticsmart-postgres    Up (healthy)
logisticsmart-redis       Up (healthy)
```

### 2.3 Verificar Logs (se necessário)

```bash
# PostgreSQL logs
docker-compose logs postgres

# Redis logs
docker-compose logs redis
```

## 3. Migrations do Banco de Dados

### 3.1 Criar Migration Inicial

```bash
alembic revision --autogenerate -m "Initial migration for v3.0"
```

### 3.2 Executar Migrations

```bash
alembic upgrade head
```

### 3.3 Verificar Status das Migrations

```bash
alembic current
```

### 3.4 (Opcional) Migrar Dados do SQLite v2.0

Se você tem dados do v2.0 em SQLite e deseja migrar:

```bash
python scripts/migrate_sqlite_to_postgres.py
```

## 4. Executar Aplicação

### 4.1 Iniciar API FastAPI

```bash
python run_api.py
```

A API estará disponível em: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

### 4.2 Iniciar Celery Worker (em outro terminal)

```bash
python run_worker.py
```

### 4.3 Iniciar Dashboard Streamlit (em outro terminal)

```bash
streamlit run app.py
```

O dashboard estará disponível em: http://localhost:8501

## 5. Verificar Funcionamento

### 5.1 Health Check da API

```bash
curl http://localhost:8000/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "service": "LogisticSmart API",
  "version": "3.0.0",
  "environment": "development"
}
```

### 5.2 Testar Autenticação JWT

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Resposta esperada:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "name": "Administrador",
    "role": "admin",
    "email": null
  }
}
```

### 5.3 Testar Endpoint Protegido

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <seu_token_jwt>"
```

## 6. Estrutura de Diretórios v3.0

```
LOGISTIC_SMART/
├── alembic/                    # Migrations do banco de dados
├── scripts/                    # Scripts utilitários
│   └── migrate_sqlite_to_postgres.py
├── src/
│   ├── api/                    # API FastAPI
│   │   ├── main.py
│   │   ├── middleware/         # JWT middleware
│   │   └── routes/             # API endpoints
│   ├── config/                 # Configurações
│   │   ├── settings.py
│   │   └── celery_config.py
│   ├── database/               # Database models e session
│   ├── operational_state/      # Motor de estado operacional (OCC)
│   └── utils/                  # Utilitários
├── workers/                    # Celery workers
│   ├── celery_app.py
│   └── tasks/                  # Tasks assíncronas
├── docker-compose.yml          # Docker Compose config
├── alembic.ini                 # Alembic config
├── .env                        # Variáveis de ambiente
├── run_api.py                  # Script para iniciar API
├── run_worker.py               # Script para iniciar Celery worker
└── app.py                      # Streamlit dashboard
```

## 7. Troubleshooting

### 7.1 Docker Desktop não está rodando

**Erro:** `unable to get image: error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/...`

**Solução:** Inicie o Docker Desktop antes de executar `docker-compose up -d`

### 7.2 PostgreSQL não aceita conexões

**Erro:** `connection refused` ou `could not connect to server`

**Solução:** Verifique se o container PostgreSQL está rodando:

```bash
docker-compose ps
docker-compose logs postgres
```

### 7.3 Redis não aceita conexões

**Erro:** `Error 111 connecting to localhost:6379`

**Solução:** Verifique se o container Redis está rodando:

```bash
docker-compose ps
docker-compose logs redis
```

### 7.4 Migrations falham

**Erro:** `Target database is not up to date`

**Solução:** Verifique o status atual das migrations:

```bash
alembic history
alembic current
```

Se necessário, recrie o banco de dados:

```bash
docker-compose down
docker-compose up -d
alembic downgrade base
alembic upgrade head
```

### 7.5 Celery worker não processa tasks

**Erro:** Tasks ficam pendentes no Redis

**Solução:** Verifique se o worker está conectado ao Redis:

```bash
# Verificar logs do worker
python run_worker.py

# Verificar conexão Redis
redis-cli ping
```

## 8. Modo Desenvolvimento (SQLite)

Para desenvolvimento sem Docker, você pode usar SQLite:

1. Não execute `docker-compose up -d`
2. Edite `.env` para usar SQLite:

```env
DATABASE_URL=sqlite:///./data/logistic_smart.db
CELERY_BROKER_URL=memory://
CELERY_RESULT_BACKEND=cache+memory://
```

3. Execute migrations (se necessário):

```bash
alembic upgrade head
```

4. Inicie a aplicação normalmente (sem Celery worker, pois não há Redis)

## 9. Próximos Passos

Após configurar o ambiente:

1. Criar módulos de negócio (ingestion, routing, tracking, reconciliation)
2. Implementar conectores de plataformas externas (Shoppi, Shopee, etc.)
3. Adicionar testes automatizados para novos componentes
4. Configurar CI/CD pipeline
5. Implementar dashboard v3.0 com novos recursos

## 10. Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
