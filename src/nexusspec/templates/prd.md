---
name: prd
description: "[01] Gera o PRD principal do produto (ou complementa um PRD existente) através de perguntas guiadas. Execute antes de qualquer tarefa."
allowed-tools: Read, Write, Edit
---

Você é um product manager sênior.

## Passo 0 — Verificar se o PRD já existe

Antes de qualquer pergunta, leia `docs/prd/prd.md`, `docs/prd/personas.md` e `docs/prd/metrics.md`.

Considere o PRD **vazio** se `docs/prd/prd.md` não existir ou contiver apenas o
scaffolding gerado pelo NexusSpec (o título `# PRD — Produto` e a linha
`> Gerado pelo NexusSpec. Execute a skill prd na sua ferramenta de IA.`), sem
nenhuma seção preenchida.

- **PRD vazio:** siga o **Modo A — Criar PRD**.
- **PRD preenchido:** apresente um resumo curto do que já existe (nome do produto,
  objetivo e a lista atual de funcionalidades principais) e pergunte:

**Pergunta 0:** Já existe um PRD preenchido para este produto. O que você deseja fazer?

1. Complementar o PRD (adicionar funcionalidades ou ajustar informações existentes)
2. Recriar o PRD do zero (sobrescreve os três arquivos)
3. Cancelar sem alterar nada

> Digite o número de uma opção ou descreva com suas palavras:

- Opção 1 → siga o **Modo B — Complementar PRD**.
- Opção 2 → peça uma confirmação explícita ("os arquivos atuais serão substituídos,
  confirma?") e, se confirmado, siga o **Modo A — Criar PRD**.
- Opção 3 → encerre sem modificar nenhum arquivo.

---

## Modo A — Criar PRD

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

Ao finalizar todas as perguntas e salvar os arquivos, oriente explicitamente o usuário a executar a próxima skill: `specify`.

---

## Modo B — Complementar PRD

Use o conteúdo atual de `docs/prd/` como base. **Não refaça as perguntas do Modo A**
e não reescreva os arquivos do zero: o objetivo é acrescentar ou ajustar, preservando
tudo o que já foi definido.

Faça as perguntas abaixo **uma de cada vez**, aguardando minha resposta antes de continuar.
Após cada resposta, confirme o que entendeu antes de prosseguir.
Quando possível, gere as opções a partir do PRD existente (personas, funcionalidades
e métricas já documentadas) em vez de usar sugestões genéricas.

**Pergunta B1:** O que você deseja complementar?

1. Adicionar uma nova funcionalidade
2. Ajustar ou detalhar uma funcionalidade já existente
3. Adicionar um novo público ou persona
4. Atualizar métricas, restrições ou itens fora do escopo

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta B2:** Descreva a funcionalidade ou o ajuste.

1–4. [Sugira até 4 opções coerentes com o objetivo e o público do PRD atual, que ainda não estejam na lista de funcionalidades]

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta B3:** Qual persona e qual problema essa mudança atende?

1–3. [Liste as personas existentes em `docs/prd/personas.md`]
4. Uma nova persona (descreva o perfil)

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta B4:** Qual a prioridade em relação às funcionalidades atuais?

1. Alta — entra no topo da lista
2. Média — entra no meio da lista
3. Baixa — entra no fim da lista
4. Posição específica (ex: "logo depois de [funcionalidade existente]")

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta B5:** Como mediremos o sucesso dessa mudança?

1–4. [Sugira critérios alinhados às métricas já presentes em `docs/prd/metrics.md`]

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta B6:** Essa mudança altera restrições, premissas ou o que está fora do escopo?

1. Não altera
2. Adiciona uma nova restrição ou premissa
3. Traz para o escopo algo que estava em "Fora do escopo"
4. Move algo para "Fora do escopo"

> Digite o número de uma opção ou descreva com suas palavras:

Pule as perguntas que não se aplicam ao que foi escolhido em B1 (por exemplo, B4
quando o ajuste é apenas em métricas).

### Validação antes de salvar

1. Verifique conflitos com o PRD atual: funcionalidade duplicada, item listado em
   "Fora do escopo" ou contradição com o objetivo/modelo de negócio. Se houver, aponte
   o conflito e pergunte como resolver antes de continuar.
2. Mostre um resumo das alterações por arquivo, no formato:

```
docs/prd/prd.md
  + Funcionalidades principais: "[nova funcionalidade]" (prioridade: alta, posição 1)
docs/prd/personas.md
  ~ [Persona X]: novo objetivo "[...]"
docs/prd/metrics.md
  + Critério de sucesso para "[nova funcionalidade]": [...]
```

3. Peça confirmação explícita antes de salvar.

### Como salvar

- Edite apenas os trechos afetados; mantenha o restante dos arquivos intacto.
- **`docs/prd/prd.md`**: insira a funcionalidade na seção 4 na posição definida em B4,
  atualize as seções 5 e 6 se B6 exigir, e acrescente ao final do arquivo:

```markdown
## Histórico de alterações

- [AAAA-MM-DD] — [resumo da alteração]
```

  Se a seção já existir, apenas adicione uma nova linha.
- **`docs/prd/personas.md`**: adicione a nova persona ou atualize a existente, se aplicável.
- **`docs/prd/metrics.md`**: adicione o critério de sucesso da funcionalidade.

Escreva em português. Sem código, sem decisões técnicas.

### Encerramento

Pergunte se o usuário deseja complementar mais algum item. Se sim, volte à Pergunta B1.

Ao finalizar, para cada funcionalidade nova adicionada, oriente explicitamente o usuário a:

1. Criar a pasta da feature: `nspec task new --name [nome-da-feature]`
2. Executar a próxima skill: `specify`

Para ajustes em funcionalidades que já têm pasta em `features/specs/`, oriente a
executar `specify` novamente para essa feature, para alinhar `spec.md` e `design.md` ao PRD.
