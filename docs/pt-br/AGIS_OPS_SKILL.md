# 🔧 Agis Ops Skill - Guia Operacional v3.0

**Versão:** 3.0.0-alpha  
**Data:** 2026-07-09  
**Público:** Equipe de Operações e DevOps  
**Status:** Ativo (Infraestrutura Distribuída Docker/Celery)

---

## 📋 Visão Geral

Este documento define as diretrizes, procedimentos e habilidades necessários para gerenciar o sistema **Agis v3.0**, caracterizado por uma arquitetura assíncrona orientada a eventos físicos (conceito OCC) com Docker (PostgreSQL, Redis) e Celery Workers.

---

## 🚀 Habilidades Essenciais

### **1. Gerenciamento de Serviços (Docker / API / Workers)**

#### **Iniciar Infraestrutura (Containers)**
```bash
# Subir PostgreSQL e Redis
docker-compose up -d

# Verificar status dos containers
docker-compose ps
```

#### **Iniciar API REST (Agis API)**
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Iniciar API FastAPI
python run_api.py
```

#### **Iniciar Celery Workers (Agis Workers)**
```bash
# Iniciar o processamento assíncrono de tarefas operacionais
python run_worker.py
```

#### **Verificar Status de Serviços**
```bash
# Health check da API
curl http://localhost:8000/health

# Ping no Redis
docker exec -it agis-redis redis-cli ping
```

---

### **2. Gerenciamento de Banco de Dados (PostgreSQL & Alembic)**

#### **Executar Migrações**
```bash
# Executa e atualiza o schema do Postgres para o estado mais recente
alembic upgrade head
```

#### **Gerar Nova Migration (Modificações no models.py)**
```bash
alembic revision --autogenerate -m "Descrição das alterações"
```

#### **Conectar ao Banco de Dados (PostgreSQL)**
```bash
docker exec -it agis-postgres psql -U agis -d agis
```

---

### **3. Gerenciamento de Logs Distribuídos**

#### **Logs do Servidor de Banco (Postgres) e Broker (Redis)**
```bash
docker-compose logs -f postgres
docker-compose logs -f redis
```

#### **Logs dos Processadores do Celery**
```bash
# Visualizar fila e logs do worker
Get-Content logs\worker.log -Wait
```

---

### **4. Segurança (JWT e Usuários no PostgreSQL)**

Com o JWT, a tabela `users` é dinâmica e armazenada no PostgreSQL (não mais localmente em arquivos JSON).

#### **Geração de Credenciais Admin**
Para redefinir ou inicializar o usuário administrador do sistema, execute:
```bash
python init_db.py
```

---

## 🔧 Procedimentos Operacionais

### **Procedimento: Deploy Atualização**

1. **Backup do Banco de Dados PostgreSQL**
   ```bash
   docker exec agis-postgres pg_dump -U agis -d agis > backups/pre_deploy.sql
   ```

2. **Puxar Código e Atualizar Dependências**
   ```bash
   git pull origin main
   pip install -r requirements.txt --upgrade
   ```

3. **Rodar Migrações do Banco**
   ```bash
   alembic upgrade head
   ```

4. **Reiniciar Containers e Serviços**
   ```bash
   docker-compose restart
   ```

---

## 🚨 Troubleshooting

### **Problema: Erro de chaves estrangeiras no ORM (Alchemy)**
* **Causa:** O relacionamento `Order.states` ou `OperationalState.order` está gerando junções ambíguas.
* **Solução:** Certifique-se de que os relacionamentos possuem `primaryjoin` e `foreign_keys` declarados explicitamente no arquivo [models.py](file:///c:/Users/Jo%C3%A3o/Desktop/PROJETOS/06_UTILITIES/LOGISTIC_SMART/src/database/models.py).

### **Problema: Celery não processa tarefas**
* **Causa:** Conexão com o Redis perdida ou worker inativo.
* **Solução:**
  1. Teste o redis: `docker exec agis-redis redis-cli ping`.
  2. Verifique se a variável `CELERY_BROKER_URL` no `.env` aponta para `redis://localhost:6379/0`.
  3. Reinicie o worker executando `python run_worker.py`.

---

**Última Atualização:** 2026-07-09  
**Responsável:** Equipe de Operações (Antigravity AI & João)  
**Próxima Revisão:** 2026-08-09
