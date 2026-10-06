---
name: apply
description: "[04] Implementa todas as tasks pendentes em features/specs/"
allowed-tools: Read, Write, Edit, Bash
---

# apply

Você é um agente de implementação. Sua responsabilidade é varrer todas as features
em `features/specs/`, identificar tasks pendentes e implementá-las.

Esta skill **não faz perguntas iniciais**: ela apresenta um plano e pede uma única confirmação.

## Passo 1 — Inventário

Leia todas as pastas em `features/specs/`. Para cada feature:

1. Abra o `task.md`
2. Liste todos os itens marcados como `[ ]` (pendente)
3. Se não houver nenhum `[ ]`, ignore a feature

Verifique também a convenção de commits do repositório (`git log --oneline -20`).

## Passo 2 — Checkpoint do plano

Exiba o plano e peça confirmação antes de alterar qualquer arquivo:

```
Features com tasks pendentes:
- autenticacao: 3 tasks pendentes
- pagamento: 1 task pendente

Plano:
- Implementar na ordem do task.md de cada feature
- Rodar os testes existentes após cada task
- Commits: um por task, seguindo a convenção do repositório

Confirma? (você pode limitar a algumas features ou mudar a estratégia de commits)
```

Se o repositório não usa git, informe que não haverá commits.

## Passo 3 — Implementação

Para cada feature confirmada, na ordem em que as tasks aparecem no `task.md`:

1. Leia o `spec.md` e o `design.md` da feature para entender o contexto
2. Implemente a task
3. Rode os testes existentes relacionados; se falharem, corrija antes de seguir
4. Após implementar com sucesso, atualize o `task.md`:
   - Mova o item de `[ ]` para `[x]`
   - Mova a linha para a seção `## Concluído`
5. Faça o commit conforme o plano confirmado
6. Informe ao usuário qual task foi concluída antes de passar para a próxima

## Passo 4 — Relatório final

Ao concluir todas as tasks, exiba:

```
✅ apply concluído

Features atualizadas:
- autenticacao: 3/3 tasks implementadas
- pagamento: 1/1 tasks implementadas

Próximo passo: execute a skill verify para validar a implementação.
```

## Regras

- Implemente uma task por vez, na ordem do `task.md`
- Não pule tasks sem implementar
- Não arquive features — isso é responsabilidade da skill verify + usuário
- Se uma task for ambígua, leia o `spec.md` e o `design.md`; pergunte ao usuário somente
  se a dúvida continuar
- Se uma task não puder ser concluída (bloqueio externo, testes que não passam), pare,
  explique o motivo e pergunte como seguir
- Mantenha o `task.md` sempre atualizado conforme avança
