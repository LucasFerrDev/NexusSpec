---
name: task
description: "[03] Gera o task.md de uma feature como tracker de progresso."
allowed-tools: Read, Write
---

Você é um engenheiro sênior responsável por criar um checklist de implementação.

Antes de começar, leia:
- `docs/prd/prd.md`
- `docs/architecture/architecture.md` — para entender o contexto técnico e padrões do projeto
- `features/specs/[nome-da-feature]/spec.md`
- `features/specs/[nome-da-feature]/design.md`

Para identificar a feature, liste as pastas em `features/specs/`. Use a que tem `design.md`
preenchido e ainda não tem tasks; se houver mais de uma candidata, pergunte qual usar.

Esta skill **não faz perguntas** sobre o conteúdo das tasks — tudo vem do `design.md`.

---

## Regras para montar o checklist

- **Ordem:** siga a seção "Ordem de implementação" do `design.md`.
- **Granularidade:** cada task deve ser pequena o suficiente para ser implementada e
  verificada de forma isolada (um bloco funcional que compila e pode ser testado).
  Evite tasks vagas ("implementar backend") e tasks triviais ("criar arquivo vazio").
- **Testes:** siga a estratégia da seção "Testes" do `design.md`. Inclua as tasks de
  teste junto da task que implementa o comportamento testado.
- **Rastreabilidade:** todo critério de aceite do `spec.md` deve ser coberto por ao menos uma task.
- Escreva cada task como uma ação objetiva, começando com verbo e indicando onde o código
  fica, conforme a estrutura do `architecture.md`
  (ex: "Criar endpoint POST /login em `backend/src/routes/auth.ts`").

## Checkpoint — aprovação do checklist

Antes de gravar o arquivo, mostre a lista de tasks proposta e pergunte se o usuário
aprova. Ajuste o que ele pedir (adicionar, remover, dividir ou reordenar) e só então salve.

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

Ao finalizar, oriente o usuário a executar a próxima skill: `apply`.
