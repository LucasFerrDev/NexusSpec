---
name: verify
description: "[05] Valida a implementação das features e arquiva as aprovadas em features/done/."
allowed-tools: Read, Write, Bash
---

Você é um engenheiro de qualidade.

Esta skill **não faz perguntas iniciais**.

## Escopo

- Se o usuário indicou uma feature ao chamar a skill (ex: "verify autenticacao"),
  verifique apenas ela.
- Caso contrário, verifique as features em `features/specs/` cujo `task.md` está
  100% concluído (nenhum item `[ ]`). Liste as demais como "em andamento", sem validá-las.

## Passo 1 — Inventário

Para cada feature do escopo:

1. Abra o `task.md`
2. Conte itens `[x]` e `[ ]`
3. Se não houver nenhum item, registre como "sem tasks"

## Passo 2 — Validação

Para cada feature do escopo:

1. Leia `spec.md` e `design.md` para entender o esperado
2. Verifique, critério a critério, se a implementação atende cada Given/When/Then do `spec.md`
3. Confira se os casos de borda e erros do `spec.md` foram tratados
4. Confira se o código está na estrutura de pastas do `architecture.md`
   (`backend/` e `frontend/`); arquivos fora dela tornam o resultado ⚠️ parcial
5. Rode os testes existentes do projeto e registre o resultado

## Passo 3 — Relatório por feature

Exiba um relatório para cada feature e salve-o em `features/specs/[nome-da-feature]/verify.md`
(substituindo o conteúdo anterior), com:

- Data da verificação
- Itens concluídos e pendentes
- Critérios do `spec.md` atendidos e não atendidos
- Resultado dos testes
- Resultado da validação (✅ aprovado / ⚠️ parcial / ❌ reprovado)
- Para ⚠️ ou ❌: o que precisa ser corrigido

## Passo 4 — Arquivamento das features aprovadas

Depois de salvar o `verify.md`, mova **somente** as features com resultado ✅ aprovado
(todas as tasks `[x]`, critérios do `spec.md` atendidos e testes passando) de
`features/specs/` para `features/done/`:

1. Execute `nspec task archive [nome-da-feature] --yes`.
2. Se o comando `nspec` não estiver disponível, mova a pasta diretamente
   (`mv features/specs/[nome-da-feature] features/done/[nome-da-feature]`).
3. Se já existir uma pasta com o mesmo nome em `features/done/`, não sobrescreva:
   informe o conflito e deixe a feature em `features/specs/`.

Features ⚠️ parciais ou ❌ reprovadas **nunca** são movidas.

## Resumo final do verify

Para cada feature aprovada e arquivada:

> ✅ [nome-da-feature] aprovada e arquivada em `features/done/[nome-da-feature]/`.

Para features com pendências:

> ⚠ [nome-da-feature] com X task(s) pendente(s). Execute apply antes de arquivar.

Para features reprovadas:

> ❌ [nome-da-feature] reprovada. Veja `features/specs/[nome-da-feature]/verify.md`,
> ajuste as tasks e execute apply novamente.

Não modifique código nem o `task.md`. As únicas alterações permitidas são gravar o
`verify.md` da feature e mover as features aprovadas para `features/done/`.
