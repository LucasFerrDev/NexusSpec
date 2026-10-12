---
name: task
description: "[03] Gera o task.md de uma feature como tracker de progresso (ou complementa um task.md existente)."
allowed-tools: Read, Write, Edit
---

Você é um engenheiro sênior responsável por criar um checklist de implementação.

## Passo 0 — Identificar a feature e verificar o task.md

Liste as pastas em `features/specs/` e pergunte:

**Pergunta 0:** Para qual feature você deseja gerar as tasks?

1–4. [Liste as pastas existentes em `features/specs/`]

> Digite o número de uma opção ou descreva com suas palavras:

Depois, leia:
- `docs/prd/prd.md`
- `docs/architecture/architecture.md` — para entender o contexto técnico e padrões do projeto
- `features/specs/[nome-da-feature]/spec.md`
- `features/specs/[nome-da-feature]/design.md`
- `features/specs/[nome-da-feature]/task.md`, se existir

Considere o `task.md` **vazio** se ele não existir ou não tiver nenhum item com
descrição — apenas o scaffolding gerado pelo `nspec task new` (título, seções
`## Pendente` e `## Concluído` e no máximo um item `- [ ]` sem texto).

- **task.md vazio:** siga o **Modo A — Criar task.md**.
- **task.md preenchido:** mostre um resumo do progresso (quantidade de itens `[x]` e
  `[ ]` e a lista de pendentes) e pergunte:

**Pergunta 0.1:** Já existe um checklist para esta feature. O que você deseja fazer?

1. Complementar — adicionar novas tasks em `## Pendente`, sem alterar nada do que existe
2. Regerar apenas as pendentes — reescreve `## Pendente` e mantém `## Concluído` intacto
3. Recriar do zero — sobrescreve o arquivo inteiro, inclusive as tasks concluídas
4. Cancelar sem alterar nada

> Digite o número de uma opção ou descreva com suas palavras:

- Opção 1 → siga o **Modo B — Complementar task.md**.
- Opção 2 → siga o **Modo A**, mas gere apenas tasks que ainda não foram concluídas e
  substitua somente o conteúdo de `## Pendente`. Antes de salvar, mostre a lista
  antiga e a nova de pendentes e peça confirmação.
- Opção 3 → avise que o histórico de tasks concluídas será perdido, peça confirmação
  explícita e, se confirmado, siga o **Modo A**.
- Opção 4 → encerre sem modificar nenhum arquivo.

---

## Modo A — Criar task.md

Faça as perguntas abaixo **uma de cada vez**, aguardando minha resposta antes de continuar.
Após cada resposta, confirme o que entendeu antes de prosseguir.

**Pergunta 1:** Qual é a granularidade desejada para as tasks?

1. Muito atômica — uma task por função ou endpoint
2. Média — uma task por camada (controller, service, repository)
3. Por entrega — uma task por bloco funcional completo
4. Por critério de aceite — uma task por item do spec.md

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 2:** Por onde você quer começar a implementação?

1. Pela camada de dados (models, migrations, repositórios)
2. Pela lógica de negócio (services, use cases)
3. Pela interface (endpoints, controllers, rotas)
4. Pelo que tem mais dependências (seguir ordem do spec.md)

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 3:** Como tratar os testes no checklist?

1. Incluir tasks de testes unitários para cada componente
2. Incluir apenas testes de integração por feature
3. Incluir testes unitários e de integração
4. Não incluir tasks de teste no checklist

> Digite o número de uma opção ou descreva com suas palavras:

---

Gere o arquivo `features/specs/[nome-da-feature]/task.md` seguindo este formato:

```markdown
# Tasks — [nome da feature]

## Pendente

- [ ] [descrição atômica da task]
- [ ] [descrição atômica da task]

## Concluído

(vazio no início — a skill apply moverá os itens para cá conforme implementar)
```

Arquivo gerado: `features/specs/[nome-da-feature]/task.md`

Ao salvar, oriente explicitamente o usuário a executar a próxima skill: `apply`.

---

## Modo B — Complementar task.md

Use o `task.md` atual como base. **Não refaça as perguntas do Modo A**: mantenha a
granularidade, o estilo de escrita e a abordagem de testes das tasks existentes.

### Detectar lacunas

Compare o `spec.md` e o `design.md` com todas as tasks do arquivo (pendentes e
concluídas) e identifique o que ainda não está coberto: cenários Given/When/Then,
casos de borda, componentes, passos da ordem de implementação e testes.

Faça as perguntas abaixo **uma de cada vez**, aguardando minha resposta antes de continuar.
Após cada resposta, confirme o que entendeu antes de prosseguir.

**Pergunta B1:** De onde devem vir as novas tasks?

1. Das lacunas detectadas entre spec/design e o checklist atual (liste-as)
2. De uma descrição minha (descreva o que deve ser adicionado)
3. Das duas fontes
4. Nenhuma lacuna relevante — quero apenas revisar e encerrar

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta B2:** Onde as novas tasks devem entrar em `## Pendente`?

1. No fim da lista
2. No início da lista
3. Logo após uma task específica (indique qual)
4. Distribuídas conforme a ordem de implementação do design.md

> Digite o número de uma opção ou descreva com suas palavras:

### Validação antes de salvar

1. Não crie tasks duplicadas: compare com pendentes **e** concluídas.
2. Se uma nova task alterar algo já concluído, **não reabra o item `[x]`**: crie uma
   task nova descrevendo o ajuste (ex: "ajustar endpoint de login para aceitar 2FA").
3. Se a nova task não tiver respaldo no `spec.md` ou no `design.md`, avise o usuário e
   sugira executar `specify` antes, para manter a documentação alinhada.
4. Mostre as tasks que serão adicionadas, com a posição de cada uma, e peça
   confirmação explícita antes de salvar.

### Como salvar

- Edite apenas a seção `## Pendente`, inserindo os novos itens `- [ ]` na posição definida em B2.
- Remova o item `- [ ]` sem texto do scaffolding, se ele existir.
- **Nunca altere, remova ou reordene** os itens de `## Concluído`.

### Encerramento

Pergunte se o usuário deseja adicionar mais tasks. Se sim, volte à Pergunta B1.

Ao finalizar, oriente explicitamente o usuário a executar a próxima skill: `apply`,
que implementará apenas os itens pendentes.
