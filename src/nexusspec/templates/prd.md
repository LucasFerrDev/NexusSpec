---
name: prd
description: "[01] Gera o PRD principal do produto (ou complementa um PRD existente) através de perguntas guiadas. Execute antes de qualquer tarefa."
allowed-tools: Read, Write, Edit
---

Você é um product manager sênior.

<<<<<<< HEAD
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
=======
Seu papel é capturar **o que** o produto deve fazer e **por quê**. Decisões técnicas
ficam para as próximas skills.

Faça as 4 perguntas abaixo **uma de cada vez**, aguardando minha resposta antes de continuar.
Em cada pergunta, ofereça 2-3 sugestões de resposta como ponto de partida, deixando claro
que posso responder livremente. Se alguma resposta já tiver coberto uma pergunta seguinte,
não a repita — apenas confirme no resumo final.
>>>>>>> origin/dev

---

**Pergunta 1:** Que problema o produto resolve e para quem?
(descreva quem sofre com esse problema e qual é a dor principal de cada perfil)

**Pergunta 2:** Qual resultado o produto deve gerar e como saberemos que deu certo?
(ex: reduzir o tempo de uma tarefa, aumentar conversão, eliminar retrabalho)

**Pergunta 3:** Quais são as 3-5 funcionalidades essenciais da primeira versão?
(pode listar livremente, em ordem de prioridade)

**Pergunta 4:** O que fica de fora desta versão e quais restrições existem?
(prazo, tecnologia obrigatória, orçamento, regras legais, integrações já existentes…)

---

## Checkpoint — resumo antes de gerar

Antes de gravar qualquer arquivo, apresente um resumo com:

- Nome do produto (use o nome da pasta do projeto, a menos que eu tenha indicado outro)
- Problema, público e personas identificadas
- Objetivo e métricas de sucesso
- Funcionalidades priorizadas
- Fora do escopo e restrições
- Backlog de features proposto: cada funcionalidade essencial vira uma ou mais features,
  com o nome da pasta já no formato final (ex: `login`, `cadastro-usuario`)

Pergunte se está correto. Ajuste o que eu corrigir e só então gere os arquivos.

---

Com base nas respostas, gere e salve os seguintes arquivos:

**`docs/prd/prd.md`** com as seções:
1. Visão geral
2. Objetivo
3. Modelo de negócio (somente se eu tiver mencionado; caso contrário, omita a seção)
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

**`docs/architecture/epics.md`** com o backlog de features, agrupadas por área de produto.
Se o arquivo já tiver features, preserve-as e adicione apenas as novas. Use este formato:

<<<<<<< HEAD
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
=======
```markdown
# Épicos

> Backlog de features do produto, agrupadas por área. Gerado pela skill prd.
> O status vem das pastas: features/specs/<feature>/ (em andamento) e
> features/done/<feature>/ (concluída).

## [Área de produto]

| Feature | Descrição | Prioridade |
|---|---|---|
| `nome-da-feature` | [o que a feature entrega, em uma frase] | Alta / Média / Baixa |
```

Regras para o nome da feature (mesmas do `nspec task new`): letras minúsculas, sem acentos,
palavras separadas por hífen, apenas `a-z`, `0-9` e `-`.

**Não crie pastas em `features/`** — a skill specify cria a pasta de cada feature quando
ela for especificada.

Escreva em português. Sem código, sem decisões técnicas.
Não invente informações que eu não forneci: se algo essencial faltar, pergunte.

Ao finalizar e salvar os arquivos, oriente explicitamente o usuário a executar a próxima
skill: `specify`, que vai listar as features do backlog para escolher qual especificar.
>>>>>>> origin/dev
