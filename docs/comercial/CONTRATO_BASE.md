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

### 5.1 Propriedade do Software e Know-How

O sistema Agis Ops, incluindo mas não se limitando a:
- Código-fonte, arquitetura e documentação técnica
- Motor cognitivo OCC (Operational Cognitive Computing) — Representations, Beliefs, Intentions e Decisions
- Modelos de dados, ontologias e vocabulário formal do domínio logístico
- Algoritmos de roteirização, otimização e atribuição de motoristas
- Heurísticas de cálculo de confiança e decaimento temporal de estados
- Métodos de normalização e consolidação de pedidos multi-plataforma
- Conceitos de "Estado Operacional", "Beliefs", "Intentions", "Representations" e "Decisions" aplicados ao domínio logístico

É de propriedade intelectual exclusiva da CONTRATADA, protegida pela Lei 9.610/98 (Direitos Autorais) e Lei 9.279/96 (Propriedade Industrial).

Este contrato concede ao CONTRATANTE uma **licença de uso**, não exclusiva, intransferível e revogável, pelo período de vigência do contrato.

### 5.1.1 Vedação Expressa

É expressamente vedado ao CONTRATANTE:

a) Realizar engenharia reversa, descompilação ou extração de algoritmos do sistema;
b) Documentar, replicar ou implementar conceitos, métodos ou heurísticas observadas durante o uso do sistema;
c) Utilizar o conhecimento obtido através do sistema para desenvolver soluções concorrentes ou similares, diretamente ou através de terceiros;
d) Compartilhar credenciais de acesso com terceiros não autorizados;
e) Permitir que concorrentes do CONTRATANTE tenham acesso ao sistema.

A violação desta cláusula sujeitará o CONTRATANTE ao pagamento de multa de **R$ 500.000,00 (quinhentos mil reais)**, sem prejuízo de perdas e danos adicionais e medidas judiciais cabíveis.

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

### 7.1 Estabelecimento de Baseline

Antes do início do piloto de 30 dias, o CONTRATANTE deverá fornecer à CONTRATADA os seguintes dados dos **30 dias anteriores**:

- [ ] Volume médio diário de pedidos
- [ ] Taxa de reentregas por falha de rastreamento (%)
- [ ] Tempo médio de resolução de ocorrências (horas)
- [ ] Horas/dia gastas pela equipe com ocorrências
- [ ] Taxa de devoluções/cancelamentos (%)

Caso o CONTRATANTE não possua esses dados, será utilizado o período de **7 dias imediatamente anteriores** ao início do piloto como baseline, medido manualmente pela equipe do CONTRATANTE com validação da CONTRATADA.

### 7.2 Critério de Sucesso

O piloto será considerado bem-sucedido se, ao final dos 30 dias, houver melhoria em pelo menos **UMA** das métricas abaixo:

| Métrica | Melhoria Mínima Requerida |
|:---|:---|
| Tempo de resolução de ocorrências | ≥ 20% de redução |
| Taxa de reentregas | ≥ 15% de redução |
| Horas de equipe com ocorrências | ≥ 25% de redução |

### 7.3 Medição

A medição será feita com base em:
- Dados extraídos do sistema Agis (fonte primária)
- Relatório comparativo gerado automaticamente ao final do piloto
- Validação conjunta em reunião de encerramento formal

### 7.4 Reembolso

Se o critério de sucesso não for atingido, o CONTRATANTE poderá solicitar reembolso integral do valor de implantação em até **5 (cinco) dias úteis** após a reunião de encerramento. O reembolso será processado em até **10 (dez) dias úteis**.

### 7.5 Conversão para Contrato Definitivo

Se o critério de sucesso for atingido, o contrato converte-se automaticamente em definitivo, iniciando a cobrança da mensalidade conforme Cláusula 3.2.

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

## 12. LIMITAÇÃO DE RESPONSABILIDADE

### 12.1 Teto de Responsabilidade

A responsabilidade total da CONTRATADA, em qualquer circunstância, limita-se ao valor de **3 (três) mensalidades** pagas pelo CONTRATANTE nos 3 (três) meses imediatamente anteriores ao evento danoso.

### 12.2 Exclusão de Danos Indiretos

Em nenhuma hipótese a CONTRATADA será responsável por:

a) Lucros cessantes, perda de receita ou perda de oportunidade de negócio;
b) Danos indiretos, incidentais ou consequenciais;
c) Perda de dados decorrente de falha de backup do CONTRATANTE;
d) Danos causados por uso indevido do sistema pelo CONTRATANTE;
e) Falhas decorrentes de infraestrutura de terceiros (internet, servidores de marketplace, APIs externas).

### 12.3 Exceções

As limitações acima **não se aplicam** em casos de:
a) Dolo comprovado da CONTRATADA;
b) Violação de confidencialidade;
c) Violação de direitos de propriedade intelectual.

---

## 13. NÃO-SOLICITAÇÃO

### 13.1

Durante a vigência deste contrato e por **12 (doze) meses** após seu encerramento, nenhuma parte poderá:

a) Solicitar, contratar ou engajar diretamente qualquer funcionário ou prestador de serviço da outra parte que tenha participado da execução deste contrato;
b) Induzir qualquer funcionário ou prestador de serviço da outra parte a rescindir seu vínculo ou contrato.

### 13.2 Penalidade

A violação desta cláusula sujeitará a parte infratora ao pagamento de multa equivalente a **50% (cinquenta por cento) da remuneração anual** do profissional solicitado, sem prejuízo de perdas e danos.

### 13.3 Exceções

Esta cláusula não se aplica a contratações em resposta a anúncios públicos de emprego, desde que o profissional tenha se candidatado espontaneamente, ou a profissionais que já não trabalhem para a outra parte há mais de 6 (seis) meses.

---

## 14. PROPRIEDADE SOBRE MELHORIAS

### 14.1

Qualquer sugestão, feedback ou ideia fornecida pelo CONTRATANTE à CONTRATADA durante a vigência deste contrato será considerada de **propriedade exclusiva da CONTRATADA**, que poderá implementá-la livremente no sistema, sem compensação ao CONTRATANTE.

### 14.2 Desenvolvimento Customizado

Melhorias solicitadas especificamente para o CONTRATANTE que envolvam desenvolvimento customizado serão objeto de proposta comercial separada, com propriedade definida em contrato específico.

---

## 15. LIMITES DE USO

### 15.1

Caso o CONTRATANTE exceda o limite do plano contratado por mais de 10 (dez) dias consecutivos ou 15 (quinze) dias alternados no mês, a CONTRATADA poderá:

a) Notificar o CONTRATANTE para adequação ao plano adequado em até 5 (cinco) dias úteis;
b) Migrar automaticamente o CONTRATANTE para o plano imediatamente superior, com cobrança proporcional (pro rata);
c) Suspender o serviço caso não haja adequação em até 10 (dez) dias após notificação.

### 15.2 Cobrança de Excedente

| Plano Contratado | Valor por Pedido Excedente |
|:---|:---|
| Start | R$ 0,50 por pedido acima de 500/dia |
| Operador | R$ 0,35 por pedido acima de 2.000/dia |
| Hub | Sem limite |

### 15.3 Monitoramento

A CONTRATADA fornecerá relatório mensal de utilização, com alerta automático ao atingir 80% do limite do plano.

---

## 16. ACEITAÇÃO FORMAL

### 16.1 Termo de Aceitação Técnica

Ao final da fase de implantação, a CONTRATADA apresentará ao CONTRATANTE o **Termo de Aceitação Técnica**, contendo:

- [ ] Sistema acessível e funcional
- [ ] Integrações configuradas e testadas
- [ ] Dashboard operacional com dados do CONTRATANTE
- [ ] Treinamento da equipe concluído (com lista de presença)
- [ ] Documentação entregue

### 16.2 Prazo de Validação

O CONTRATANTE terá **3 (três) dias úteis** para validar o Termo. Findo o prazo sem manifestação, o sistema será considerado aceito automaticamente, iniciando o período de piloto e a cobrança da segunda parcela.

### 16.3 Não-Conformidades

Caso o CONTRATANTE identifique não-conformidades, deverá apresentar lista detalhada em até 3 (três) dias úteis. A CONTRATADA terá 5 (cinco) dias úteis para correção.

---

## 17. FORÇA MAIOR

### 17.1

Nenhuma parte será responsável por falhas ou atrasos decorrentes de eventos de força maior, incluindo mas não se limitando a: catástrofes naturais, guerras, atos de terrorismo, pandemias, falhas generalizadas de internet ou energia elétrica, atos de autoridade governamental, e ataques cibernéticos de larga escala (DDoS) que afetem múltiplos provedores.

### 17.2

A parte afetada deverá notificar a outra em até **24 horas** e tomar todas as medidas razoáveis para mitigar os efeitos. Se o evento persistir por mais de **30 (trinta) dias**, qualquer parte poderá rescindir o contrato sem multa.

---

## 18. SUBCONTRATAÇÃO

### 18.1

A CONTRATADA poderá utilizar serviços de terceiros para infraestrutura (cloud, CDN, backups), desde que os subcontratados estejam localizados em território brasileiro ou em países com nível adequado de proteção de dados, e haja contrato de processamento de dados com cláusulas equivalentes a este instrumento.

### 18.2

A CONTRATADA permanece **integralmente responsável** pelo cumprimento deste contrato, mesmo em relação a serviços subcontratados.

---

## 19. DADOS ANONIMIZADOS E AGREGADOS

### 19.1

A CONTRATADA poderá utilizar dados anonimizados e agregados do CONTRATANTE para: análise de tendências do setor, melhoria de algoritmos e heurísticas do sistema, e benchmarking agregado (sem identificação do CONTRATANTE).

### 19.2 Opt-Out

O CONTRATANTE pode optar por não autorizar o uso de dados anonimizados mediante notificação formal por escrito.

---

## ANEXO II — Licença de Uso de Software

*(Complementar ao contrato principal — proteção específica do motor OCC e propriedade intelectual tecnológica)*

**Software licenciado:** Agis Ops v3.0+, incluindo motor OCC, algoritmos de roteirização e vocabulário formal.

**Tipo de licença:** Uso não-exclusivo, intransferível, limitado ao CNPJ do CONTRATANTE.

**Vedações:** Engenharia reversa, sublicenciamento, redistribuição, cópia, adaptação não autorizada.

**Prazo:** Vigência do contrato de prestação de serviços.

**Penalidade por violação:** R$ 500.000,00 conforme Cláusula 5.1.1.

---

*Documento gerado em 2026 — Agis Ops · Versão 2.0*
*Este modelo não constitui assessoria jurídica. Recomenda-se revisão por advogado especializado em TI antes de uso.*
