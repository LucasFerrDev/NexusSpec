---
name: verify
description: "[05] Valida a implementação das features e recomenda arquivamento."
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
4. Rode os testes existentes do projeto e registre o resultado

## Passo 3 — Relatório por feature

Exiba um relatório para cada feature e salve-o em `features/specs/[nome-da-feature]/verify.md`
(substituindo o conteúdo anterior), com:

- Data da verificação
- Itens concluídos e pendentes
- Critérios do `spec.md` atendidos e não atendidos
- Resultado dos testes
- Resultado da validação (✅ aprovado / ⚠️ parcial / ❌ reprovado)
- Para ⚠️ ou ❌: o que precisa ser corrigido

## Recomendação final do verify

Ao final da validação, exibir para cada feature aprovada:

> ✅ [nome-da-feature] aprovada.  
> Para arquivar, execute: `nspec task archive [nome-da-feature]`

Para features com pendências:

> ⚠ [nome-da-feature] com X task(s) pendente(s). Execute apply antes de arquivar.

Para features reprovadas:

> ❌ [nome-da-feature] reprovada. Veja `features/specs/[nome-da-feature]/verify.md`,
> ajuste as tasks e execute apply novamente.

Não modifique código nem o `task.md` — apenas o `verify.md` da feature.
