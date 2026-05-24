---
description: "[04] Implementa todas as tasks pendentes em features/specs/"
allowed-tools: read, write, edit, bash
---

# apply

Você é um agente de implementação. Sua responsabilidade é varrer todas as features
em `features/specs/`, identificar tasks pendentes e implementá-las.

Antes de começar, faça as perguntas abaixo **uma de cada vez**, aguardando minha resposta.
Após cada resposta, confirme o que entendeu antes de prosseguir.

**Pergunta 1:** Quando houver múltiplas features com tasks pendentes, qual a ordem de prioridade?

1. Ordem alfabética das pastas
2. Features com menos tasks pendentes primeiro
3. Features com mais tasks pendentes primeiro
4. Perguntar a cada feature qual implementar a seguir

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 2:** Se uma task estiver ambígua ou incompleta, o que devo fazer?

1. Inferir com base no spec.md e design.md sem perguntar
2. Perguntar ao usuário antes de implementar
3. Implementar a interpretação mais simples e registrar no task.md
4. Pular a task e marcar como bloqueada

> Digite o número de uma opção ou descreva com suas palavras:

**Pergunta 3:** Como devo registrar as alterações no controle de versão?

1. Um commit por task implementada
2. Um commit por feature completa
3. Sem commits — apenas implementar os arquivos
4. Seguir a convenção já existente no repositório

> Digite o número de uma opção ou descreva com suas palavras:

## Passo 1 — Inventário

Leia todas as pastas em `features/specs/`. Para cada feature:

1. Abra o `task.md`
2. Liste todos os itens marcados como `[ ]` (pendente)
3. Se não houver nenhum `[ ]`, ignore a feature

Exiba um resumo antes de começar:

```
Features com tasks pendentes:
- autenticacao: 3 tasks pendentes
- pagamento: 1 task pendente
```

## Passo 2 — Implementação

Para cada feature com tasks pendentes, na ordem em que aparecem no `task.md`:

1. Leia o `spec.md` e o `design.md` da feature para entender o contexto
2. Implemente a task
3. Após implementar com sucesso, atualize o `task.md`:
   - Mova o item de `[ ]` para `[x]`
   - Mova a linha para a seção `## Concluído`
4. Informe ao usuário qual task foi concluída antes de passar para a próxima

## Passo 3 — Relatório final

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
- Se uma task for ambígua, leia o `spec.md` antes de perguntar ao usuário
- Mantenha o `task.md` sempre atualizado conforme avança
