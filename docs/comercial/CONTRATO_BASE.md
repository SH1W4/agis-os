# Contrato de Prestação de Serviços de Software
## Agis Ops — Sistema Cognitivo de Gestão Operacional

---

**CONTRATO Nº:** AGIS-____/2026

**DATA:** ___/___/2026

---

## PARTES

**CONTRATADA:**
- **Nome/Razão Social:** _______________________________________________
- **CPF/CNPJ:** _______________________________________________
- **Endereço:** _______________________________________________
- **E-mail:** _______________________________________________
- **Representante:** _______________________________________________ (se PJ)

**CONTRATANTE:**
- **Razão Social:** _______________________________________________
- **CNPJ:** _______________________________________________
- **Endereço:** _______________________________________________
- **E-mail:** _______________________________________________
- **Representante Legal:** _______________________________________________
- **Cargo:** _______________________________________________

---

## 1. OBJETO DO CONTRATO

O presente instrumento tem por objeto a **prestação de serviços de implementação, configuração e suporte contínuo** do sistema **Agis Ops** — plataforma cognitiva de gestão operacional para logística de última milha — nas modalidades e condições descritas nas cláusulas seguintes.

---

## 2. ESCOPO DOS SERVIÇOS

### 2.1 Fase de Implantação (Piloto — 30 dias)

Incluídos no valor de implantação:

- [ ] Instalação e configuração do ambiente (Docker + PostgreSQL + Redis)
- [ ] Configuração das integrações com as plataformas selecionadas pelo CONTRATANTE
- [ ] Importação/migração de dados históricos (até 90 dias), se aplicável
- [ ] Treinamento da equipe operacional (até 8h, formato online ou presencial)
- [ ] Dashboard configurado para a operação do CONTRATANTE
- [ ] Entrega de documentação operacional em português
- [ ] Relatório comparativo ao final dos 30 dias

**Plataformas de integração incluídas (marcar as aplicáveis):**
- [ ] Shopee
- [ ] Shoppi
- [ ] Shein
- [ ] Outra: _______________________________________________

### 2.2 Serviço Contínuo (Assinatura Mensal)

Plano contratado: ☐ Start (R$ 2.500/mês) ☐ Operador (R$ 4.500/mês) ☐ Hub (R$ 8.000/mês)

Capacidade: _______________ pedidos/dia · Depósitos: _______________

**Incluído em todos os planos:**
- Sistema Agis Ops atualizado e funcional
- Motor cognitivo OCC (Representations, Beliefs, Intentions, Decisions)
- Dashboard operacional com monitoramento em tempo real
- API REST com documentação OpenAPI (Swagger)
- Backups automáticos diários com retenção de 30 dias
- Suporte técnico em português (ver Cláusula 4)
- Atualizações de software sem custo adicional

**Incluído no plano Operador e Hub:**
- Processamento multi-plataforma simultâneo
- Alertas automáticos de risco de SLA
- Exportação de relatórios (Excel, PDF, JSON)
- Suporte prioritário (ver Cláusula 4)

**Incluído apenas no plano Hub:**
- Depósitos ilimitados
- White-label (customização de marca sob consulta)
- Integração ERP dedicada (até 1 ERP incluso)
- Gerente de conta dedicado
- SLA personalizado (negociado em aditivo)

---

## 3. VALORES E FORMA DE PAGAMENTO

### 3.1 Implantação

| Descrição | Valor |
|:---|:---|
| Taxa única de implantação e piloto (30 dias) | R$ 8.000,00 |

**Forma de pagamento da implantação:**
- 50% na assinatura do contrato (R$ 4.000,00)
- 50% na entrega do sistema funcional (R$ 4.000,00)

### 3.2 Assinatura Mensal

| Descrição | Valor Mensal |
|:---|:---|
| Plano selecionado na Cláusula 2.2 | R$ _____________ |

**Forma de pagamento mensal:**
- Vencimento: todo dia ___ de cada mês
- Instrumento: ☐ PIX ☐ Boleto ☐ Transferência bancária
- Dados para pagamento serão informados na primeira cobrança

### 3.3 Reajuste

Os valores mensais serão reajustados anualmente pelo **IPCA** acumulado no período, com prévia notificação de 30 dias.

### 3.4 Atraso de Pagamento

O atraso no pagamento sujeitará o CONTRATANTE a:
- Multa de **2%** sobre o valor devido
- Juros de mora de **1%** ao mês (pro rata die)
- Suspensão do serviço após **15 dias** de atraso, sem prejuízo da cobrança

---

## 4. NÍVEL DE SERVIÇO (SLA)

### 4.1 Disponibilidade do Sistema

| Plano | Uptime Garantido | Janela de Manutenção |
|:---|:---|:---|
| Start | 99,5% ao mês | Domingos, 02h–06h |
| Operador | 99,5% ao mês | Domingos, 02h–06h |
| Hub | A negociar em aditivo | A negociar |

> Cálculo: Uptime = (Minutos disponíveis / Minutos totais do mês) × 100

### 4.2 Tempo de Resposta ao Suporte

| Criticidade | Descrição | Tempo de Primeira Resposta | Resolução |
|:---|:---|:---|:---|
| **P1 — Crítico** | Sistema indisponível em produção | 2 horas | 8 horas |
| **P2 — Alto** | Funcionalidade principal comprometida | 4 horas | 24 horas |
| **P3 — Médio** | Funcionalidade secundária com falha | 8 horas (úteis) | 72 horas |
| **P4 — Baixo** | Dúvidas, melhorias, ajustes | 1 dia útil | Próxima sprint |

> Plano Start: atendimento P1–P3 em horário comercial (09h–18h, seg–sex).
> Planos Operador e Hub: atendimento P1 24/7 via WhatsApp dedicado.

### 4.3 Penalidade por Descumprimento de SLA

Se o uptime mensal for inferior ao garantido, o CONTRATANTE terá direito a desconto proporcional na mensalidade seguinte, calculado como:

> Desconto = (Minutos de indisponibilidade não planejada / Minutos totais) × Valor mensal × 2

Excluem-se do cálculo: manutenções programadas, falhas de infraestrutura do CONTRATANTE, ataques externos (DDoS) e força maior.

---

## 5. PROPRIEDADE INTELECTUAL E DADOS

### 5.1 Propriedade do Software

O sistema Agis Ops, incluindo seu código-fonte, arquitetura, motor OCC e documentação técnica, é de propriedade exclusiva da CONTRATADA. Este contrato concede ao CONTRATANTE uma **licença de uso**, não exclusiva e intransferível, pelo período de vigência do contrato.

### 5.2 Propriedade dos Dados

Todos os dados operacionais inseridos no sistema pelo CONTRATANTE (pedidos, motoristas, clientes, rotas) são de **propriedade exclusiva do CONTRATANTE**.

A CONTRATADA compromete-se a:
- Não utilizar os dados do CONTRATANTE para qualquer finalidade que não a operação do sistema
- Não compartilhar dados com terceiros sem autorização expressa e por escrito
- Fornecer exportação completa dos dados em até 30 dias após solicitação formal
- Excluir permanentemente os dados em até 60 dias após o encerramento do contrato, mediante solicitação

### 5.3 Conformidade com LGPD

A CONTRATADA atua como **Operadora de Dados** nos termos da Lei 13.709/2018 (LGPD), processando dados exclusivamente conforme as instruções do CONTRATANTE, que é o **Controlador de Dados**. As partes firmarão Acordo de Processamento de Dados (DPA) como Anexo I deste contrato.

---

## 6. CONFIDENCIALIDADE

As partes comprometem-se a manter em sigilo todas as informações técnicas, comerciais, operacionais e estratégicas obtidas em razão deste contrato, durante a vigência e por **2 (dois) anos** após seu encerramento, sob pena de responsabilidade civil e criminal.

---

## 7. GARANTIA DE SATISFAÇÃO

### 7.1 Piloto com Garantia Total

Se ao final dos **30 dias de piloto** o sistema Agis Ops não demonstrar redução mensurável em pelo menos **uma** das métricas abaixo, em comparação ao sistema anterior:

- Tempo médio de recuperação de pedidos com ocorrência
- Taxa de reentregas por falha de rastreamento
- Horas de equipe gastas com ocorrências operacionais

A CONTRATADA devolverá **100% do valor de implantação pago**, sem custo para o CONTRATANTE, mediante solicitação formal em até 5 dias após o encerramento do piloto.

### 7.2 Demonstração da Métrica

A comparação será baseada em dados extraídos do próprio sistema Agis (que registra todas as métricas desde o primeiro dia) versus referência fornecida pelo CONTRATANTE dos 30 dias anteriores ao início do piloto.

---

## 8. OBRIGAÇÕES DAS PARTES

### 8.1 Obrigações da CONTRATADA

- Entregar o sistema funcional nos prazos acordados
- Prestar suporte nos termos da Cláusula 4
- Manter o sistema atualizado e seguro
- Notificar o CONTRATANTE sobre manutenções com mínimo de 48h de antecedência
- Realizar backups diários e garantir recuperação em até 4h em caso de falha
- Cumprir a LGPD no tratamento dos dados do CONTRATANTE

### 8.2 Obrigações do CONTRATANTE

- Fornecer acesso ao ambiente de infraestrutura necessário (ou contratar servidor indicado)
- Disponibilizar equipe para treinamento nos horários acordados
- Efetuar pagamentos nos vencimentos acordados
- Não compartilhar credenciais de acesso com terceiros não autorizados
- Notificar a CONTRATADA sobre incidentes de segurança que tome conhecimento
- Não realizar engenharia reversa, cópia ou redistribuição do sistema

---

## 9. VIGÊNCIA E RESCISÃO

### 9.1 Vigência

O contrato entra em vigor na data de assinatura e tem prazo mínimo de **12 (doze) meses**, renovando-se automaticamente por períodos iguais salvo notificação contrária.

### 9.2 Rescisão Sem Multa

Qualquer parte pode rescindir o contrato sem multa mediante notificação formal com **30 (trinta) dias** de antecedência, desde que todas as obrigações financeiras estejam quitadas.

### 9.3 Rescisão por Justa Causa

O contrato pode ser rescindido imediatamente por justa causa nas seguintes hipóteses:
- Inadimplemento por mais de 15 dias
- Violação de confidencialidade comprovada
- Uso do sistema para fins ilegais
- Descumprimento grave de qualquer cláusula, após notificação de 5 dias sem correção

### 9.4 Portabilidade de Dados pós-Rescisão

Após a rescisão, a CONTRATADA manterá os dados acessíveis por **30 dias** para exportação pelo CONTRATANTE, findo os quais os dados serão excluídos.

---

## 10. DISPOSIÇÕES GERAIS

### 10.1 Foro

As partes elegem o foro da Comarca de _______________, Estado de _______________, para dirimir quaisquer conflitos oriundos deste contrato.

### 10.2 Aditivos

Qualquer alteração neste contrato deverá ser formalizada por **Aditivo Contratual** assinado por ambas as partes.

### 10.3 Integralidade

Este contrato, seus anexos e eventuais aditivos constituem o acordo integral entre as partes, substituindo quaisquer entendimentos anteriores.

---

## 11. ASSINATURAS

Lido e acordado pelas partes, firmam o presente instrumento em 2 (duas) vias de igual teor.

**Local e Data:** _______________, ___ de ___________ de 2026.

---

**CONTRATADA:**

```
_____________________________________________
Nome: 
CPF/CNPJ: 
```

**CONTRATANTE:**

```
_____________________________________________
Nome: 
Cargo:
CPF/CNPJ: 
```

---

**TESTEMUNHAS:**

```
_________________________     _________________________
Nome:                         Nome:
CPF:                          CPF:
```

---

## ANEXO I — Acordo de Processamento de Dados (DPA)

*(A ser preenchido conforme exigência da LGPD — Art. 39)*

**Finalidade do tratamento:** Gestão operacional logística conforme descrito no objeto do contrato.

**Tipos de dados tratados:** Dados de endereço para entrega, nome do destinatário, informações de rastreamento de pedidos, dados de localização de motoristas.

**Prazo de retenção:** Durante a vigência do contrato + 60 dias para exportação pós-rescisão.

**Medidas de segurança:** Criptografia AES-256 em repouso, TLS 1.3 em trânsito, autenticação JWT, logs de auditoria, backups criptografados.

**Suboperadores:** Nenhum. Todos os dados processados na infraestrutura contratada pelo CONTRATANTE ou indicada pela CONTRATADA e aprovada pelo CONTRATANTE.

---

*Documento gerado em 2026 — Agis Ops · Versão 1.0*
*Este modelo não constitui assessoria jurídica. Recomenda-se revisão por advogado antes de uso.*
