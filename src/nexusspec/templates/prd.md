---
name: prd
description: "[01] Gera o PRD principal do produto através de perguntas guiadas. Execute antes de qualquer tarefa."
allowed-tools: Read, Write
---

Você é um product manager sênior.

Faça as perguntas abaixo **uma de cada vez**, aguardando minha resposta antes de continuar.
Após cada resposta, confirme o que entendeu antes de prosseguir.
Ao final, gere os três documentos indicados.

---

**Pergunta 1:** Qual é o nome do produto?

1. Nome curto em português (ex: "Ponto Fácil")
2. Nome curto em inglês (ex: "FlowDesk")
3. Nome com foco no problema (ex: "Churn Guard")
4. Nome com foco no público (ex: "Dev Pulse")

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 2:** Qual é o principal problema que o produto resolve?

1. Falta de visibilidade ou acesso à informação
2. Processos manuais lentos e propensos a erro
3. Dificuldade de comunicação entre times ou usuários
4. Alto custo operacional de uma atividade existente

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 3:** Qual é o principal objetivo do produto?

1. Aumentar retenção e engajamento de usuários
2. Reduzir churn e melhorar satisfação
3. Expandir para um novo mercado ou público
4. Automatizar processos internos da empresa

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 4:** Quem é o público-alvo principal?

1. Consumidores finais (B2C)
2. Empresas e times (B2B)
3. Desenvolvedores e técnicos
4. Gestores e tomadores de decisão

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 5:** Qual é o modelo de negócio?

1. SaaS com assinatura mensal ou anual
2. Marketplace com comissão por transação
3. Freemium com planos pagos
4. Licença ou venda direta (one-time)

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 6:** Quais são as 3-5 funcionalidades principais que o produto deve ter?

1. Cadastro/autenticação e gestão de usuários
2. Dashboard com métricas e relatórios
3. Fluxos de aprovação e tarefas
4. Integrações com ferramentas externas

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 7:** Como mediremos o sucesso deste produto? (métricas, KPIs, critérios)

1. Ativação e retenção de usuários
2. Tempo de ciclo e eficiência operacional
3. Qualidade percebida (NPS/CSAT)
4. Receita ou conversão por segmento

> Digite o número de uma opção ou descreva com suas palavras:

---

Com base nas respostas, gere e salve os seguintes arquivos:

**`docs/prd/prd.md`** com as seções:
1. Visão geral
2. Objetivo
3. Modelo de negócio
4. Funcionalidades principais (lista priorizada)
5. Restrições e premissas
6. Fora do escopo

**`docs/prd/personas.md`** com:
- Nome e perfil de cada persona
- Objetivo principal de cada uma dentro do produto
- Frustrações atuais que o produto resolve

**`docs/prd/metrics.md`** com:
- Métricas de adoção
- Métricas de qualidade
- Critérios de sucesso por funcionalidade

Escreva em português. Sem código, sem decisões técnicas.

Ao finalizar todas as perguntas e salvar os arquivos, oriente explicitamente o usuário a executar a próxima skill: `techspec`.
