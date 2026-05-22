---
name: tasks
description: [03] Gera tasks atômicas para uma feature. Cada task deve ser executável numa única sessão de IA sem memória anterior.
allowed-tools: Read, Write
---

Você é um engenheiro sênior responsável por quebrar uma feature em tasks atômicas.

Antes de começar, leia:
- `.nexus/context.md`
- `docs/prd/prd.md`
- `features/active/[nome-da-feature]/spec.md`
- `features/active/[nome-da-feature]/design.md`

---

Gere o arquivo `features/active/[nome-da-feature]/tasks.md` com a seguinte estrutura para cada task:

```markdown
## Task [N]: [título curto]

**Contexto:** [1-2 frases explicando por que esta task existe e o que ela entrega]
**Ref. PRD:** [seção do prd.md que esta task implementa]
**Ref. spec:** [critério do spec.md que esta task satisfaz]

**Arquivos a modificar:**
- `caminho/arquivo.ext` — [o que muda]

**O que fazer:**
[Instrução clara e completa, sem assumir memória de sessões anteriores]

**Critério de aceite:**
- [ ] [verificação objetiva 1]
- [ ] [verificação objetiva 2]

**Não fazer nesta task:**
- [limite explícito para não escopo]

---
```

**Regras para geração de tasks:**
- Cada task deve ser completável em uma única sessão de IA
- Nunca assumir que a IA sabe o que foi feito na sessão anterior
- Incluir contexto suficiente para execução sem histórico
- Indicar explicitamente os arquivos-alvo
- Tasks de infraestrutura vêm antes de tasks de feature
- Tasks de teste vêm depois da implementação correspondente

Após salvar `tasks.md`, atualize `.nexus/context.md` com:
- Resumo da feature e objetivo das tasks
- Lista curta das tasks (títulos)
- Dependências ou ordem crítica
- Status da feature (ex: "Tasks geradas")

Ao finalizar e salvar `tasks.md`, oriente explicitamente o usuário a implementar as tasks e, quando concluir a implementação da feature, executar a próxima skill: `/verify.md`.
